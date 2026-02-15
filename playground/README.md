# Sofia Core API Playgrounds

Interactive playgrounds for testing and exploring the Sofia Core API. Choose from React, Vue, or Web Component implementations based on your preferred framework.

## Available Playgrounds

### 🔷 React Playground
**Location**: `react/Playground.tsx`

A fully-featured React playground with TypeScript support.

- ✅ TypeScript support
- ✅ React 18+ with hooks
- ✅ Modern React patterns
- ✅ Full type safety

[📖 React Playground Documentation](./react/README.md)

### 🟢 Vue Playground
**Location**: `vue/SofiaPlayground.vue`

Modern Vue 3 implementation using Composition API.

- ✅ Vue 3 Composition API
- ✅ TypeScript support
- ✅ Reactive state management
- ✅ Scoped styles

[📖 Vue Playground Documentation](./vue/README.md)

### 🔶 Web Component
**Location**: `web-component/sofia-playground.js`

Framework-agnostic custom element that works everywhere.

- ✅ Zero dependencies
- ✅ Works with any framework
- ✅ Shadow DOM encapsulation
- ✅ Native browser support

[📖 Web Component Documentation](./web-component/README.md)

## Quick Start

### React

```bash
# Install React dependencies
npm install react react-dom @types/react @types/react-dom

# Use the playground
import Playground from './playground/react/Playground';
```

### Vue

```bash
# Install Vue
npm install vue

# Use the playground
import SofiaPlayground from './playground/vue/SofiaPlayground.vue';
```

### Web Component

```html
<!-- No installation required! -->
<sofia-playground></sofia-playground>
<script src="./playground/web-component/sofia-playground.js"></script>
```

## Common Features

All playgrounds include:

- ✅ **Full Conversation History** - See all messages in order
- ✅ **Real-time Updates** - Messages appear instantly
- ✅ **Loading States** - Visual feedback during API calls
- ✅ **Error Handling** - Clear error messages
- ✅ **Keyboard Shortcuts** - Enter to send, Shift+Enter for new line
- ✅ **Responsive Design** - Works on desktop and mobile
- ✅ **Professional Styling** - Beautiful gradient themes
- ✅ **API Key Management** - Secure authentication

## Choosing a Playground

### Use React When:
- You have an existing React application
- You prefer TypeScript and type safety
- You want the latest React features
- You're building a complex UI

### Use Vue When:
- You have an existing Vue 3 application
- You prefer Composition API
- You want reactive state management
- You're familiar with Vue ecosystem

### Use Web Component When:
- You want framework-agnostic solution
- You need to embed in any app
- You want zero dependencies
- You're using vanilla JavaScript
- You need to support multiple frameworks

## Configuration

All playgrounds connect to the same Sofia Core API:

```
https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend
```

### Required: API Key

Each playground requires an API key for authentication. Enter it in the header input field.

### API Endpoints

The playgrounds use the following endpoints:

- `POST /v1/chat/completions` - Send chat messages

### Request Format

```json
{
  "model": "sofia-core",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "stream": false,
  "sofia_identity": {
    "mode": "unified",
    "tone": "conversational"
  }
}
```

### Response Format

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## Sofia Identity Extensions

All playgrounds support Sofia's sovereign extensions:

### Identity Modes
- `unified` - Single consistent identity
- `multi_persona` - Multiple personas
- `sovereign` - Autonomous identity
- `continuum` - Identity across contexts

### Tone Options
- `conversational` - Friendly and casual
- `professional` - Business-appropriate
- `ceremonial` - Formal and dignified

### Example Request

```json
{
  "model": "sofia-core",
  "messages": [
    {"role": "user", "content": "Tell me about yourself"}
  ],
  "sofia_identity": {
    "mode": "unified",
    "tone": "professional",
    "vector": "identity-vector-123"
  },
  "continuum": "session-abc-123",
  "sofia_directives": {
    "preserve_identity": true,
    "governance_level": "strict"
  }
}
```

## Development

### Testing Locally

Each playground can be tested independently:

**React:**
```bash
cd playground/react
npm install
npm run dev
```

**Vue:**
```bash
cd playground/vue
npm install
npm run dev
```

**Web Component:**
```bash
cd playground/web-component
# Open index.html in browser
python -m http.server 8000
```

### Integration Testing

Test the API integration:

```bash
# Test chat completions
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [{"role": "user", "content": "Test"}]
  }'
```

## Browser Support

All playgrounds support modern browsers:

| Browser | React | Vue | Web Component |
|---------|-------|-----|---------------|
| Chrome 90+ | ✅ | ✅ | ✅ |
| Firefox 88+ | ✅ | ✅ | ✅ |
| Safari 14+ | ✅ | ✅ | ✅ |
| Edge 90+ | ✅ | ✅ | ✅ |

## Keyboard Shortcuts

All playgrounds support:

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift + Enter` | New line |
| `Ctrl + L` | Clear (planned) |

## Styling

Each playground includes:

- **Modern Design** - Clean, professional interface
- **Gradient Theme** - Purple-blue gradient background
- **Responsive Layout** - Adapts to screen size
- **Smooth Animations** - Loading indicators and transitions
- **High Contrast** - Readable text and clear UI elements

### Color Scheme

```css
Primary Gradient: #667eea → #764ba2
User Messages: Purple gradient
Assistant Messages: Light gray (#f5f5f5)
Error Messages: Red (#c33)
Loading Dots: Purple (#667eea)
```

## Architecture

### Component Structure

```
Playground
├── Header (Title, API Key Input)
├── Messages Container
│   ├── Empty State
│   ├── Message List
│   │   ├── User Messages
│   │   └── Assistant Messages
│   └── Loading Indicator
└── Input Container
    ├── Error Message
    ├── Text Area
    ├── Send Button
    ├── Clear Button
    └── Keyboard Hints
```

### State Management

Each playground manages:

- `messages: Message[]` - Conversation history
- `input: string` - Current user input
- `loading: boolean` - API call in progress
- `error: string | null` - Error message
- `apiKey: string` - Authentication key

### API Integration

All playgrounds use the Fetch API:

```javascript
const response = await fetch(`${apiUrl}/v1/chat/completions`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`,
  },
  body: JSON.stringify({
    model: 'sofia-core',
    messages: messages,
    stream: false,
  }),
});
```

## Error Handling

Common errors and solutions:

### Missing API Key
```
Error: "Please enter your API key"
Solution: Enter valid API key in header input
```

### Authentication Failed
```
Error: "API Error: 401 Unauthorized"
Solution: Verify API key is correct and active
```

### Network Error
```
Error: "Failed to send message"
Solution: Check internet connection and API endpoint
```

### CORS Error
```
Error: "CORS policy blocked"
Solution: Ensure API supports CORS or use proxy
```

## Security

All playgrounds implement security best practices:

- ✅ API keys stored in memory only
- ✅ No localStorage persistence
- ✅ HTTPS-only API calls
- ✅ Input sanitization
- ✅ No sensitive data logging
- ✅ Content Security Policy compatible

## Performance

Optimization features:

- **Lazy Rendering** - Only render visible messages
- **Debounced Input** - Reduce re-renders
- **Auto-scroll** - Smooth scrolling to latest message
- **Efficient Updates** - Minimal DOM manipulation

## Accessibility

All playgrounds include:

- Semantic HTML elements
- Keyboard navigation support
- High contrast colors
- Focus indicators
- Screen reader friendly (enhancement in progress)
- ARIA labels (enhancement in progress)

## Troubleshooting

### Playground Not Loading

1. Check browser console for errors
2. Verify JavaScript is enabled
3. Ensure all dependencies are installed
4. Try clearing browser cache

### API Calls Failing

1. Verify API key is correct
2. Check network connection
3. Confirm API endpoint is accessible
4. Review browser console for CORS errors

### Styling Issues

1. Check for CSS conflicts
2. Verify Shadow DOM support (Web Component)
3. Clear browser cache
4. Test in incognito mode

## Resources

### Documentation
- [Deployment Guide](../docs/deployment.md)
- [OpenAPI Schema](../openapi/sofia-core.json)
- [React Docs](./react/README.md)
- [Vue Docs](./vue/README.md)
- [Web Component Docs](./web-component/README.md)

### API Reference
- OpenAPI Specification: `../openapi/sofia-core.json`
- API Endpoint: Production URL in deployment docs
- Authentication: Bearer token in Authorization header

### GitHub
- Repository: https://github.com/emeraldorbit/sofia-core-backend
- Issues: https://github.com/emeraldorbit/sofia-core-backend/issues
- Discussions: https://github.com/emeraldorbit/sofia-core-backend/discussions

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Choose a playground to enhance
3. Make your changes
4. Test thoroughly across browsers
5. Submit a pull request

### Enhancement Ideas

- [ ] Add streaming support
- [ ] Implement message editing
- [ ] Add conversation export
- [ ] Support image messages
- [ ] Add dark mode toggle
- [ ] Implement voice input
- [ ] Add message reactions
- [ ] Support file attachments

## License

MIT License - See LICENSE file in repository root

## Support

For help and questions:

- **Issues**: https://github.com/emeraldorbit/sofia-core-backend/issues
- **Discussions**: https://github.com/emeraldorbit/sofia-core-backend/discussions
- **Email**: support@emeraldestates.com (coming soon)

## Version History

- **v1.0.0** (Current) - Initial release with React, Vue, and Web Component playgrounds

---

Made with 💜 by the Sofia Core team
