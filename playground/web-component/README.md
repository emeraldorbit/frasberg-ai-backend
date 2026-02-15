# Sofia Core Web Component Playground

A framework-agnostic Web Component for testing the Sofia Core API. Works with any JavaScript framework or vanilla HTML.

## Features

✅ Framework-agnostic (works everywhere)  
✅ Native Web Components (Custom Elements)  
✅ Shadow DOM encapsulation  
✅ Zero external dependencies  
✅ Full conversation history  
✅ Loading states and animations  
✅ Error handling  
✅ Keyboard shortcuts  
✅ Responsive design  
✅ Professional styling  

## Installation

### CDN (Easiest)

```html
<!DOCTYPE html>
<html>
<head>
  <title>Sofia Core Playground</title>
</head>
<body>
  <sofia-playground></sofia-playground>
  
  <script src="https://cdn.jsdelivr.net/gh/emeraldorbit/sofia-core-backend/playground/web-component/sofia-playground.js"></script>
</body>
</html>
```

### NPM Package (Coming Soon)

```bash
npm install @sofia-core/playground
```

### Local File

```html
<!DOCTYPE html>
<html>
<head>
  <title>Sofia Core Playground</title>
</head>
<body>
  <sofia-playground></sofia-playground>
  
  <script src="./sofia-playground.js"></script>
</body>
</html>
```

## Usage

### Vanilla HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sofia Core Playground</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <sofia-playground></sofia-playground>
  
  <script src="./sofia-playground.js"></script>
</body>
</html>
```

### React

```jsx
import React from 'react';

function App() {
  return (
    <div>
      <h1>My Sofia Core App</h1>
      <sofia-playground></sofia-playground>
    </div>
  );
}

export default App;
```

### Vue

```vue
<template>
  <div>
    <h1>My Sofia Core App</h1>
    <sofia-playground></sofia-playground>
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    // Component is automatically available
  }
}
</script>
```

### Angular

```typescript
// app.component.ts
import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

@Component({
  selector: 'app-root',
  template: '<sofia-playground></sofia-playground>',
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppComponent {}
```

```typescript
// app.module.ts
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

@NgModule({
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule {}
```

### Svelte

```svelte
<script>
  import { onMount } from 'svelte';
  
  onMount(() => {
    // Component is loaded from script tag
  });
</script>

<h1>My Sofia Core App</h1>
<sofia-playground></sofia-playground>
```

## Configuration

### Attributes (Future Enhancement)

```html
<sofia-playground
  api-url="https://your-api.com"
  theme="dark"
  initial-message="Hello!"
></sofia-playground>
```

### JavaScript API

```javascript
const playground = document.querySelector('sofia-playground');

// Access internal state
console.log(playground.messages);
console.log(playground.loading);

// Programmatically send message
playground.sendMessage();

// Clear conversation
playground.clearConversation();

// Set API key
playground.apiKey = 'your-api-key';
```

## Web Component Structure

### Custom Element Definition

```javascript
class SofiaPlayground extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.messages = [];
    this.loading = false;
    this.apiKey = '';
  }

  connectedCallback() {
    this.render();
    this.attachEventListeners();
  }
}

customElements.define('sofia-playground', SofiaPlayground);
```

### Shadow DOM

The component uses Shadow DOM for style encapsulation:

```javascript
this.shadowRoot.innerHTML = `
  <style>
    /* Scoped styles */
  </style>
  <div class="playground-container">
    <!-- Component HTML -->
  </div>
`;
```

## API Reference

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `messages` | `Array` | Conversation history |
| `loading` | `Boolean` | Loading state |
| `apiKey` | `String` | API authentication key |
| `apiUrl` | `String` | API endpoint URL |

### Methods

| Method | Description |
|--------|-------------|
| `sendMessage()` | Sends the current input message |
| `clearConversation()` | Clears all messages |
| `updateMessages()` | Re-renders message list |
| `showError(message)` | Displays error message |
| `hideError()` | Hides error message |

### Events (Future Enhancement)

```javascript
const playground = document.querySelector('sofia-playground');

playground.addEventListener('message-sent', (e) => {
  console.log('Message sent:', e.detail);
});

playground.addEventListener('response-received', (e) => {
  console.log('Response:', e.detail);
});

playground.addEventListener('error', (e) => {
  console.error('Error:', e.detail);
});
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift + Enter` | New line in message |
| `Ctrl + L` | Clear conversation (planned) |

## Styling

### Shadow DOM Styles

Styles are encapsulated in Shadow DOM and won't leak to or from the parent page.

### Custom Styling (Future Enhancement)

Using CSS custom properties:

```html
<style>
  sofia-playground {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --text-color: #333;
    --background-color: #fff;
  }
</style>

<sofia-playground></sofia-playground>
```

### Theme Override

```javascript
const playground = document.querySelector('sofia-playground');
const style = document.createElement('style');
style.textContent = `
  .playground-container {
    background: linear-gradient(135deg, #ff6b6b, #4ecdc4) !important;
  }
`;
playground.shadowRoot.appendChild(style);
```

## Browser Support

| Browser | Version | Supported |
|---------|---------|-----------|
| Chrome | 53+ | ✅ |
| Firefox | 63+ | ✅ |
| Safari | 10.1+ | ✅ |
| Edge | 79+ | ✅ |
| IE | 11 | ❌ (use polyfill) |

### Polyfills

For older browsers:

```html
<script src="https://unpkg.com/@webcomponents/webcomponentsjs@latest/webcomponents-loader.js"></script>
<script src="./sofia-playground.js"></script>
```

## Development

### Local Development

1. Create an HTML file:
```html
<!DOCTYPE html>
<html>
<body>
  <sofia-playground></sofia-playground>
  <script src="./sofia-playground.js"></script>
</body>
</html>
```

2. Serve with any local server:
```bash
# Python
python -m http.server 8000

# Node.js
npx serve

# PHP
php -S localhost:8000
```

3. Open http://localhost:8000

### Debugging

```javascript
// Enable debug mode
const playground = document.querySelector('sofia-playground');
playground.debug = true;

// Access internal state
console.log(playground.messages);
console.log(playground.shadowRoot);
```

## Testing

### Manual Testing

1. Load component in browser
2. Enter API key
3. Type message
4. Press Enter
5. Verify message displays
6. Check loading state
7. Verify response appears

### Automated Testing (Playwright)

```javascript
import { test, expect } from '@playwright/test';

test('sofia playground works', async ({ page }) => {
  await page.goto('http://localhost:8000');
  
  // Find component
  const playground = await page.locator('sofia-playground');
  
  // Enter API key
  const apiKeyInput = playground.locator('input[type="password"]');
  await apiKeyInput.fill('test-api-key');
  
  // Send message
  const messageInput = playground.locator('textarea');
  await messageInput.fill('Hello Sofia');
  
  const sendButton = playground.locator('button:has-text("Send")');
  await sendButton.click();
  
  // Wait for response
  await expect(playground.locator('.message.assistant')).toBeVisible();
});
```

### Unit Testing (Jest)

```javascript
import './sofia-playground.js';

describe('SofiaPlayground', () => {
  let element;

  beforeEach(() => {
    element = document.createElement('sofia-playground');
    document.body.appendChild(element);
  });

  afterEach(() => {
    element.remove();
  });

  test('renders correctly', () => {
    expect(element.shadowRoot.querySelector('.playground-container')).toBeTruthy();
  });

  test('sends message', async () => {
    element.apiKey = 'test-key';
    const input = element.shadowRoot.querySelector('#message-input');
    input.value = 'Test message';
    
    await element.sendMessage();
    
    expect(element.messages.length).toBeGreaterThan(0);
  });
});
```

## Performance

### Optimization Tips

1. **Lazy loading**: Load component only when needed
```javascript
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const script = document.createElement('script');
        script.src = './sofia-playground.js';
        document.body.appendChild(script);
        observer.disconnect();
      }
    });
  });
  observer.observe(document.querySelector('#playground-container'));
}
```

2. **Virtual scrolling**: For long conversations
3. **Debounced input**: Reduce re-renders

### Bundle Size

- Minified: ~12KB
- Gzipped: ~4KB
- Zero external dependencies

## Security

### XSS Prevention

```javascript
escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
```

### Best Practices

- API key not persisted to localStorage
- Input sanitization
- HTTPS-only API calls
- Content Security Policy compatible
- No eval() or innerHTML with user data

## Accessibility

### Keyboard Navigation

- Tab through interactive elements
- Enter to send messages
- Escape to clear (planned)

### Screen Readers (Future Enhancement)

```javascript
// Add ARIA labels
<div role="log" aria-live="polite" aria-label="Chat messages">
  {messages}
</div>
```

### Color Contrast

- WCAG AA compliant color ratios
- High contrast mode support

## Troubleshooting

### Issue: Component Not Rendering

**Solution**: Ensure script is loaded before DOM:
```html
<sofia-playground></sofia-playground>
<script src="./sofia-playground.js"></script>
```

### Issue: Styles Not Applied

**Solution**: Check Shadow DOM is attached:
```javascript
console.log(playground.shadowRoot);
```

### Issue: Events Not Working

**Solution**: Ensure event listeners are attached after render:
```javascript
connectedCallback() {
  this.render();
  this.attachEventListeners(); // After render
}
```

### Issue: CORS Errors

**Solution**: 
- Verify API supports CORS
- Use proper authentication
- Check browser console for details

## Migration Guide

### From React Component

```jsx
// Before (React)
<Playground />

// After (Web Component)
<sofia-playground></sofia-playground>
```

### From Vue Component

```vue
<!-- Before (Vue) -->
<SofiaPlayground />

<!-- After (Web Component) -->
<sofia-playground></sofia-playground>
```

## Advanced Usage

### Custom Themes

```javascript
class ThemedSofiaPlayground extends SofiaPlayground {
  constructor() {
    super();
    this.theme = 'dark';
  }
  
  render() {
    super.render();
    if (this.theme === 'dark') {
      this.applyDarkTheme();
    }
  }
  
  applyDarkTheme() {
    const style = document.createElement('style');
    style.textContent = `
      .playground-container {
        background: #1a1a1a;
        color: #fff;
      }
    `;
    this.shadowRoot.appendChild(style);
  }
}

customElements.define('themed-sofia-playground', ThemedSofiaPlayground);
```

### Multiple Instances

```html
<sofia-playground id="playground1"></sofia-playground>
<sofia-playground id="playground2"></sofia-playground>

<script>
  const p1 = document.getElementById('playground1');
  const p2 = document.getElementById('playground2');
  
  // Each instance maintains its own state
  p1.apiKey = 'key1';
  p2.apiKey = 'key2';
</script>
```

## Contributing

1. Fork the repository
2. Make changes to `sofia-playground.js`
3. Test in multiple browsers
4. Ensure Web Component standards compliance
5. Submit pull request

## Resources

- [Web Components MDN](https://developer.mozilla.org/en-US/docs/Web/Web_Components)
- [Custom Elements Spec](https://html.spec.whatwg.org/multipage/custom-elements.html)
- [Shadow DOM Spec](https://dom.spec.whatwg.org/#shadow-trees)
- [OpenAPI Schema](../../openapi/sofia-core.json)
- [Deployment Guide](../../docs/deployment.md)

## Related Playgrounds

- [React Playground](../react/Playground.tsx)
- [Vue Playground](../vue/SofiaPlayground.vue)

## License

MIT License - See LICENSE file in repository root
