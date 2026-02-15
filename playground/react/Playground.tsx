import React, { useState } from 'react';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface SofiaPlaygroundProps {
  baseUrl?: string;
  apiKey?: string;
}

export const SofiaPlayground: React.FC<SofiaPlaygroundProps> = ({
  baseUrl = 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
  apiKey: initialApiKey = ''
}) => {
  const [apiKey, setApiKey] = useState(initialApiKey);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const [sovereign, setSovereign] = useState(false);
  const [temperature, setTemperature] = useState(0.7);

  const sendMessage = async (stream: boolean = false) => {
    if (!input.trim() || !apiKey) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const requestBody = {
        model: 'sofia-core',
        messages: [...messages, userMessage],
        temperature,
        stream,
        ...(sovereign && {
          sofia_identity: {
            mode: 'sovereign',
            tone: 'ceremonial',
            vector: 'auto'
          },
          sofia_directives: {
            sovereignty: true,
            ritual_mode: 'invocation'
          }
        })
      };

      const response = await fetch(`${baseUrl}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      if (stream) {
        let assistantMessage: Message = { role: 'assistant', content: '' };
        setMessages(prev => [...prev, assistantMessage]);

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (reader) {
          let buffer = '';
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') break;

                try {
                  const chunk = JSON.parse(data);
                  const content = chunk.choices[0]?.delta?.content;
                  if (content) {
                    assistantMessage.content += content;
                    setMessages(prev => [...prev.slice(0, -1), { ...assistantMessage }]);
                  }
                } catch {}
              }
            }
          }
        }
      } else {
        const result = await response.json();
        const assistantMessage: Message = {
          role: 'assistant',
          content: result.choices[0].message.content
        };
        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error: any) {
      const errorMessage: Message = {
        role: 'assistant',
        content: `Error: ${error.message}`
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>🜁 Sofia Core Playground</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="password"
          placeholder="API Key"
          value={apiKey}
          onChange={e => setApiKey(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        
        <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
          <label>
            <input
              type="checkbox"
              checked={sovereign}
              onChange={e => setSovereign(e.target.checked)}
            />
            Sovereign Mode
          </label>
          
          <label>
            Temperature: {temperature.toFixed(1)}
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={temperature}
              onChange={e => setTemperature(parseFloat(e.target.value))}
            />
          </label>
        </div>
      </div>

      <div style={{
        border: '1px solid #ccc',
        borderRadius: '8px',
        padding: '20px',
        minHeight: '300px',
        maxHeight: '500px',
        overflowY: 'auto',
        marginBottom: '20px',
        backgroundColor: '#f5f5f5'
      }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              marginBottom: '15px',
              padding: '10px',
              borderRadius: '8px',
              backgroundColor: msg.role === 'user' ? '#e3f2fd' : '#fff',
              border: '1px solid #ddd'
            }}
          >
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && !loading && sendMessage(streaming)}
          disabled={loading}
          style={{ flex: 1, padding: '10px' }}
        />
        <button
          onClick={() => sendMessage(false)}
          disabled={loading || !input.trim() || !apiKey}
          style={{ padding: '10px 20px' }}
        >
          Send
        </button>
        <button
          onClick={() => sendMessage(true)}
          disabled={loading || !input.trim() || !apiKey}
          style={{ padding: '10px 20px' }}
        >
          Stream
        </button>
      </div>
    </div>
  );
};

export default SofiaPlayground;
