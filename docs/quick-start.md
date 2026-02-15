# Sofia Core - Quick Start Guide

Get started with Sofia Core in less than 5 minutes.

## Prerequisites

- An API key for Sofia Core
- Node.js 14+ (for TypeScript/JavaScript) or Python 3.7+ (for Python)

## Installation

### TypeScript/Node.js

```bash
npm install @emerald-estates/sofia-core
```

### Python

```bash
pip install sofia-sdk
```

### Browser

No installation needed! Use the SDK directly:

```html
<script type="module" src="path/to/sofia-client.js"></script>
```

## Your First Request

### TypeScript

```typescript
import { SofiaClient } from '@emerald-estates/sofia-core';

const sofia = new SofiaClient({
  baseUrl: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
  apiKey: 'your-api-key'
});

const response = await sofia.chat([
  { role: "user", content: "Hello Sofia" }
]);

console.log(response.choices[0].message.content);
```

### Python

```python
from sofia_sdk import SofiaCoreClient

client = SofiaCoreClient(
    base_url="https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend",
    api_key="your-api-key"
)

result = client.chat([
    {"role": "user", "content": "Hello Sofia"}
])

print(result["choices"][0]["message"]["content"])
```

### CLI

```bash
export SOFIA_API_KEY="your-api-key"
npx sofia "Hello Sofia"
```

## Streaming Responses

### TypeScript

```typescript
for await (const chunk of sofia.chatStream([
  { role: "user", content: "Tell me a story" }
])) {
  process.stdout.write(chunk);
}
```

### Python

```python
for chunk in client.chat_stream([
    {"role": "user", "content": "Tell me a story"}
]):
    print(chunk, end='', flush=True)
```

### CLI

```bash
npx sofia --stream "Tell me a story"
```

## Sovereign Mode

Sofia Core supports sovereign extensions for enhanced capabilities:

### TypeScript

```typescript
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

### Python

```python
result = client.sovereign(
    messages=[{"role": "user", "content": "What is your purpose?"}],
    identity={
        "mode": "sovereign",
        "tone": "ceremonial",
        "vector": "auto"
    },
    directives={
        "sovereignty": True,
        "ritual_mode": "invocation"
    }
)
```

### CLI

```bash
npx sofia --sovereign "What is your purpose?"
```

## Configuration Options

### Temperature

Controls randomness (0-2, default: 0.7):

```typescript
await sofia.chat(messages, { temperature: 0.9 });
```

### Max Tokens

Limits response length:

```typescript
await sofia.chat(messages, { max_tokens: 500 });
```

### Continuum

Maintains context across requests:

```typescript
await sofia.chat(messages, { continuum: "project-12345" });
```

## Next Steps

- Explore [Examples](../examples/)
- Read the [API Reference](./api-reference.md)
- Try the [Playground](../playground/)
- Check out [Developer Tools](../tools/)

## Support

- GitHub Issues: https://github.com/emeraldorbit/sofia-core-backend/issues
- Documentation: https://docs.sofia-core.dev

## Security

Never commit your API key! Use environment variables:

```bash
# .env
SOFIA_API_KEY=your-api-key
```

Then load it in your code:

```typescript
import { config } from 'dotenv';
config();

const apiKey = process.env.SOFIA_API_KEY;
```
