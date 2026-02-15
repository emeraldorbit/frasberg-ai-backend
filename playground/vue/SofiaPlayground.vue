<template>
  <div class="playground-container">
    <div class="playground-header">
      <h1>🌟 Sofia Core Playground</h1>
      <p class="subtitle">OpenAI-compatible API with sovereign extensions</p>
      <input
        type="password"
        class="api-key-input"
        placeholder="Enter your API key"
        v-model="apiKey"
      />
    </div>

    <div class="messages-container" ref="messagesContainer">
      <div v-if="messages.length === 0" class="empty-state">
        <h2>👋 Welcome to Sofia Core</h2>
        <p>Start a conversation with the Sofia AI assistant</p>
      </div>

      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['message', msg.role]"
      >
        <div class="message-role">{{ msg.role.toUpperCase() }}</div>
        <div class="message-content">{{ msg.content }}</div>
      </div>

      <div v-if="loading" class="loading-indicator">
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
      </div>
    </div>

    <div class="input-container">
      <div v-if="error" class="error-message">{{ error }}</div>
      <div class="input-row">
        <textarea
          ref="inputRef"
          class="input-textarea"
          placeholder="Type your message..."
          v-model="input"
          @keydown="handleKeyDown"
          :disabled="loading"
        />
        <div class="button-group">
          <button
            class="btn btn-primary"
            @click="sendMessage"
            :disabled="loading || !input.trim()"
          >
            {{ loading ? 'Sending...' : 'Send' }}
          </button>
          <button class="btn btn-secondary" @click="clearConversation">
            Clear
          </button>
        </div>
      </div>
      <div class="keyboard-hint">
        Press Enter to send • Shift+Enter for new line
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue';

interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

interface SofiaIdentity {
  mode?: 'unified' | 'multi_persona' | 'sovereign' | 'continuum';
  tone?: 'conversational' | 'professional' | 'ceremonial';
  vector?: string;
}

const messages = ref<Message[]>([]);
const input = ref('');
const loading = ref(false);
const error = ref<string | null>(null);
const apiKey = ref('');
const apiUrl = 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend';
const messagesContainer = ref<HTMLDivElement | null>(null);
const inputRef = ref<HTMLTextAreaElement | null>(null);

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

watch(messages, () => {
  scrollToBottom();
}, { deep: true });

const sendMessage = async () => {
  if (!input.value.trim() || loading.value) return;
  if (!apiKey.value) {
    error.value = 'Please enter your API key';
    return;
  }

  const userMessage: Message = { role: 'user', content: input.value };
  messages.value.push(userMessage);
  input.value = '';
  loading.value = true;
  error.value = null;

  try {
    const response = await fetch(`${apiUrl}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`,
      },
      body: JSON.stringify({
        model: 'sofia-core',
        messages: messages.value,
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
    messages.value.push(assistantMessage);
  } catch (err: any) {
    error.value = err.message || 'Failed to send message';
    console.error('Error:', err);
  } finally {
    loading.value = false;
    inputRef.value?.focus();
  }
};

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
};

const clearConversation = () => {
  messages.value = [];
  error.value = null;
};
</script>

<style scoped>
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

.empty-state h2 {
  margin: 0 0 10px 0;
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

.loading-dot:nth-child(1) {
  animation-delay: -0.32s;
}
.loading-dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
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
