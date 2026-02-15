# Sofia Core TypeScript SDK

Official TypeScript SDK for Sofia Core - OpenAI-compatible API with sovereign extensions.

## Installation

```bash
npm install @emerald-estates/sofia-core
```

## Quick Start

```typescript
import { SofiaClient } from '@emerald-estates/sofia-core';

const sofia = new SofiaClient({
  baseUrl: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
  apiKey: process.env.SOFIA_API_KEY!
});

// Basic chat
const result = await sofia.chat([
  { role: "user", content: "Hello Sofia" }
]);

console.log(result.choices[0].message.content);
```

## Features

- ✅ **OpenAI-compatible** - Works with OpenAI client code
- ✅ **Streaming support** - Real-time responses
- ✅ **Sovereign extensions** - Sofia-specific features
- ✅ **TypeScript types** - Full type safety
- ✅ **Timeout handling** - Configurable request timeouts

## Usage

### Standard Chat

```typescript
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

```typescript
for await (const chunk of sofia.chatStream([
  { role: "user", content: "Tell me a story" }
])) {
  process.stdout.write(chunk);
}
```

### Sovereign Mode

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

## Configuration

```typescript
const sofia = new SofiaClient({
  baseUrl: 'https://your-endpoint.com',
  apiKey: 'your-api-key',
  timeout: 60000  // 60 seconds (default)
});
```

## API Reference

### SofiaClient

#### `chat(messages, options?): Promise<SofiaResponse>`

Send messages and get a completion.

**Parameters:**
- `messages`: Array of message objects with `role` and `content`
- `options`: Optional configuration
  - `temperature`: Number (0-2)
  - `max_tokens`: Number
  - `sofia_identity`: SofiaIdentity object
  - `continuum`: String
  - `sofia_directives`: SofiaDirectives object

#### `chatStream(messages, options?): AsyncGenerator<string>`

Stream chat completion chunks.

#### `sovereign(messages, identity, directives?): Promise<SofiaResponse>`

Chat with sovereign mode enabled.

## Types

```typescript
interface SofiaMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

interface SofiaIdentity {
  mode?: "unified" | "multi_persona" | "sovereign" | "continuum";
  tone?: "conversational" | "professional" | "ceremonial";
  vector?: string | "auto";
}

interface SofiaDirectives {
  sovereignty?: boolean;
  ritual_mode?: string;
  field_alignment?: string;
  [key: string]: any;
}
```

## License

MIT
