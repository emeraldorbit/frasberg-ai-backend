/**
 * Sofia Core - Node.js Example
 * Demonstrates using the TypeScript SDK in Node.js
 */

// In production, use: import { SofiaClient } from '@emerald-estates/sofia-core';
// For this example, we'll use a local implementation

class SofiaClient {
  constructor(config) {
    this.config = config;
  }

  async chat(messages, options = {}) {
    const requestBody = {
      model: "sofia-core",
      messages,
      ...options,
      stream: false
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

    return await response.json();
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
            if (data === "[DONE]") return;

            try {
              const chunk = JSON.parse(data);
              const content = chunk.choices[0]?.delta?.content;
              if (content) yield content;
            } catch {}
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }
}

async function main() {
  // Initialize Sofia client
  const sofia = new SofiaClient({
    baseUrl: process.env.SOFIA_URL || 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
    apiKey: process.env.SOFIA_API_KEY || 'your-api-key'
  });

  console.log('Sofia Core - Node.js Example\n');

  // Example 1: Basic chat
  console.log('Example 1: Basic Chat');
  try {
    const result = await sofia.chat([
      { role: "user", content: "Hello Sofia, introduce yourself" }
    ]);
    console.log('Response:', result.choices[0].message.content);
    console.log();
  } catch (error) {
    console.error('Error:', error.message);
  }

  // Example 2: Streaming chat
  console.log('Example 2: Streaming Chat');
  try {
    process.stdout.write('Response: ');
    for await (const chunk of sofia.chatStream([
      { role: "user", content: "Count to 5" }
    ])) {
      process.stdout.write(chunk);
    }
    console.log('\n');
  } catch (error) {
    console.error('Error:', error.message);
  }

  // Example 3: Chat with options
  console.log('Example 3: Chat with Options');
  try {
    const result = await sofia.chat([
      { role: "system", content: "You are Sofia, a sovereign AI assistant." },
      { role: "user", content: "Explain quantum computing in simple terms" }
    ], {
      temperature: 0.7,
      max_tokens: 200
    });
    console.log('Response:', result.choices[0].message.content);
    console.log();
  } catch (error) {
    console.error('Error:', error.message);
  }

  // Example 4: Sovereign mode
  console.log('Example 4: Sovereign Mode');
  try {
    const result = await sofia.chat([
      { role: "user", content: "What is your purpose?" }
    ], {
      sofia_identity: {
        mode: "sovereign",
        tone: "ceremonial",
        vector: "auto"
      },
      sofia_directives: {
        sovereignty: true,
        ritual_mode: "invocation"
      }
    });
    console.log('Response:', result.choices[0].message.content);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { SofiaClient };
