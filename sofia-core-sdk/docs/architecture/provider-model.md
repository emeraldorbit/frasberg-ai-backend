# Provider Model

The Sofia Core SDK implements a strict, sovereign provider architecture.

## Philosophy

The provider model enforces these principles:

1. **Single Provider** - Sofia Core API exclusively
2. **No Fallbacks** - No backup or alternative providers
3. **Explicit Failures** - Failed requests throw errors immediately
4. **No External Calls** - No communication with OpenAI, Anthropic, etc.

## Provider Architecture

```
┌────────────────────────────────┐
│      Application Code          │
└────────────┬───────────────────┘
             │
             ▼
┌────────────────────────────────┐
│       Sofia Core SDK           │
│  ┌──────────────────────────┐  │
│  │    Client Interface      │  │
│  │  - generateText()        │  │
│  │  - generateImage()       │  │
│  │  - generateVideo()       │  │
│  └────────────┬─────────────┘  │
│               │                 │
│  ┌────────────▼─────────────┐  │
│  │   Provider: Sofia Core   │  │
│  │   - Base URL             │  │
│  │   - API Key              │  │
│  │   - HTTP Client          │  │
│  └────────────┬─────────────┘  │
└───────────────┼─────────────────┘
                │
                ▼
        Sofia Core API Only
        (No alternatives)
```

## Why Sovereign Provider?

### Security

- Full control over data flow
- No unexpected external calls
- Audit trail is deterministic
- No data leakage to third parties

### Reliability

- Single point of failure is explicit
- No silent fallback masking issues
- Predictable error behavior
- Clear operational boundaries

### Compliance

- Data never leaves approved infrastructure
- Satisfies regulatory requirements
- Clear data residency
- No third-party processors

## Implementation

### Single Provider Instantiation

```typescript
// src/client/createSofiaClient.ts
export function createSofiaClient(): SofiaClient {
  const apiKey = process.env.SOFIA_CORE_API_KEY;
  const baseUrl = process.env.SOFIA_CORE_API_URL || 
    'https://api.sofia-core.yourdomain.com';
  
  // Only Sofia Core is configured
  // No other providers are initialized
  
  return {
    async generateText(input: string) {
      return await callSofiaCoreAPI('/v1/text', { input });
    },
    async generateImage(prompt: string) {
      return await callSofiaCoreAPI('/v1/image', { prompt });
    },
    async generateVideo(prompt: string) {
      return await callSofiaCoreAPI('/v1/video', { prompt });
    }
  };
}
```

### No Provider Selection

There is no provider selection mechanism:

```typescript
// ❌ NOT IMPLEMENTED - No provider selection
interface ClientOptions {
  provider?: 'sofia' | 'openai' | 'anthropic'; // DOES NOT EXIST
}

// ✅ ACTUAL - Single provider only
function createSofiaClient(): SofiaClient {
  // Always Sofia Core, no alternatives
}
```

### No Fallback Logic

Errors are thrown immediately, never falling back:

```typescript
// ❌ NOT IMPLEMENTED - No fallback
async generateText(input: string) {
  try {
    return await sofiaCoreAPI.generate(input);
  } catch {
    return await openAIAPI.generate(input); // DOES NOT EXIST
  }
}

// ✅ ACTUAL - Explicit failure
async generateText(input: string) {
  try {
    return await sofiaCoreAPI.generate(input);
  } catch (error) {
    throw error; // Propagate immediately
  }
}
```

## Configuration

### Environment Variables

Only Sofia Core variables are recognized:

```bash
# Required
SOFIA_CORE_API_KEY=your-key-here

# Optional
SOFIA_CORE_API_URL=https://api.sofia-core.yourdomain.com
```

### Rejected Variables

These variables are **not** recognized:

```bash
# ❌ These are IGNORED
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
```

## Provider Guarantees

The SDK guarantees:

### 1. Single Endpoint

All requests go to Sofia Core API:
- Text: `{baseUrl}/v1/text`
- Image: `{baseUrl}/v1/image`
- Video: `{baseUrl}/v1/video`

### 2. No External Calls

The SDK will **never** make requests to:
- `api.openai.com`
- `api.anthropic.com`
- `generativelanguage.googleapis.com`
- Any other third-party AI service

### 3. Explicit Failures

When Sofia Core API fails:
- Error is thrown immediately
- No retry to alternative providers
- No silent fallback
- Clear error message

### 4. Auditable

All HTTP requests are predictable:
- Destination: Sofia Core API only
- Headers: Authorization Bearer token
- Body: Documented request format
- No surprise requests

## Validation

### Startup Validation

The SDK validates configuration at startup:

```typescript
import { createSofiaClient } from '@sofia/core-sdk';

try {
  const client = createSofiaClient();
  // Configuration valid, Sofia Core API configured
} catch (error) {
  // Missing API key or invalid configuration
  console.error(error.message);
}
```

### Runtime Validation

Every request validates before sending:

```typescript
async generateText(input: string) {
  // Validate API key exists
  if (!apiKey) {
    throw new Error('SOFIA_CORE_API_KEY is missing');
  }
  
  // Make request to Sofia Core
  const response = await fetch(`${baseUrl}/v1/text`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ input })
  });
  
  // Handle response or throw
  if (!response.ok) {
    throw new Error(`Text generation failed: ${response.status}`);
  }
  
  return (await response.json()).output;
}
```

## Comparison with Multi-Provider SDKs

| Feature | Sofia Core SDK | Multi-Provider SDK |
|---------|---------------|-------------------|
| Providers | 1 (Sofia Core) | Multiple (OpenAI, Anthropic, etc.) |
| Fallback | No | Yes |
| Configuration | Simple | Complex |
| Security | High (controlled) | Lower (many endpoints) |
| Compliance | Easy | Difficult |
| Debugging | Simple | Complex |
| Dependencies | Zero | Many |

## Future Considerations

### If Additional Providers Needed

If Sofia Core needs to support multiple backends:

1. Keep single public API
2. Route internally at Sofia Core API level
3. SDK remains unchanged
4. No client-side provider selection

### Provider Abstraction

Currently not needed, but if required:

```typescript
// Potential future internal structure
interface ProviderBackend {
  generateText(input: string): Promise<string>;
  generateImage(prompt: string): Promise<Buffer>;
  generateVideo(prompt: string): Promise<Buffer>;
}

// But still single provider from SDK perspective
const provider: ProviderBackend = createSofiaCoreProvider();
```

## Related Documentation

- [Architecture Overview](overview.md) - System architecture
- [Provider Abstraction](provider-abstraction.md) - Provider contract
- [Security Policy](../governance/security.md) - Security guidelines
- [Configuration](../getting-started/configuration.md) - Setup guide
