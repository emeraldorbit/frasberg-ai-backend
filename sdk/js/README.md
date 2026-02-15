# Sofia Core JavaScript SDK

Official JavaScript SDK for Sofia Core - Works in both Node.js and browser environments.

## Installation

```bash
npm install @emerald-estates/sofia-client
```

Or use directly in browser via CDN:

```html
<script type="module">
  import { SofiaClient } from 'https://cdn.jsdelivr.net/npm/@emerald-estates/sofia-client/sofia-client.js';
</script>
```

## Quick Start

### Node.js

```javascript
import { SofiaClient } from '@emerald-estates/sofia-client';

const sofia = new SofiaClient({
  baseUrl: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
  apiKey: process.env.SOFIA_API_KEY
});

const result = await sofia.chat([
  { role: "user", content: "Hello Sofia" }
]);

console.log(result.choices[0].message.content);
```

### Browser

```html
<!DOCTYPE html>
<html>
<head>
  <title>Sofia Core Example</title>
</head>
<body>
  <h1>Sofia Core Chat</h1>
  <button id="chat">Send Message</button>
  <div id="response"></div>

  <script type="module">
    import { SofiaClient } from './sofia-client.js';

    const sofia = new SofiaClient({
      baseUrl: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
      apiKey: 'your-api-key'
    });

    document.getElementById('chat').addEventListener('click', async () => {
      const result = await sofia.chat([
        { role: "user", content: "Hello Sofia" }
      ]);
      
      document.getElementById('response').textContent = 
        result.choices[0].message.content;
    });
  </script>
</body>
</html>
```

## Features

- ✅ **Universal** - Works in Node.js and browsers
- ✅ **OpenAI-compatible** - Drop-in replacement for OpenAI client
- ✅ **Streaming support** - Real-time responses
- ✅ **Sovereign extensions** - Sofia-specific features
- ✅ **Zero dependencies** - Pure JavaScript

## Usage

### Standard Chat

```javascript
const response = await sofia.chat([
  { role: "system", content: "You are Sofia, a sovereign AI." },
  { role: "user", content: "Explain quantum computing" }
], {
  temperature: 0.7,
  max_tokens: 1000
});

console.log(response.choices[0].message.content);
```

### Streaming Chat

```javascript
for await (const chunk of sofia.chatStream([
  { role: "user", content: "Tell me a story" }
])) {
  process.stdout.write(chunk);
}
```

### Browser Streaming

```javascript
const stream = sofia.chatStream([
  { role: "user", content: "Count to 10" }
]);

for await (const chunk of stream) {
  document.getElementById('output').textContent += chunk;
}
```

### Sovereign Mode

```javascript
const response = await sofia.sovereign(
  [{ role: "user", content: "What is your purpose?" }],
  {
    mode: "sovereign",
    tone: "ceremonial",
    vector: "auto"
  },
  {
    sovereignty: true,
    ritual_mode: "invocation"
  }
);
```

## API Reference

### `new SofiaClient(config)`

Create a new Sofia client instance.

**Config:**
- `baseUrl`: API endpoint URL (required)
- `apiKey`: Your Sofia API key (required)
- `timeout`: Request timeout in ms (default: 60000)

### `chat(messages, options)`

Send messages and get a completion.

**Parameters:**
- `messages`: Array of `{ role, content }` objects
- `options`: Optional configuration
  - `temperature`: Number (0-2)
  - `max_tokens`: Number
  - `sofia_identity`: Identity configuration
  - `continuum`: String
  - `sofia_directives`: Directive configuration

**Returns:** Promise<SofiaResponse>

### `chatStream(messages, options)`

Stream chat completion chunks.

**Returns:** AsyncGenerator<string>

### `sovereign(messages, identity, directives)`

Chat with sovereign mode enabled.

## License

MIT
