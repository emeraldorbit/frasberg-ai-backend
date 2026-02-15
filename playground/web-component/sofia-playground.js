class SofiaPlayground extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.messages = [];
    this.loading = false;
    this.apiKey = '';
    this.apiUrl = 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend';
  }

  connectedCallback() {
    this.render();
    this.attachEventListeners();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        }

        .playground-container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          max-width: 1200px;
          margin: 0 auto;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 20px;
          box-sizing: border-box;
        }

        .playground-header {
          background: white;
          padding: 20px;
          border-radius: 12px 12px 0 0;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .playground-header h1 {
          margin: 0 0 10px 0;
          color: #333;
          font-size: 24px;
        }

        .subtitle {
          margin: 0;
          color: #666;
          font-size: 14px;
        }

        .api-key-input {
          width: 100%;
          padding: 10px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 14px;
          margin-top: 10px;
          box-sizing: border-box;
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

        .empty-state {
          text-align: center;
          color: #999;
          padding: 40px;
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

        .message-content {
          white-space: pre-wrap;
        }

        .input-container {
          background: white;
          padding: 20px;
          border-radius: 0 0 12px 12px;
          box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
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

        .button-group {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }

        .btn {
          padding: 12px 24px;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
          white-space: nowrap;
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
      </style>

      <div class="playground-container">
        <div class="playground-header">
          <h1>🌟 Sofia Core Playground</h1>
          <p class="subtitle">OpenAI-compatible API with sovereign extensions</p>
          <input
            type="password"
            class="api-key-input"
            placeholder="Enter your API key"
            id="api-key"
          />
        </div>

        <div class="messages-container" id="messages-container">
          <div class="empty-state" id="empty-state">
            <h2>👋 Welcome to Sofia Core</h2>
            <p>Start a conversation with the Sofia AI assistant</p>
          </div>
        </div>

        <div class="input-container">
          <div class="error-message" id="error-message" style="display: none;"></div>
          <div class="input-row">
            <textarea
              class="input-textarea"
              placeholder="Type your message..."
              id="message-input"
            ></textarea>
            <div class="button-group">
              <button class="btn btn-primary" id="send-btn">Send</button>
              <button class="btn btn-secondary" id="clear-btn">Clear</button>
            </div>
          </div>
          <div class="keyboard-hint">
            Press Enter to send • Shift+Enter for new line • Ctrl+L to clear
          </div>
        </div>
      </div>
    `;
  }

  attachEventListeners() {
    const apiKeyInput = this.shadowRoot.getElementById('api-key');
    const messageInput = this.shadowRoot.getElementById('message-input');
    const sendBtn = this.shadowRoot.getElementById('send-btn');
    const clearBtn = this.shadowRoot.getElementById('clear-btn');

    apiKeyInput.addEventListener('input', (e) => {
      this.apiKey = e.target.value;
    });

    messageInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    sendBtn.addEventListener('click', () => this.sendMessage());
    clearBtn.addEventListener('click', () => this.clearConversation());
  }

  async sendMessage() {
    const messageInput = this.shadowRoot.getElementById('message-input');
    const input = messageInput.value.trim();

    if (!input || this.loading) return;
    
    if (!this.apiKey) {
      this.showError('Please enter your API key');
      return;
    }

    const userMessage = { role: 'user', content: input };
    this.messages.push(userMessage);
    this.updateMessages();
    messageInput.value = '';
    this.loading = true;
    this.updateSendButton();
    this.hideError();

    try {
      const response = await fetch(`${this.apiUrl}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify({
          model: 'sofia-core',
          messages: this.messages,
          stream: false,
        }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      const assistantMessage = {
        role: 'assistant',
        content: data.choices?.[0]?.message?.content || 'No response',
      };
      this.messages.push(assistantMessage);
      this.updateMessages();
    } catch (err) {
      this.showError(err.message || 'Failed to send message');
      console.error('Error:', err);
    } finally {
      this.loading = false;
      this.updateSendButton();
      messageInput.focus();
    }
  }

  updateMessages() {
    const container = this.shadowRoot.getElementById('messages-container');
    const emptyState = this.shadowRoot.getElementById('empty-state');

    if (this.messages.length === 0) {
      emptyState.style.display = 'block';
      return;
    }

    emptyState.style.display = 'none';

    // Remove existing messages but keep empty state
    const existingMessages = container.querySelectorAll('.message, .loading-indicator');
    existingMessages.forEach(el => el.remove());

    // Add all messages
    this.messages.forEach(msg => {
      const messageEl = document.createElement('div');
      messageEl.className = `message ${msg.role}`;
      messageEl.innerHTML = `
        <div class="message-role">${msg.role.toUpperCase()}</div>
        <div class="message-content">${this.escapeHtml(msg.content)}</div>
      `;
      container.appendChild(messageEl);
    });

    // Add loading indicator if loading
    if (this.loading) {
      const loadingEl = document.createElement('div');
      loadingEl.className = 'loading-indicator';
      loadingEl.innerHTML = `
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
      `;
      container.appendChild(loadingEl);
    }

    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
  }

  updateSendButton() {
    const sendBtn = this.shadowRoot.getElementById('send-btn');
    const messageInput = this.shadowRoot.getElementById('message-input');
    
    sendBtn.textContent = this.loading ? 'Sending...' : 'Send';
    sendBtn.disabled = this.loading || !messageInput.value.trim();
    messageInput.disabled = this.loading;
  }

  clearConversation() {
    this.messages = [];
    this.hideError();
    this.updateMessages();
  }

  showError(message) {
    const errorEl = this.shadowRoot.getElementById('error-message');
    errorEl.textContent = message;
    errorEl.style.display = 'block';
  }

  hideError() {
    const errorEl = this.shadowRoot.getElementById('error-message');
    errorEl.style.display = 'none';
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

customElements.define('sofia-playground', SofiaPlayground);
