"""
Sofia Core OpenAI-Compatible Client
Provides OpenAI-style chat completions API
"""

import requests
from typing import Dict, Any, Optional, List, Iterator
from .exceptions import APIError, ValidationError


class SofiaCoreClient:
    """OpenAI-compatible client for Sofia Core"""
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 60):
        """
        Initialize Sofia Core client
        
        Args:
            base_url: Base URL of Sofia Core API
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        sofia_identity: Optional[Dict[str, Any]] = None,
        continuum: Optional[str] = None,
        sofia_directives: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a chat completion
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            sofia_identity: Sofia identity configuration
            continuum: Continuum identifier
            sofia_directives: Sofia-specific directives
            
        Returns:
            Chat completion response
        """
        payload = {
            "model": "sofia-core",
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if sofia_identity is not None:
            payload["sofia_identity"] = sofia_identity
        if continuum is not None:
            payload["continuum"] = continuum
        if sofia_directives is not None:
            payload["sofia_directives"] = sofia_directives
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422:
                raise ValidationError(str(e))
            raise APIError(f"API request failed: {e}")
        except Exception as e:
            raise APIError(f"Request failed: {e}")
    
    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        sofia_identity: Optional[Dict[str, Any]] = None,
        continuum: Optional[str] = None,
        sofia_directives: Optional[Dict[str, Any]] = None
    ) -> Iterator[str]:
        """
        Create a streaming chat completion
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            sofia_identity: Sofia identity configuration
            continuum: Continuum identifier
            sofia_directives: Sofia-specific directives
            
        Yields:
            Content chunks as they arrive
        """
        payload = {
            "model": "sofia-core",
            "messages": messages,
            "temperature": temperature,
            "stream": True
        }
        
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if sofia_identity is not None:
            payload["sofia_identity"] = sofia_identity
        if continuum is not None:
            payload["continuum"] = continuum
        if sofia_directives is not None:
            payload["sofia_directives"] = sofia_directives
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        data = line_text[6:]
                        if data == '[DONE]':
                            break
                        
                        try:
                            import json
                            chunk = json.loads(data)
                            content = chunk.get('choices', [{}])[0].get('delta', {}).get('content')
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
                            
        except requests.exceptions.HTTPError as e:
            raise APIError(f"API request failed: {e}")
        except Exception as e:
            raise APIError(f"Request failed: {e}")
    
    def sovereign(
        self,
        messages: List[Dict[str, str]],
        identity: Dict[str, Any],
        directives: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a chat completion with sovereign mode
        
        Args:
            messages: List of message dicts
            identity: Sofia identity configuration
            directives: Sofia-specific directives
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Chat completion response
        """
        return self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            sofia_identity=identity,
            sofia_directives=directives
        )
