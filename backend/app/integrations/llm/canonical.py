"""Canonical LLM endpoint for Sofia Core.

Reads LLM_PROVIDER, LLM_API_KEY, SOFIA_CORE_MODEL,
SOFIA_CORE_TEMPERATURE, and SOFIA_CORE_MAX_TOKENS to route requests to
the appropriate provider and return a normalised response.
"""

import logging
import os
from typing import List, Optional, Tuple

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# ── defaults read once at import time; endpoint re-reads per request so that
#    env vars set after import (e.g. in tests) are picked up correctly.
_DEFAULT_MODEL = "gpt-4.1"
_DEFAULT_TEMPERATURE = 0.2
_DEFAULT_MAX_TOKENS = 4096

router = APIRouter(prefix="/api/llm", tags=["llm-canonical"])


# ── Request / Response models ──────────────────────────────────────────────


class Message(BaseModel):
    role: str
    content: str


class GenerateRequest(BaseModel):
    model: Optional[str] = Field(
        default=None,
        description=(
            "Model to use for generation. Pass ``'sofia-core'`` or omit to use "
            "the ``SOFIA_CORE_MODEL`` environment variable (default: ``gpt-4.1``). "
            "Any other value is forwarded verbatim to the provider."
        ),
    )
    messages: List[Message]


class UsageInfo(BaseModel):
    input_tokens: int
    output_tokens: int


class GenerateResponse(BaseModel):
    output: str
    usage: UsageInfo


# ── Helpers ────────────────────────────────────────────────────────────────


def _resolve_model(requested: Optional[str]) -> str:
    """Return the concrete model name.

    Uses SOFIA_CORE_MODEL env var when the request model is ``"sofia-core"``
    or omitted.
    """
    if not requested or requested == "sofia-core":
        return os.getenv("SOFIA_CORE_MODEL", _DEFAULT_MODEL)
    return requested


async def _call_openai(
    api_key: str,
    model: str,
    messages: List[dict],
    temperature: float,
    max_tokens: int,
) -> Tuple[str, int, int]:
    """Call OpenAI chat completions and return (output, input_tokens, output_tokens)."""
    try:
        from openai import AsyncOpenAI  # type: ignore
    except ImportError as exc:
        raise HTTPException(
            status_code=503, detail="openai library not installed"
        ) from exc

    try:
        client = AsyncOpenAI(api_key=api_key)
        response = await client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore[arg-type]
            temperature=temperature,
            max_tokens=max_tokens,
        )
        output = response.choices[0].message.content or ""
        input_tokens = response.usage.prompt_tokens if response.usage else 0
        output_tokens = response.usage.completion_tokens if response.usage else 0
        return output, input_tokens, output_tokens
    except Exception as exc:
        logger.error("OpenAI API error: %s", exc)
        raise HTTPException(
            status_code=502, detail=f"OpenAI request failed: {exc}"
        ) from exc


async def _call_anthropic(
    api_key: str,
    model: str,
    messages: List[dict],
    temperature: float,
    max_tokens: int,
) -> Tuple[str, int, int]:
    """Call Anthropic messages API and return (output, input_tokens, output_tokens)."""
    try:
        from anthropic import AsyncAnthropic  # type: ignore
    except ImportError as exc:
        raise HTTPException(
            status_code=503, detail="anthropic library not installed"
        ) from exc

    try:
        # Anthropic separates the system prompt from the user/assistant turns.
        system = ""
        user_messages = []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                user_messages.append(m)

        kwargs: dict = {
            "model": model,
            "messages": user_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if system:
            kwargs["system"] = system

        client = AsyncAnthropic(api_key=api_key)
        response = await client.messages.create(**kwargs)
        output = response.content[0].text if response.content else ""
        input_tokens = response.usage.input_tokens if response.usage else 0
        output_tokens = response.usage.output_tokens if response.usage else 0
        return output, input_tokens, output_tokens
    except Exception as exc:
        logger.error("Anthropic API error: %s", exc)
        raise HTTPException(
            status_code=502, detail=f"Anthropic request failed: {exc}"
        ) from exc


async def _log_usage_to_supabase(
    provider: str, model: str, input_tokens: int, output_tokens: int
) -> None:
    """Fire-and-forget usage log to Supabase.

    Does **not** log prompt content or secrets.  Silently skips when
    SUPABASE_URL / SUPABASE_KEY are not configured.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        logger.debug("Supabase not configured; skipping usage logging.")
        return

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                f"{supabase_url}/functions/v1/log-event",
                headers={
                    "Authorization": f"Bearer {supabase_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "event_type": "llm_usage",
                    "data": {
                        "provider": provider,
                        "model": model,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                    },
                },
            )
    except Exception as exc:
        logger.warning("Usage logging to Supabase failed (non-fatal): %s", exc)


async def generate(request: GenerateRequest) -> GenerateResponse:
    """Core generation logic — shared by the HTTP endpoint and agent wrappers."""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    api_key = os.getenv("LLM_API_KEY")
    model = _resolve_model(request.model)

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail=(
                "LLM_API_KEY is not configured. "
                "Set the LLM_API_KEY environment variable to enable LLM generation."
            ),
        )

    try:
        temperature = float(os.getenv("SOFIA_CORE_TEMPERATURE", str(_DEFAULT_TEMPERATURE)))
        if not 0.0 <= temperature <= 2.0:
            raise ValueError
    except ValueError:
        logger.warning(
            "SOFIA_CORE_TEMPERATURE is invalid; falling back to %.1f", _DEFAULT_TEMPERATURE
        )
        temperature = _DEFAULT_TEMPERATURE

    try:
        max_tokens = int(os.getenv("SOFIA_CORE_MAX_TOKENS", str(_DEFAULT_MAX_TOKENS)))
        if max_tokens < 1:
            raise ValueError
    except ValueError:
        logger.warning(
            "SOFIA_CORE_MAX_TOKENS is invalid; falling back to %d", _DEFAULT_MAX_TOKENS
        )
        max_tokens = _DEFAULT_MAX_TOKENS

    messages = [m.model_dump() for m in request.messages]

    if provider == "openai":
        output, input_tokens, output_tokens = await _call_openai(
            api_key, model, messages, temperature, max_tokens
        )
    elif provider == "anthropic":
        output, input_tokens, output_tokens = await _call_anthropic(
            api_key, model, messages, temperature, max_tokens
        )
    else:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unknown LLM_PROVIDER '{provider}'. "
                "Supported values: openai, anthropic."
            ),
        )

    await _log_usage_to_supabase(provider, model, input_tokens, output_tokens)

    return GenerateResponse(
        output=output,
        usage=UsageInfo(input_tokens=input_tokens, output_tokens=output_tokens),
    )


# ── HTTP endpoint ──────────────────────────────────────────────────────────


@router.post("/generate", response_model=GenerateResponse)
async def canonical_generate(request: GenerateRequest) -> GenerateResponse:
    """Canonical LLM generation endpoint.

    Reads ``LLM_PROVIDER`` and ``LLM_API_KEY`` from the environment and
    routes the request to the appropriate provider.  When ``model`` is
    ``"sofia-core"`` or omitted the defaults from ``SOFIA_CORE_MODEL``,
    ``SOFIA_CORE_TEMPERATURE``, and ``SOFIA_CORE_MAX_TOKENS`` are applied.
    """
    return await generate(request)
