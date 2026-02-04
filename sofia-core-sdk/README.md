# Sofia Core SDK

> Unified TypeScript client for Sofia Core text, image, and video generation.

[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-UNLICENSED-red.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)

The Sofia Core SDK provides a simple, type-safe interface for interacting with the Sofia Core AI platform. It enforces Sofia Core as the sole provider with no external dependencies or fallback mechanisms.

## Features

- 🔒 **Sofia Core Only** - No external providers or fallbacks
- 🎯 **Type-Safe** - Full TypeScript support with strict typing
- 🚀 **Simple API** - Easy-to-use client interface
- 🔐 **Secure** - Environment-based configuration with API key validation
- 📦 **Zero Dependencies** - Minimal footprint, uses native fetch
- ⚡ **Modern** - ESM and CJS support

## Installation

```bash
npm install @sofia/core-sdk
```

Or with pnpm:

```bash
pnpm add @sofia/core-sdk
```

Or with yarn:

```bash
yarn add @sofia/core-sdk
```

## Quick Start

### 1. Configure Environment

Create a `.env` file in your project root:

```bash
# Sofia Core API Configuration
SOFIA_CORE_API_KEY=your-api-key-here
SOFIA_CORE_API_URL=https://api.sofia-core.yourdomain.com

# Provider Configuration
AI_API_KEY_SOURCE=github-or-supabase
IMAGE_API_KEY_SOURCE=github-or-supabase
VIDEO_API_KEY_SOURCE=github-or-supabase
```

### 2. Create Client

```typescript
import { createSofiaClient } from '@sofia/core-sdk';

const client = createSofiaClient();
```

### 3. Generate Content

```typescript
// Generate text
const text = await client.generateText('What is the meaning of life?');
console.log(text);

// Generate image
const imageBuffer = await client.generateImage('A serene mountain landscape');
// Save or process the image buffer

// Generate video
const videoBuffer = await client.generateVideo('A time-lapse of a sunset');
// Save or process the video buffer
```

## API Reference

### `createSofiaClient()`

Creates a new Sofia Core client instance.

```typescript
function createSofiaClient(): SofiaClient
```

**Returns:** A `SofiaClient` instance with methods for content generation.

**Throws:** 
- `Error` if `SOFIA_CORE_API_KEY` is not set
- `Error` if required configuration variables are missing

**Example:**

```typescript
const client = createSofiaClient();
```

---

### `SofiaClient.generateText(input: string)`

Generate text using Sofia Core AI.

```typescript
async generateText(input: string): Promise<string>
```

**Parameters:**
- `input` (string): The text prompt for generation

**Returns:** Promise resolving to generated text

**Throws:** Error if the API request fails

**Example:**

```typescript
const response = await client.generateText('Explain quantum computing');
console.log(response);
```

---

### `SofiaClient.generateImage(prompt: string)`

Generate an image using Sofia Core.

```typescript
async generateImage(prompt: string): Promise<Buffer>
```

**Parameters:**
- `prompt` (string): The image generation prompt

**Returns:** Promise resolving to image data as Buffer

**Throws:** Error if the API request fails

**Example:**

```typescript
import { writeFile } from 'fs/promises';

const imageBuffer = await client.generateImage('A futuristic cityscape');
await writeFile('output.png', imageBuffer);
```

---

### `SofiaClient.generateVideo(prompt: string)`

Generate a video using Sofia Core.

```typescript
async generateVideo(prompt: string): Promise<Buffer>
```

**Parameters:**
- `prompt` (string): The video generation prompt

**Returns:** Promise resolving to video data as Buffer

**Throws:** Error if the API request fails

**Example:**

```typescript
import { writeFile } from 'fs/promises';

const videoBuffer = await client.generateVideo('Ocean waves at sunset');
await writeFile('output.mp4', videoBuffer);
```

---

### `loadSofiaConfig()`

Load and validate Sofia Core configuration from environment variables.

```typescript
function loadSofiaConfig(): SofiaSystemConfig
```

**Returns:** Validated `SofiaSystemConfig` object

**Throws:** Error if required environment variables are missing

**Example:**

```typescript
import { loadSofiaConfig } from '@sofia/core-sdk';

const config = loadSofiaConfig();
console.log(config.ai.provider); // 'sofia-core'
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SOFIA_CORE_API_KEY` | ✅ | Your Sofia Core API key |
| `SOFIA_CORE_API_URL` | ❌ | API base URL (default: `https://api.sofia-core.yourdomain.com`) |
| `AI_API_KEY_SOURCE` | ✅ | Key source: `github` or `supabase` |
| `IMAGE_API_KEY_SOURCE` | ✅ | Key source: `github` or `supabase` |
| `VIDEO_API_KEY_SOURCE` | ✅ | Key source: `github` or `supabase` |

### Configuration Object

The SDK enforces a strict configuration where Sofia Core is the only provider:

```typescript
interface SofiaSystemConfig {
  ai: {
    provider: 'sofia-core';
    apiKeySource: 'github' | 'supabase';
    allowExternalProviders: false;
    fallbackProviders: [];
  };
  imageGeneration: {
    provider: 'sofia-core';
    apiKeySource: 'github' | 'supabase';
    allowExternalProviders: false;
    fallbackProviders: [];
  };
  videoGeneration: {
    provider: 'sofia-core';
    apiKeySource: 'github' | 'supabase';
    allowExternalProviders: false;
    fallbackProviders: [];
  };
  disabledProviders: Array<
    'openai' | 'anthropic' | 'google-gemini' | 'stability-ai' | 'emergent-llm'
  >;
}
```

## Advanced Usage

### Error Handling

```typescript
try {
  const client = createSofiaClient();
  const text = await client.generateText('Hello, world!');
  console.log(text);
} catch (error) {
  if (error instanceof Error) {
    console.error('Generation failed:', error.message);
  }
}
```

### Custom API URL

```typescript
// Set via environment variable
process.env.SOFIA_CORE_API_URL = 'https://custom-api.example.com';

const client = createSofiaClient();
```

### Working with Buffers

```typescript
import { writeFile } from 'fs/promises';
import { createSofiaClient } from '@sofia/core-sdk';

const client = createSofiaClient();

// Generate and save image
const imageBuffer = await client.generateImage('Abstract art');
await writeFile('./output.png', imageBuffer);

// Generate and save video
const videoBuffer = await client.generateVideo('Animated logo');
await writeFile('./output.mp4', videoBuffer);
```

### Integration with Express

```typescript
import express from 'express';
import { createSofiaClient } from '@sofia/core-sdk';

const app = express();
const client = createSofiaClient();

app.post('/generate-text', express.json(), async (req, res) => {
  try {
    const { input } = req.body;
    const text = await client.generateText(input);
    res.json({ text });
  } catch (error) {
    res.status(500).json({ error: 'Generation failed' });
  }
});

app.listen(3000);
```

## Development

### Prerequisites

- Node.js >= 18.0.0
- npm or pnpm
- TypeScript 5.0+

### Building from Source

```bash
# Clone the repository
git clone https://github.com/emeraldorbit/sofia-core-backend.git
cd sofia-core-backend/sofia-core-sdk

# Install dependencies
npm install

# Build the SDK
npm run build

# Run tests
npm test
```

### Project Structure

```
sofia-core-sdk/
├── src/
│   ├── client/
│   │   └── createSofiaClient.ts    # Client implementation
│   ├── config/
│   │   ├── types.ts                # TypeScript types
│   │   └── loadSofiaConfig.ts      # Configuration loader
│   └── index.ts                    # Public exports
├── dist/                           # Build output
├── package.json
├── tsconfig.json
└── README.md
```

## Security

### Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all configuration
3. **Rotate keys regularly** (every 90 days recommended)
4. **Use GitHub Secrets or Supabase Vault** for key storage
5. **Enable HTTPS** for all communications
6. **Validate inputs** before sending to the API
7. **Monitor usage** for unusual patterns

### Reporting Vulnerabilities

If you discover a security vulnerability, please email security@emeraldestates.com. Do not open public issues for security vulnerabilities.

See [SECURITY.md](SECURITY.md) for more details.

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Reporting bugs
- Suggesting enhancements
- Submitting pull requests
- Code style and standards

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

## License

UNLICENSED - This software is proprietary and confidential.

Copyright (c) Emerald Estates® and Mr. Clayton-M. Bernard-Ex.

See [LICENSE](LICENSE) for full license text.

## Support

- 📧 Email: support@emeraldestates.com
- 📖 Documentation: [docs/SOFIA_PROVIDER_ARCHITECTURE.md](../../docs/SOFIA_PROVIDER_ARCHITECTURE.md)
- 🐛 Issues: [GitHub Issues](https://github.com/emeraldorbit/sofia-core-backend/issues)

## Related Projects

- [Sofia Core Backend](https://github.com/emeraldorbit/sofia-core-backend)
- Sofia Governance Engine
- Sofia Continuum Identity
- Sofia Membrane Protocol

---

Made with ⚡ by Emerald Estates®
