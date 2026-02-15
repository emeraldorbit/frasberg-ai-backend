# Sofia Core - Browser Example

This example demonstrates using Sofia Core directly in the browser.

## Setup

1. Open `index.html` in a web browser
2. Enter your API key
3. Type a message and click "Send Message" or "Stream Message"

## Features

- ✅ Pure browser-based implementation (no build step)
- ✅ OpenAI-compatible chat
- ✅ Streaming support
- ✅ Sovereign mode toggle
- ✅ Beautiful responsive UI

## Usage

### Local Testing

```bash
# Start a simple HTTP server
python -m http.server 8000
# Or with Node.js
npx http-server

# Open http://localhost:8000 in your browser
```

### Deploy

You can deploy this example to:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

## Security Note

Never commit your API key! Always enter it at runtime or use environment-specific configuration.
