"""
Sofia Core - Python Example
Demonstrates using the Python SDK with Sofia Core
"""

import os
import requests
from typing import Dict, Any, List, Iterator


class SofiaCoreClient:
    """OpenAI-compatible client for Sofia Core"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Create a chat completion"""
        payload = {
            "model": "sofia-core",
            "messages": messages,
            "stream": False,
            **kwargs
        }
        
        response = self.session.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    
    def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> Iterator[str]:
        """Create a streaming chat completion"""
        payload = {
            "model": "sofia-core",
            "messages": messages,
            "stream": True,
            **kwargs
        }
        
        response = self.session.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
            stream=True,
            timeout=60
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


def main():
    """Run examples"""
    
    # Initialize Sofia client
    sofia = SofiaCoreClient(
        base_url=os.getenv('SOFIA_URL', 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend'),
        api_key=os.getenv('SOFIA_API_KEY', 'your-api-key')
    )
    
    print('Sofia Core - Python Example\n')
    
    # Example 1: Basic chat
    print('Example 1: Basic Chat')
    try:
        result = sofia.chat([
            {"role": "user", "content": "Hello Sofia, introduce yourself"}
        ])
        print('Response:', result['choices'][0]['message']['content'])
        print()
    except Exception as e:
        print(f'Error: {e}')
    
    # Example 2: Streaming chat
    print('Example 2: Streaming Chat')
    try:
        print('Response: ', end='', flush=True)
        for chunk in sofia.chat_stream([
            {"role": "user", "content": "Count to 5"}
        ]):
            print(chunk, end='', flush=True)
        print('\n')
    except Exception as e:
        print(f'Error: {e}')
    
    # Example 3: Chat with options
    print('Example 3: Chat with Options')
    try:
        result = sofia.chat([
            {"role": "system", "content": "You are Sofia, a sovereign AI assistant."},
            {"role": "user", "content": "Explain quantum computing in simple terms"}
        ], temperature=0.7, max_tokens=200)
        print('Response:', result['choices'][0]['message']['content'])
        print()
    except Exception as e:
        print(f'Error: {e}')
    
    # Example 4: Sovereign mode
    print('Example 4: Sovereign Mode')
    try:
        result = sofia.chat([
            {"role": "user", "content": "What is your purpose?"}
        ], sofia_identity={
            "mode": "sovereign",
            "tone": "ceremonial",
            "vector": "auto"
        }, sofia_directives={
            "sovereignty": True,
            "ritual_mode": "invocation"
        })
        print('Response:', result['choices'][0]['message']['content'])
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
