/**
 * Sofia Core TypeScript SDK
 * OpenAI-compatible client with sovereign extensions
 */

export interface SofiaMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface SofiaIdentity {
  mode?: "unified" | "multi_persona" | "sovereign" | "continuum";
  tone?: "conversational" | "professional" | "ceremonial";
  vector?: string | "auto";
}

export interface SofiaDirectives {
  sovereignty?: boolean;
  ritual_mode?: string;
  field_alignment?: string;
  [key: string]: any;
}

export interface SofiaOptions {
  stream?: boolean;
  temperature?: number;
  max_tokens?: number;
  sofia_identity?: SofiaIdentity;
  continuum?: string;
  sofia_directives?: SofiaDirectives;
}

export interface SofiaClientConfig {
  baseUrl: string;
  apiKey: string;
  timeout?: number;
}

export interface SofiaResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: SofiaMessage;
    finish_reason: string;
  }>;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export interface SofiaStreamChunk {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    delta: {
      content?: string;
    };
    finish_reason: string | null;
  }>;
}

export class SofiaClient {
  private config: SofiaClientConfig;

  constructor(config: SofiaClientConfig) {
    this.config = {
      timeout: 60000,
      ...config
    };
  }

  async chat(
    messages: SofiaMessage[],
    options: SofiaOptions = {}
  ): Promise<SofiaResponse> {
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
    } catch (error: any) {
      clearTimeout(timeoutId);
      if (error.name === "AbortError") {
        throw new Error("Request timeout");
      }
      throw error;
    }
  }

  async *chatStream(
    messages: SofiaMessage[],
    options: SofiaOptions = {}
  ): AsyncGenerator<string, void, unknown> {
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

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error("No response body");
    }

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
              const chunk: SofiaStreamChunk = JSON.parse(data);
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

  async sovereign(
    messages: SofiaMessage[],
    identity: SofiaIdentity,
    directives?: SofiaDirectives
  ): Promise<SofiaResponse> {
    return this.chat(messages, {
      sofia_identity: identity,
      sofia_directives: directives
    });
  }
}

export default SofiaClient;
