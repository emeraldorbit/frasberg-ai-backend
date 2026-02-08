"""Real OpenAI Integration for Sofia Core v5.1"""
import os
from typing import Optional, Dict, Any, AsyncIterator
import logging

logger = logging.getLogger(__name__)

class OpenAIClient:
    """Production-ready OpenAI integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OpenAI API key not set. Will return mock responses.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                logger.warning("OpenAI library not installed. Using mock mode.")
                self.mock_mode = True
    
    def generate(
        self, 
        prompt: str, 
        model: str = "gpt-4-turbo-preview",
        max_tokens: int = 1000, 
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate completion using OpenAI"""
        
        if self.mock_mode:
            return self._mock_generate(prompt, model)
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": model,
                "provider": "openai",
                "tokens_used": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason,
                "mock": False
            }
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {"error": str(e), "provider": "openai", "mock": False}
    
    async def generate_streaming(
        self,
        prompt: str,
        model: str = "gpt-4-turbo-preview",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """Stream completion from OpenAI"""
        if self.mock_mode:
            yield f"[MOCK STREAMING] {prompt[:50]}..."
            return
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"OpenAI streaming error: {e}")
            yield f"[ERROR] {str(e)}"
    
    def generate_embeddings(self, text: str, model: str = "text-embedding-3-small") -> Dict[str, Any]:
        """Generate embeddings for text"""
        if self.mock_mode:
            return {"embedding": [0.1] * 1536, "model": model, "mock": True}
        
        try:
            response = self.client.embeddings.create(
                model=model,
                input=text
            )
            return {
                "embedding": response.data[0].embedding,
                "model": model,
                "tokens_used": response.usage.total_tokens,
                "mock": False
            }
        except Exception as e:
            logger.error(f"OpenAI embeddings error: {e}")
            return {"error": str(e), "mock": False}
    
    def _mock_generate(self, prompt: str, model: str) -> Dict[str, Any]:
        """Mock response when API key not available"""
        return {
            "response": f"[MOCK OPENAI] Response to: {prompt[:50]}...\n\nThis is a simulated response. Set OPENAI_API_KEY environment variable for real responses.",
            "model": model,
            "provider": "openai",
            "tokens_used": 150,
            "finish_reason": "stop",
            "mock": True
        }

# Global instance
def get_openai_client() -> OpenAIClient:
    """Get or create OpenAI client singleton"""
    if not hasattr(get_openai_client, "_instance"):
        get_openai_client._instance = OpenAIClient()
    return get_openai_client._instance
