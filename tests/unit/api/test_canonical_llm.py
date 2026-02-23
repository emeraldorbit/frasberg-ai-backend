"""Unit tests for the canonical LLM endpoint (POST /api/llm/generate).

Tests cover:
- env-var parsing and model resolution
- provider routing (openai / anthropic)
- response normalisation
- graceful error handling when env vars are missing or providers unknown
"""

import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Ensure the backend package is importable regardless of where pytest is run
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../backend"))

from backend.app.integrations.llm.canonical import (
    GenerateRequest,
    GenerateResponse,
    Message,
    _resolve_model,
    generate,
)


# ── _resolve_model ─────────────────────────────────────────────────────────


def test_resolve_model_none_uses_env(monkeypatch):
    monkeypatch.setenv("SOFIA_CORE_MODEL", "my-model")
    assert _resolve_model(None) == "my-model"


def test_resolve_model_sofia_core_uses_env(monkeypatch):
    monkeypatch.setenv("SOFIA_CORE_MODEL", "gpt-4.1")
    assert _resolve_model("sofia-core") == "gpt-4.1"


def test_resolve_model_explicit_passes_through(monkeypatch):
    monkeypatch.setenv("SOFIA_CORE_MODEL", "gpt-4.1")
    assert _resolve_model("gpt-4o") == "gpt-4o"


def test_resolve_model_default_when_env_missing(monkeypatch):
    monkeypatch.delenv("SOFIA_CORE_MODEL", raising=False)
    assert _resolve_model(None) == "gpt-4.1"


# ── generate — missing LLM_API_KEY ─────────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_missing_api_key_raises_503(monkeypatch):
    from fastapi import HTTPException

    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.setenv("LLM_PROVIDER", "openai")

    req = GenerateRequest(messages=[Message(role="user", content="hello")])
    with pytest.raises(HTTPException) as exc_info:
        await generate(req)
    assert exc_info.value.status_code == 503
    assert "LLM_API_KEY" in exc_info.value.detail


# ── generate — unknown provider ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_unknown_provider_raises_400(monkeypatch):
    from fastapi import HTTPException

    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_PROVIDER", "unknown_provider")

    req = GenerateRequest(messages=[Message(role="user", content="hello")])
    with pytest.raises(HTTPException) as exc_info:
        await generate(req)
    assert exc_info.value.status_code == 400
    assert "unknown_provider" in exc_info.value.detail


# ── generate — openai routing ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_routes_to_openai(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "sk-test")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("SOFIA_CORE_MODEL", "gpt-4.1")
    monkeypatch.setenv("SOFIA_CORE_TEMPERATURE", "0.2")
    monkeypatch.setenv("SOFIA_CORE_MAX_TOKENS", "4096")

    with patch(
        "backend.app.integrations.llm.canonical._call_openai",
        new_callable=AsyncMock,
        return_value=("Hello from OpenAI", 10, 5),
    ) as mock_openai, patch(
        "backend.app.integrations.llm.canonical._log_usage_to_supabase",
        new_callable=AsyncMock,
    ):
        req = GenerateRequest(
            model="sofia-core",
            messages=[Message(role="user", content="hello")],
        )
        result = await generate(req)

    assert isinstance(result, GenerateResponse)
    assert result.output == "Hello from OpenAI"
    assert result.usage.input_tokens == 10
    assert result.usage.output_tokens == 5
    mock_openai.assert_awaited_once()
    # Verify the resolved model was passed
    call_args = mock_openai.call_args
    assert call_args.args[1] == "gpt-4.1"


# ── generate — anthropic routing ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_routes_to_anthropic(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "anthro-key")
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("SOFIA_CORE_MODEL", "claude-3-5-sonnet-20241022")

    with patch(
        "backend.app.integrations.llm.canonical._call_anthropic",
        new_callable=AsyncMock,
        return_value=("Hello from Anthropic", 20, 8),
    ) as mock_anthropic, patch(
        "backend.app.integrations.llm.canonical._log_usage_to_supabase",
        new_callable=AsyncMock,
    ):
        req = GenerateRequest(
            model="sofia-core",
            messages=[Message(role="user", content="hi")],
        )
        result = await generate(req)

    assert result.output == "Hello from Anthropic"
    assert result.usage.input_tokens == 20
    mock_anthropic.assert_awaited_once()


# ── generate — explicit model override ────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_explicit_model_overrides_env(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "sk-test")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("SOFIA_CORE_MODEL", "gpt-4.1")

    with patch(
        "backend.app.integrations.llm.canonical._call_openai",
        new_callable=AsyncMock,
        return_value=("output", 1, 1),
    ) as mock_openai, patch(
        "backend.app.integrations.llm.canonical._log_usage_to_supabase",
        new_callable=AsyncMock,
    ):
        req = GenerateRequest(
            model="gpt-4o",
            messages=[Message(role="user", content="test")],
        )
        await generate(req)

    call_args = mock_openai.call_args
    assert call_args.args[1] == "gpt-4o"


# ── _log_usage_to_supabase — no Supabase configured ───────────────────────


@pytest.mark.asyncio
async def test_log_usage_skips_when_supabase_not_configured(monkeypatch, caplog):
    import logging

    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)

    from backend.app.integrations.llm.canonical import _log_usage_to_supabase

    with caplog.at_level(logging.DEBUG, logger="backend.app.integrations.llm.canonical"):
        await _log_usage_to_supabase("openai", "gpt-4.1", 10, 5)

    assert "Supabase not configured" in caplog.text


# ── HTTP endpoint integration ─────────────────────────────────────────────


def test_canonical_endpoint_missing_key_returns_503(monkeypatch):
    """Verify the FastAPI route also returns 503 when LLM_API_KEY is absent."""
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.setenv("LLM_PROVIDER", "openai")

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from backend.app.integrations.llm.canonical import router as canonical_router

    _app = FastAPI()
    _app.include_router(canonical_router)

    client = TestClient(_app, raise_server_exceptions=False)
    response = client.post(
        "/api/llm/generate",
        json={
            "model": "sofia-core",
            "messages": [{"role": "user", "content": "hello"}],
        },
    )
    assert response.status_code == 503
