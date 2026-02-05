# SDK Surface

The public API surface of the Sofia Core SDK.

## Design Philosophy

The SDK surface is intentionally minimal:

1. **Small API** - Few functions, clear purpose
2. **No Surprises** - Predictable behavior
3. **Type Safe** - Full TypeScript support
4. **Stable** - Minimal breaking changes

## Public Exports

Located in `src/index.ts`:

```typescript
// Functions
export { createSofiaClient } from './client/createSofiaClient';
export { loadSofiaConfig } from './config/loadSofiaConfig';

// Types
export type { SofiaClient } from './client/createSofiaClient';
export type { SofiaSystemConfig } from './config/types';
```

## API Functions

### createSofiaClient()

Creates a Sofia Core SDK client instance.

**Signature:**
```typescript
function createSofiaClient(): SofiaClient
```

**Returns:** `SofiaClient` instance

**Throws:** `Error` if configuration is invalid

**Example:**
```typescript
import { createSofiaClient } from '@sofia/core-sdk';

const client = createSofiaClient();
```

### loadSofiaConfig()

Loads SDK configuration from environment.

**Signature:**
```typescript
function loadSofiaConfig(): SofiaSystemConfig
```

**Returns:** `SofiaSystemConfig` object

**Example:**
```typescript
import { loadSofiaConfig } from '@sofia/core-sdk';

const config = loadSofiaConfig();
```

## API Types

### SofiaClient

Interface for the SDK client.

```typescript
interface SofiaClient {
  generateText(input: string): Promise<string>;
  generateImage(prompt: string): Promise<Buffer>;
  generateVideo(prompt: string): Promise<Buffer>;
}
```

**Methods:**

- **generateText** - Generate text from prompt
- **generateImage** - Generate image from prompt
- **generateVideo** - Generate video from prompt

### SofiaSystemConfig

Configuration type for the SDK.

```typescript
interface SofiaSystemConfig {
  // Internal configuration structure
}
```

## API Stability

### Semantic Versioning

The SDK follows [SemVer 2.0.0](https://semver.org/):

- **Patch** (x.y.Z) - Bug fixes, no API changes
- **Minor** (x.Y.z) - New features, backward compatible
- **Major** (X.y.z) - Breaking changes

### Stability Guarantee

Current API (v1.x.x) guarantees:

1. Function signatures won't change
2. Return types won't change
3. Error behavior stays consistent
4. TypeScript types remain compatible

## API Surface Guidelines

### What's Included

- Core client creation
- Generation methods
- Configuration loading
- Essential types

### What's Excluded

- Internal utilities (not exported)
- Provider implementations (internal)
- HTTP client (internal)
- Request/response parsing (internal)

## Internal vs Public

### Public (Exported)

```typescript
// ✅ Public API
export { createSofiaClient } from './client/createSofiaClient';
export type { SofiaClient } from './client/createSofiaClient';
```

### Internal (Not Exported)

```typescript
// ❌ Internal implementation
function validateApiKey(key: string): boolean {
  // Internal validation logic
}

function buildRequestHeaders(apiKey: string): Record<string, string> {
  // Internal header construction
}
```

## Usage Patterns

### Basic Usage

```typescript
import { createSofiaClient } from '@sofia/core-sdk';

const client = createSofiaClient();
const result = await client.generateText('Hello');
```

### With Type Annotations

```typescript
import { createSofiaClient, SofiaClient } from '@sofia/core-sdk';

const client: SofiaClient = createSofiaClient();
const text: string = await client.generateText('Hello');
```

### Configuration Check

```typescript
import { loadSofiaConfig } from '@sofia/core-sdk';

try {
  const config = loadSofiaConfig();
  console.log('Configuration valid');
} catch (error) {
  console.error('Configuration error:', error.message);
}
```

## Extension Patterns

The API surface supports extension without modification:

### Wrapper Pattern

```typescript
import { createSofiaClient, SofiaClient } from '@sofia/core-sdk';

interface ExtendedClient extends SofiaClient {
  generateTextCached(input: string): Promise<string>;
}

function createExtendedClient(): ExtendedClient {
  const client = createSofiaClient();
  const cache = new Map<string, string>();
  
  return {
    ...client,
    async generateTextCached(input: string) {
      if (cache.has(input)) return cache.get(input)!;
      const result = await client.generateText(input);
      cache.set(input, result);
      return result;
    }
  };
}
```

### Decorator Pattern

```typescript
function withRetry<T extends SofiaClient>(client: T): T {
  return new Proxy(client, {
    get(target, prop) {
      const original = target[prop];
      if (typeof original !== 'function') return original;
      
      return async function(...args: any[]) {
        for (let i = 0; i < 3; i++) {
          try {
            return await original.apply(target, args);
          } catch (error) {
            if (i === 2) throw error;
          }
        }
      };
    }
  });
}

const client = withRetry(createSofiaClient());
```

## API Evolution

### Adding Features (Minor Version)

New optional methods can be added:

```typescript
// v1.0.0
interface SofiaClient {
  generateText(input: string): Promise<string>;
  generateImage(prompt: string): Promise<Buffer>;
  generateVideo(prompt: string): Promise<Buffer>;
}

// v1.1.0 - New optional feature
interface SofiaClient {
  generateText(input: string): Promise<string>;
  generateImage(prompt: string): Promise<Buffer>;
  generateVideo(prompt: string): Promise<Buffer>;
  generateTextStream?(input: string): AsyncIterator<string>; // New
}
```

### Breaking Changes (Major Version)

Signature changes require major version bump:

```typescript
// v1.x.x
generateText(input: string): Promise<string>;

// v2.0.0 - Breaking change
generateText(options: TextOptions): Promise<TextResult>;
```

## Documentation

Each exported function/type is documented:

```typescript
/**
 * Creates a Sofia Core SDK client instance.
 * 
 * @returns A configured SofiaClient instance
 * @throws {Error} If SOFIA_CORE_API_KEY is not set
 * 
 * @example
 * ```typescript
 * const client = createSofiaClient();
 * const result = await client.generateText('Hello');
 * ```
 */
export function createSofiaClient(): SofiaClient {
  // Implementation
}
```

## Testing Surface

All public API is tested:

```typescript
describe('Public API', () => {
  it('exports createSofiaClient', () => {
    expect(typeof createSofiaClient).toBe('function');
  });
  
  it('exports loadSofiaConfig', () => {
    expect(typeof loadSofiaConfig).toBe('function');
  });
  
  it('exports SofiaClient type', () => {
    const client: SofiaClient = createSofiaClient();
    expect(client).toHaveProperty('generateText');
    expect(client).toHaveProperty('generateImage');
    expect(client).toHaveProperty('generateVideo');
  });
});
```

## Related Documentation

- [Client API](../api/client.md) - Detailed API reference
- [Types Reference](../api/types.md) - TypeScript types
- [Architecture Overview](overview.md) - System design
- [Versioning Policy](../governance/versioning.md) - Version strategy
