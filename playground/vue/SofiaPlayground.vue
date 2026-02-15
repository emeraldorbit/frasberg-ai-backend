<template>
  <div class="sofia-playground">
    <h1>🜁 Sofia Core Playground</h1>
    
    <div class="config">
      <input
        v-model="apiKey"
        type="password"
        placeholder="API Key"
        class="api-key-input"
      />
      
      <div class="options">
        <label>
          <input v-model="sovereign" type="checkbox" />
          Sovereign Mode
        </label>
        
        <label>
          Temperature: {{ temperature.toFixed(1) }}
          <input
            v-model.number="temperature"
            type="range"
            min="0"
            max="2"
            step="0.1"
          />
        </label>
      </div>
    </div>

    <div class="messages-container">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['message', msg.role]"
      >
        <strong>{{ msg.role }}:</strong> {{ msg.content }}
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="input"
        type="text"
        placeholder="Type your message..."
        :disabled="loading"
        @keypress.enter="sendMessage(false)"
        class="message-input"
      />
      <button
        @click="sendMessage(false)"
        :disabled="loading || !input.trim() || !apiKey"
        class="send-btn"
      >
        Send
      </button>
      <button
        @click="sendMessage(true)"
        :disabled="loading || !input.trim() || !apiKey"
        class="stream-btn"
      >
        Stream
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

const props = defineProps<{
  baseUrl?: string;
  apiKey?: string;
}>();

const baseUrl = props.baseUrl || 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend';
const apiKey = ref(props.apiKey || '');
const messages = ref<Message[]>([]);
const input = ref('');
const loading = ref(false);
const sovereign = ref(false);
const temperature = ref(0.7);

const sendMessage = async (stream: boolean = false) => {
  if (!input.value.trim() || !apiKey.value) return;

  const userMessage: Message = { role: 'user', content: input.value };
  messages.value.push(userMessage);
  input.value = '';
  loading.value = true;

  try {
    const requestBody = {
      model: 'sofia-core',
      messages: messages.value,
      temperature: temperature.value,
      stream,
      ...(sovereign.value && {
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
        'Authorization': `Bearer ${apiKey.value}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    if (stream) {
      const assistantMessage: Message = { role: 'assistant', content: '' };
      messages.value.push(assistantMessage);

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
                  messages.value = [...messages.value];
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
      messages.value.push(assistantMessage);
    }
  } catch (error: any) {
    messages.value.push({
      role: 'assistant',
      content: `Error: ${error.message}`
    });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.sofia-playground {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #667eea;
  margin-bottom: 20px;
}

.config {
  margin-bottom: 20px;
}

.api-key-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
}

.options {
  display: flex;
  gap: 20px;
}

.messages-container {
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
}

.message.user {
  background-color: #e3f2fd;
}

.message.assistant {
  background-color: #fff;
}

.input-area {
  display: flex;
  gap: 10px;
}

.message-input {
  flex: 1;
  padding: 10px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
}

.send-btn,
.stream-btn {
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.send-btn:hover,
.stream-btn:hover {
  background: #5568d3;
}

.send-btn:disabled,
.stream-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
