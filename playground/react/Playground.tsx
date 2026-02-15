import React, { useState, useRef, useEffect } from 'react';

interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

interface SofiaIdentity {
  mode?: 'unified' | 'multi_persona' | 'sovereign' | 'continuum';
  tone?: 'conversational' | 'professional' | 'ceremonial';
  vector?: string;
}

const Playground: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiKey, setApiKey] = useState('');
  const [apiUrl] = useState('https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    if (!apiKey) {
      setError('Please enter your API key');
      return;
    }

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiUrl}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: 'sofia-core',
          messages: [...messages, userMessage],
          stream: false,
        }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.choices?.[0]?.message?.content || 'No response',
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err.message || 'Failed to send message');
      console.error('Error:', err);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearConversation = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="playground-container">
      <style>{`
        .playground-container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          max-width: 1200px;
          margin: 0 auto;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 20px;
        }

        .playground-header {
          background: white;
          padding: 20px;
          border-radius: 12px 12px 0 0;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .playground-header h1 {
          margin: 0 0 10px 0;
          color: #333;
          font-size: 24px;
        }

        .api-key-input {
          width: 100%;
          padding: 10px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 14px;
          margin-top: 10px;
        }

        .messages-container {
          flex: 1;
          overflow-y: auto;
          background: white;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        .message {
          display: flex;
          flex-direction: column;
          max-width: 80%;
          padding: 12px 16px;
          border-radius: 12px;
          word-wrap: break-word;
        }

        .message.user {
          align-self: flex-end;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .message.assistant {
          align-self: flex-start;
          background: #f5f5f5;
          color: #333;
        }

        .message-role {
          font-size: 12px;
          font-weight: 600;
          margin-bottom: 5px;
          opacity: 0.8;
        }

        .input-container {
          background: white;
          padding: 20px;
          border-radius: 0 0 12px 12px;
          box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }

        .input-row {
          display: flex;
          gap: 10px;
        }

        .input-textarea {
          flex: 1;
          padding: 12px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 14px;
          font-family: inherit;
          resize: none;
          min-height: 60px;
        }

        .input-textarea:focus {
          outline: none;
          border-color: #667eea;
        }

        .btn {
          padding: 12px 24px;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }

        .btn-primary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .btn-primary:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .btn-primary:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .btn-secondary {
          background: #f5f5f5;
          color: #666;
        }

        .btn-secondary:hover {
          background: #e0e0e0;
        }

        .error-message {
          background: #fee;
          color: #c33;
          padding: 12px;
          border-radius: 8px;
          margin-bottom: 10px;
        }

        .loading-indicator {
          display: flex;
          gap: 5px;
          padding: 12px 16px;
          background: #f5f5f5;
          border-radius: 12px;
          align-self: flex-start;
          max-width: 80%;
        }

        .loading-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #667eea;
          animation: bounce 1.4s infinite ease-in-out both;
        }

        .loading-dot:nth-child(1) { animation-delay: -0.32s; }
        .loading-dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }

        .keyboard-hint {
          font-size: 12px;
          color: #999;
          margin-top: 8px;
          text-align: center;
        }

        @media (max-width: 768px) {
          .playground-container {
            padding: 10px;
          }
          .message {
            max-width: 90%;
          }
        }
      `}</style>

      <div className="playground-header">
        <h1>🌟 Sofia Core Playground</h1>
        <p style={{ margin: 0, color: '#666', fontSize: '14px' }}>
          OpenAI-compatible API with sovereign extensions
        </p>
        <input
          type="password"
          className="api-key-input"
          placeholder="Enter your API key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
      </div>

      <div className="messages-container">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: '#999', padding: '40px' }}>
            <h2>👋 Welcome to Sofia Core</h2>
            <p>Start a conversation with the Sofia AI assistant</p>
          </div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-role">{msg.role.toUpperCase()}</div>
            <div>{msg.content}</div>
          </div>
        ))}
        {loading && (
          <div className="loading-indicator">
            <div className="loading-dot"></div>
            <div className="loading-dot"></div>
            <div className="loading-dot"></div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        {error && <div className="error-message">{error}</div>}
        <div className="input-row">
          <textarea
            ref={inputRef}
            className="input-textarea"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <button
              className="btn btn-primary"
              onClick={sendMessage}
              disabled={loading || !input.trim()}
            >
              {loading ? 'Sending...' : 'Send'}
            </button>
            <button
              className="btn btn-secondary"
              onClick={clearConversation}
            >
              Clear
            </button>
          </div>
        </div>
        <div className="keyboard-hint">
          Press Enter to send • Shift+Enter for new line • Ctrl+L to clear
        </div>
      </div>
    </div>
  );
};

export default Playground;
