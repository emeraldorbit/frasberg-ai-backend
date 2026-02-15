/**
 * Sofia Core JavaScript SDK
 * OpenAI-compatible client with sovereign extensions
 * Works in both Node.js and browser environments
 */

export class SofiaClient {
  constructor(config) {
    this.config = {
      timeout: 60000,
      ...config
    };
  }

  async chat(messages, options = {}) {
    const requestBody = {
      model: "sofia-core",
      messages,
      ...options,
      stream: false
    };

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.config.timeout);

    try {
      const response = await fetch(`${this.config.baseUrl}/v1/chat/completions`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.config.apiKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === "AbortError") {
        throw new Error("Request timeout");
      }
      throw error;
    }
  }

  async *chatStream(messages, options = {}) {
    const requestBody = {
      model: "sofia-core",
      messages,
      ...options,
      stream: true
    };

    const response = await fetch(`${this.config.baseUrl}/v1/chat/completions`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${this.config.apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `HTTP ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6);
            if (data === "[DONE]") {
              return;
            }

            try {
              const chunk = JSON.parse(data);
              const content = chunk.choices[0]?.delta?.content;
              if (content) {
                yield content;
              }
            } catch {
              // Ignore parse errors
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }

  async sovereign(messages, identity, directives = {}) {
    return this.chat(messages, {
      sofia_identity: identity,
      sofia_directives: directives
    });
  }
}

// For CommonJS compatibility
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SofiaClient };
}
