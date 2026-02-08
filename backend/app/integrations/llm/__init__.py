"""LLM Integration Router for v5.1"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional

from .openai_client import get_openai_client
from .anthropic_client import get_anthropic_client

router = APIRouter(prefix="/api/v5.1/llm", tags=["llm-real"])

class GenerateRequest(BaseModel):
    prompt: str
    provider: str = "openai"
    model: Optional[str] = None
    max_tokens: int = 1000
    temperature: float = 0.7
    system_prompt: Optional[str] = None
    stream: bool = False

@router.post("/generate")
async def generate_real(request: GenerateRequest):
    """Generate using real LLM providers"""
    
    if request.provider == "openai":
        client = get_openai_client()
        model = request.model or "gpt-4-turbo-preview"
        
        if request.stream:
            return StreamingResponse(
                client.generate_streaming(request.prompt, model, request.max_tokens, request.temperature),
                media_type="text/event-stream"
            )
        
        return client.generate(request.prompt, model, request.max_tokens, request.temperature, request.system_prompt)
    
    elif request.provider == "anthropic":
        client = get_anthropic_client()
        model = request.model or "claude-3-5-sonnet-20241022"
        
        if request.stream:
            return StreamingResponse(
                client.generate_streaming(request.prompt, model, request.max_tokens, request.temperature),
                media_type="text/event-stream"
            )
        
        return client.generate(request.prompt, model, request.max_tokens, request.temperature, request.system_prompt)
    
    else:
        return {"error": f"Unknown provider: {request.provider}"}

@router.get("/providers")
async def list_providers():
    """List available LLM providers and their status"""
    openai_client = get_openai_client()
    anthropic_client = get_anthropic_client()
    
    return {
        "providers": [
            {
                "name": "openai",
                "available": not openai_client.mock_mode,
                "models": ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"],
                "features": ["chat", "streaming", "embeddings"],
                "status": "ready" if not openai_client.mock_mode else "mock (API key not set)"
            },
            {
                "name": "anthropic",
                "available": not anthropic_client.mock_mode,
                "models": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-sonnet-20240229"],
                "features": ["chat", "streaming"],
                "status": "ready" if not anthropic_client.mock_mode else "mock (API key not set)"
            }
        ]
    }

@router.post("/embeddings")
async def generate_embeddings(text: str, model: str = "text-embedding-3-small"):
    """Generate embeddings using OpenAI"""
    client = get_openai_client()
    return client.generate_embeddings(text, model)
