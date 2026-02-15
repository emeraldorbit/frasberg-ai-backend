# Sofia Core Vue Playground

A modern Vue 3 playground using Composition API and TypeScript for testing the Sofia Core API.

## Features

✅ Vue 3 Composition API  
✅ Full TypeScript support  
✅ Reactive conversation history  
✅ Real-time message updates  
✅ Loading states with animations  
✅ Error handling  
✅ Keyboard shortcuts  
✅ Responsive design  
✅ Professional styling  

## Installation

### Prerequisites

- Node.js 18+
- Vue 3.3+
- TypeScript 5+

### Setup

```bash
# Install dependencies
npm install vue

# Or with yarn
yarn add vue

# For TypeScript support
npm install --save-dev @vue/compiler-sfc typescript
```

## Usage

### Basic Integration

```typescript
// main.ts
import { createApp } from 'vue';
import SofiaPlayground from './SofiaPlayground.vue';

const app = createApp(SofiaPlayground);
app.mount('#app');
```

### In Existing Vue App

```vue
<template>
  <div>
    <h1>My Sofia Core Application</h1>
    <SofiaPlayground />
  </div>
</template>

<script setup lang="ts">
import SofiaPlayground from './components/SofiaPlayground.vue';
</script>
```

### Standalone HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sofia Core Vue Playground</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

## Configuration

### API Key

Users enter their API key in the header input field. The key is stored in reactive state:

```typescript
const apiKey = ref('');
```

### API Endpoint

Default endpoint:
```
https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend
```

To customize, modify the `apiUrl` constant:

```typescript
const apiUrl = 'YOUR_CUSTOM_ENDPOINT';
```

## Composition API Structure

```typescript
<script setup lang="ts">
// Reactive State
const messages = ref<Message[]>([]);
const input = ref('');
const loading = ref(false);
const error = ref<string | null>(null);
const apiKey = ref('');

// Refs
const messagesContainer = ref<HTMLDivElement | null>(null);
const inputRef = ref<HTMLTextAreaElement | null>(null);

// Functions
const sendMessage = async () => { ... };
const handleKeyDown = (e: KeyboardEvent) => { ... };
const clearConversation = () => { ... };
const scrollToBottom = async () => { ... };

// Watchers
watch(messages, () => {
  scrollToBottom();
}, { deep: true });
</script>
```

## TypeScript Interfaces

```typescript
interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

interface SofiaIdentity {
  mode?: 'unified' | 'multi_persona' | 'sovereign' | 'continuum';
  tone?: 'conversational' | 'professional' | 'ceremonial';
  vector?: string;
}
```

## Template Structure

```vue
<template>
  <div class="playground-container">
    <!-- Header -->
    <div class="playground-header">
      <h1>🌟 Sofia Core Playground</h1>
      <p class="subtitle">OpenAI-compatible API with sovereign extensions</p>
      <input type="password" class="api-key-input" v-model="apiKey" />
    </div>

    <!-- Messages -->
    <div class="messages-container" ref="messagesContainer">
      <div v-if="messages.length === 0" class="empty-state">
        <h2>👋 Welcome to Sofia Core</h2>
        <p>Start a conversation with the Sofia AI assistant</p>
      </div>
      
      <div v-for="(msg, idx) in messages" :key="idx" :class="['message', msg.role]">
        <div class="message-role">{{ msg.role.toUpperCase() }}</div>
        <div class="message-content">{{ msg.content }}</div>
      </div>

      <div v-if="loading" class="loading-indicator">
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
      </div>
    </div>

    <!-- Input -->
    <div class="input-container">
      <div v-if="error" class="error-message">{{ error }}</div>
      <div class="input-row">
        <textarea
          ref="inputRef"
          class="input-textarea"
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
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift + Enter` | New line in message |
| `Ctrl + L` | Clear conversation (planned) |

## Reactivity

### Reactive State Management

```typescript
// Messages automatically update UI
messages.value.push(newMessage);

// Loading state controls UI elements
loading.value = true;

// Error handling
error.value = 'Error message';
```

### Watchers

Auto-scroll on message updates:

```typescript
watch(messages, () => {
  scrollToBottom();
}, { deep: true });
```

## Styling

Scoped styles ensure no conflicts with parent applications:

```vue
<style scoped>
.playground-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
```

### Customization

Override styles using CSS variables or deep selectors:

```vue
<style>
:deep(.playground-container) {
  --primary-color: #your-color;
}
</style>
```

## Error Handling

Comprehensive error management:

- **Missing API Key**: User prompt
- **Network Errors**: Display connection issues
- **API Errors**: Show HTTP status and details
- **Invalid Responses**: Handle malformed data

```typescript
try {
  const response = await fetch(...);
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }
} catch (err: any) {
  error.value = err.message || 'Failed to send message';
}
```

## Development

### Run Development Server

```bash
# Vite
npm run dev

# Or Vue CLI
npm run serve
```

### Build for Production

```bash
# Vite
npm run build

# Preview
npm run preview
```

### Type Checking

```bash
npm run type-check
```

## Testing

### Manual Testing

1. Enter API key
2. Type a message
3. Press Enter
4. Verify message appears
5. Check loading state
6. Verify response displays

### Unit Testing with Vitest

```typescript
import { mount } from '@vue/test-utils';
import SofiaPlayground from './SofiaPlayground.vue';

describe('SofiaPlayground', () => {
  it('renders properly', () => {
    const wrapper = mount(SofiaPlayground);
    expect(wrapper.text()).toContain('Sofia Core Playground');
  });

  it('sends message on enter', async () => {
    const wrapper = mount(SofiaPlayground);
    const textarea = wrapper.find('textarea');
    await textarea.setValue('Hello');
    await textarea.trigger('keydown.enter');
    // Assert message was sent
  });
});
```

## Performance

### Optimization Tips

1. **Use `v-memo` for message lists** (Vue 3.2+):
```vue
<div v-for="msg in messages" :key="msg.id" v-memo="[msg.content]">
```

2. **Lazy load images** in messages:
```vue
<img :src="msg.image" loading="lazy" />
```

3. **Virtual scrolling** for long conversations:
```bash
npm install vue-virtual-scroller
```

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Vite Configuration

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
```

## TypeScript Configuration

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## Accessibility

- Semantic HTML elements
- Keyboard navigation
- ARIA labels (enhance as needed)
- Screen reader support (enhance as needed)
- High contrast colors

## Security

- API key in component state (not persisted)
- No console logging of sensitive data
- HTTPS-only API calls
- Input validation

## Troubleshooting

### Issue: TypeScript Errors

**Solution**: Ensure `@vue/compiler-sfc` is installed and TypeScript is properly configured.

### Issue: Styles Not Scoped

**Solution**: Verify `<style scoped>` is used and no global style conflicts exist.

### Issue: Reactivity Not Working

**Solution**: Ensure you're using `ref()` or `reactive()` and accessing values with `.value`.

### Issue: Watch Not Triggering

**Solution**: Add `{ deep: true }` option for nested object watching.

## Vue Devtools

Install Vue Devtools for debugging:
- Chrome: https://chrome.google.com/webstore
- Firefox: https://addons.mozilla.org/firefox

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following Vue 3 best practices
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file in repository root

## Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [Composition API Guide](https://vuejs.org/guide/extras/composition-api-faq.html)
- [TypeScript with Vue](https://vuejs.org/guide/typescript/overview.html)
- [OpenAPI Schema](../../openapi/sofia-core.json)
- [Deployment Guide](../../docs/deployment.md)

## Related Playgrounds

- [React Playground](../react/Playground.tsx)
- [Web Component](../web-component/sofia-playground.js)
