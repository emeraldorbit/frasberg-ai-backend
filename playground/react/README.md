# Sofia Core React Playground

A fully-featured React playground for testing the Sofia Core API with TypeScript support.

## Features

✅ Full conversation history  
✅ Real-time message display  
✅ Loading states with animated indicators  
✅ Error handling with user-friendly messages  
✅ Keyboard shortcuts (Enter to send, Shift+Enter for new line)  
✅ Responsive design for mobile and desktop  
✅ Professional styling with gradient themes  
✅ TypeScript support for type safety  

## Installation

### Prerequisites

- Node.js 18+
- React 18+
- TypeScript 5+

### Setup

```bash
# Install dependencies
npm install react react-dom @types/react @types/react-dom

# Or with yarn
yarn add react react-dom @types/react @types/react-dom
```

## Usage

### Basic Integration

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import Playground from './Playground';

const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(
  <React.StrictMode>
    <Playground />
  </React.StrictMode>
);
```

### With Custom API URL

```tsx
import React, { useState } from 'react';
import Playground from './Playground';

function App() {
  return (
    <div>
      <h1>My Sofia Core App</h1>
      <Playground />
    </div>
  );
}

export default App;
```

### Standalone HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sofia Core Playground</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.tsx"></script>
</body>
</html>
```

## Configuration

### API Key

Users need to enter their API key in the input field at the top of the playground. The key is stored in component state and used for authentication.

### API Endpoint

The default endpoint is:
```
https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend
```

To customize, modify the `apiUrl` state in `Playground.tsx`:

```tsx
const [apiUrl] = useState('YOUR_CUSTOM_ENDPOINT');
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift + Enter` | New line in message |
| `Ctrl + L` | Clear conversation (planned) |

## Components Structure

```tsx
Playground
├── State Management
│   ├── messages: Message[]
│   ├── input: string
│   ├── loading: boolean
│   ├── error: string | null
│   └── apiKey: string
├── UI Components
│   ├── Header (title, subtitle, API key input)
│   ├── Messages Container (conversation history)
│   └── Input Container (textarea, buttons, hints)
└── Functionality
    ├── sendMessage()
    ├── handleKeyDown()
    ├── clearConversation()
    └── scrollToBottom()
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

## Styling

The playground uses inline styles with CSS-in-JS for zero external dependencies. Key styling features:

- **Gradient background**: Purple-blue gradient (#667eea to #764ba2)
- **Card-based layout**: White cards with rounded corners and shadows
- **Responsive design**: Adapts to mobile and desktop screens
- **Smooth animations**: Loading indicators and hover effects
- **Accessible colors**: High contrast for readability

### Customizing Styles

To customize the appearance, modify the `<style>` tag inside the component:

```tsx
<style>{`
  .playground-container {
    background: linear-gradient(135deg, #your-color-1, #your-color-2);
  }
`}</style>
```

## Error Handling

The playground includes comprehensive error handling:

- **Missing API Key**: Prompts user to enter key
- **Network Errors**: Displays connection error messages
- **API Errors**: Shows HTTP status and error details
- **Invalid Responses**: Handles malformed API responses

## Features in Detail

### Loading State

Shows animated dots while waiting for API response:

```tsx
{loading && (
  <div className="loading-indicator">
    <div className="loading-dot"></div>
    <div className="loading-dot"></div>
    <div className="loading-dot"></div>
  </div>
)}
```

### Message Display

Messages are styled based on role:
- **User messages**: Right-aligned, purple gradient background
- **Assistant messages**: Left-aligned, light gray background
- **System messages**: (Future enhancement)

### Auto-scroll

Automatically scrolls to the latest message using React refs:

```tsx
useEffect(() => {
  scrollToBottom();
}, [messages]);
```

## Development

### Run in Development Mode

```bash
# Start development server
npm run dev

# Or with yarn
yarn dev
```

### Build for Production

```bash
# Create optimized build
npm run build

# Preview production build
npm run preview
```

## Testing

### Manual Testing

1. Enter API key in the header input
2. Type a message in the textarea
3. Press Enter or click Send
4. Verify message appears in conversation
5. Check loading indicator displays
6. Verify assistant response appears

### Common Test Cases

- ✅ Send simple message
- ✅ Send message with special characters
- ✅ Test without API key (should show error)
- ✅ Test with invalid API key (should show auth error)
- ✅ Test long messages
- ✅ Test rapid consecutive messages
- ✅ Clear conversation
- ✅ Responsive layout on mobile

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Troubleshooting

### Issue: API Key Not Working

**Solution**: Ensure you're using a valid Bearer token from Sofia Core API.

### Issue: CORS Errors

**Solution**: Verify your API endpoint supports CORS or use a proxy server.

### Issue: Messages Not Displaying

**Solution**: Check browser console for errors. Verify API response format matches expected structure.

### Issue: Styles Not Applying

**Solution**: Ensure the component is properly mounted and styles are injected.

## Performance Optimization

- Uses React.memo for message components (future enhancement)
- Efficient re-rendering with proper state management
- Debounced input handling (future enhancement)
- Virtualized message list for long conversations (future enhancement)

## Accessibility

- Semantic HTML elements
- Keyboard navigation support
- High contrast colors
- Screen reader friendly (future enhancement)
- ARIA labels (future enhancement)

## Security

- API key stored in component state (not localStorage)
- No sensitive data logged to console
- Input sanitization (enhance as needed)
- HTTPS-only API calls

## Contributing

To contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file in repository root

## Support

For issues and questions:
- GitHub Issues: https://github.com/emeraldorbit/sofia-core-backend/issues
- Documentation: See `/docs/deployment.md`
- API Reference: See `/openapi/sofia-core.json`

## Related Playgrounds

- [Vue Playground](../vue/SofiaPlayground.vue)
- [Web Component](../web-component/sofia-playground.js)
