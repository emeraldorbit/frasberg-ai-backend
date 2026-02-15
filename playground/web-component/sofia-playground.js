class SofiaPlayground extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.messages = [];
    this.loading = false;
  }

  connectedCallback() {
    this.baseUrl = this.getAttribute('base-url') || 
      'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend';
    this.render();
    this.attachEventListeners();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        h1 {
          color: #667eea;
          margin-bottom: 20px;
        }

        .config {
          margin-bottom: 20px;
        }

        input[type="password"],
        input[type="text"] {
          width: 100%;
          padding: 10px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 14px;
        }

        .options {
          display: flex;
          gap: 20px;
          margin-top: 10px;
        }

        .messages {
          border: 1px solid #ccc;
          border-radius: 8px;
          padding: 20px;
          min-height: 300px;
          max-height: 500px;
          overflow-y: auto;
          margin-bottom: 20px;
          background-color: #f5f5f5;
        }

        .message {
          margin-bottom: 15px;
          padding: 10px;
          border-radius: 8px;
          border: 1px solid #ddd;
          background-color: #fff;
        }

        .message.user {
          background-color: #e3f2fd;
        }

        .input-area {
          display: flex;
          gap: 10px;
        }

        button {
          padding: 10px 20px;
          background: #667eea;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-size: 14px;
          font-weight: 600;
        }

        button:hover:not(:disabled) {
          background: #5568d3;
        }

        button:disabled {
          background: #ccc;
          cursor: not-allowed;
        }

        input[type="range"] {
          width: 100px;
        }
      </style>

      <h1>🜁 Sofia Core Playground</h1>
      
      <div class="config">
        <input
          type="password"
          id="apiKey"
          placeholder="API Key"
        />
        
        <div class="options">
          <label>
            <input type="checkbox" id="sovereign" />
            Sovereign Mode
          </label>
          
          <label>
            Temperature: <span id="tempValue">0.7</span>
            <input
              type="range"
              id="temperature"
              min="0"
              max="2"
              step="0.1"
              value="0.7"
            />
          </label>
        </div>
      </div>

      <div class="messages" id="messages"></div>

      <div class="input-area">
        <input
          type="text"
          id="messageInput"
          placeholder="Type your message..."
        />
        <button id="sendBtn">Send</button>
        <button id="streamBtn">Stream</button>
      </div>
    `;
  }

  attachEventListeners() {
    const sendBtn = this.shadowRoot.getElementById('sendBtn');
    const streamBtn = this.shadowRoot.getElementById('streamBtn');
    const messageInput = this.shadowRoot.getElementById('messageInput');
    const tempSlider = this.shadowRoot.getElementById('temperature');
    const tempValue = this.shadowRoot.getElementById('tempValue');

    sendBtn.addEventListener('click', () => this.sendMessage(false));
    streamBtn.addEventListener('click', () => this.sendMessage(true));
    
    messageInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !this.loading) {
        this.sendMessage(false);
      }
    });

    tempSlider.addEventListener('input', (e) => {
      tempValue.textContent = e.target.value;
    });
  }

  async sendMessage(stream = false) {
    if (this.loading) return;

    const apiKey = this.shadowRoot.getElementById('apiKey').value;
    const messageInput = this.shadowRoot.getElementById('messageInput');
    const message = messageInput.value.trim();
    const sovereign = this.shadowRoot.getElementById('sovereign').checked;
    const temperature = parseFloat(this.shadowRoot.getElementById('temperature').value);

    if (!apiKey || !message) return;

    this.addMessage('user', message);
    messageInput.value = '';
    this.loading = true;
    this.updateButtons();

    try {
      const requestBody = {
        model: 'sofia-core',
        messages: this.messages,
        temperature,
        stream
      };

      if (sovereign) {
        requestBody.sofia_identity = {
          mode: 'sovereign',
          tone: 'ceremonial',
          vector: 'auto'
        };
        requestBody.sofia_directives = {
          sovereignty: true,
          ritual_mode: 'invocation'
        };
      }

      const response = await fetch(`${this.baseUrl}/v1/chat/completions`, {
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
        await this.handleStreamResponse(response);
      } else {
        const result = await response.json();
        this.addMessage('assistant', result.choices[0].message.content);
      }
    } catch (error) {
      this.addMessage('assistant', `Error: ${error.message}`);
    } finally {
      this.loading = false;
      this.updateButtons();
    }
  }

  async handleStreamResponse(response) {
    const messageEl = this.createMessageElement('assistant', '');
    let content = '';

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
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
            const deltaContent = chunk.choices[0]?.delta?.content;
            if (deltaContent) {
              content += deltaContent;
              messageEl.textContent = `assistant: ${content}`;
            }
          } catch {}
        }
      }
    }

    this.messages.push({ role: 'assistant', content });
  }

  addMessage(role, content) {
    this.messages.push({ role, content });
    this.createMessageElement(role, content);
  }

  createMessageElement(role, content) {
    const messagesDiv = this.shadowRoot.getElementById('messages');
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    messageEl.innerHTML = `<strong>${role}:</strong> ${content}`;
    messagesDiv.appendChild(messageEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return messageEl;
  }

  updateButtons() {
    const sendBtn = this.shadowRoot.getElementById('sendBtn');
    const streamBtn = this.shadowRoot.getElementById('streamBtn');
    sendBtn.disabled = this.loading;
    streamBtn.disabled = this.loading;
  }
}

customElements.define('sofia-playground', SofiaPlayground);
