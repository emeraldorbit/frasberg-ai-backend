# Configuration API Reference

API reference for the Sofia Core SDK configuration system.

## loadSofiaConfig

Loads and validates the Sofia Core SDK configuration.

### Signature

```typescript
function loadSofiaConfig(): SofiaSystemConfig
```

### Returns

`SofiaSystemConfig` - The validated configuration object

### Example

```typescript
import { loadSofiaConfig } from '@sofia/core-sdk';

const config = loadSofiaConfig();
console.log('Configuration loaded:', config);
```

### Behavior

The `loadSofiaConfig` function:
1. Reads configuration from the environment
2. Validates required fields
3. Returns a configuration object

### Usage in Client

This function is called internally by `createSofiaClient()`:

```typescript
// Inside createSofiaClient()
const config = loadSofiaConfig();
```

You typically don't need to call this directly unless you want to validate configuration before creating a client.

---

## SofiaSystemConfig

Type representing the SDK configuration.

### Type Definition

```typescript
interface SofiaSystemConfig {
  // Configuration structure
  // (Specific fields depend on implementation)
}
```

### Fields

The configuration object contains system-level settings for the SDK. Currently, the SDK uses environment variables directly, so this interface serves as a placeholder for future configuration expansions.

---

## Environment Variables

Configuration is loaded from environment variables:

### Required Variables

**`SOFIA_CORE_API_KEY`**

Your Sofia Core API authentication key.

```bash
export SOFIA_CORE_API_KEY="your-api-key-here"
```

**Throws:** Error if not set

### Optional Variables

**`SOFIA_CORE_API_URL`**

Base URL for the Sofia Core API.

```bash
export SOFIA_CORE_API_URL="https://api.sofia-core.yourdomain.com"
```

**Default:** `https://api.sofia-core.yourdomain.com`

---

## Configuration Validation

The SDK validates configuration on initialization:

```typescript
import { createSofiaClient } from '@sofia/core-sdk';

try {
  const client = createSofiaClient();
  console.log('Configuration is valid');
} catch (error) {
  console.error('Configuration error:', error.message);
  // Output: "SOFIA_CORE_API_KEY is missing"
}
```

---

## Configuration Methods

### 1. Environment Variables (Recommended)

```bash
export SOFIA_CORE_API_KEY="your-key"
export SOFIA_CORE_API_URL="https://api.sofia-core.com"
```

### 2. .env File (Local Development)

Create `.env` file:

```env
SOFIA_CORE_API_KEY=your-key
SOFIA_CORE_API_URL=https://api.sofia-core.com
```

Load with dotenv:

```typescript
import 'dotenv/config';
import { createSofiaClient } from '@sofia/core-sdk';

const client = createSofiaClient();
```

### 3. GitHub Secrets (CI/CD)

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    env:
      SOFIA_CORE_API_KEY: ${{ secrets.SOFIA_CORE_API_KEY }}
    steps:
      - uses: actions/checkout@v3
      - run: npm test
```

### 4. Supabase Vault (Production)

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(url, key);

async function getApiKey() {
  const { data } = await supabase.rpc('get_secret', {
    secret_name: 'sofia_core_api_key'
  });
  
  process.env.SOFIA_CORE_API_KEY = data;
}

await getApiKey();
const client = createSofiaClient();
```

---

## Security Best Practices

### ✅ DO

- Load API keys from environment variables
- Use GitHub Secrets for CI/CD
- Use Supabase Vault for production
- Validate configuration at startup
- Keep different keys for dev/prod

### ❌ DON'T

- Hardcode API keys in source code
- Commit `.env` files to git
- Log API keys
- Share API keys in plain text
- Use production keys in development

---

## Configuration Validation Examples

### Startup Validation

```typescript
#!/usr/bin/env node

import { createSofiaClient } from '@sofia/core-sdk';

function validateEnvironment() {
  const required = ['SOFIA_CORE_API_KEY'];
  const missing = required.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    console.error('Missing required environment variables:');
    missing.forEach(key => console.error(`  - ${key}`));
    process.exit(1);
  }
  
  try {
    createSofiaClient();
    console.log('✓ Configuration valid');
  } catch (error) {
    console.error('✗ Configuration error:', error.message);
    process.exit(1);
  }
}

validateEnvironment();
```

### Runtime Validation

```typescript
function ensureConfigured() {
  if (!process.env.SOFIA_CORE_API_KEY) {
    throw new Error(
      'SOFIA_CORE_API_KEY must be set. ' +
      'See: https://docs.sofia-core.com/configuration'
    );
  }
}

ensureConfigured();
const client = createSofiaClient();
```

---

## Configuration for Testing

### Mock Configuration

```typescript
// test-setup.ts
process.env.SOFIA_CORE_API_KEY = 'test-key';
process.env.SOFIA_CORE_API_URL = 'https://test-api.sofia-core.com';
```

### Per-Test Configuration

```typescript
describe('SDK Tests', () => {
  const originalKey = process.env.SOFIA_CORE_API_KEY;
  
  beforeEach(() => {
    process.env.SOFIA_CORE_API_KEY = 'test-key';
  });
  
  afterEach(() => {
    process.env.SOFIA_CORE_API_KEY = originalKey;
  });
  
  it('creates client', () => {
    const client = createSofiaClient();
    expect(client).toBeDefined();
  });
});
```

---

## Troubleshooting

### Missing API Key

**Error:** `SOFIA_CORE_API_KEY is missing`

**Solution:**
```bash
export SOFIA_CORE_API_KEY="your-key"
```

### Invalid Configuration

**Error:** `Configuration validation failed`

**Solution:** Check all required fields are set and valid

### Environment Not Loading

**Solution:** Ensure dotenv is imported before SDK:
```typescript
import 'dotenv/config'; // Must be first
import { createSofiaClient } from '@sofia/core-sdk';
```

---

## Related Documentation

- [Configuration Guide](../getting-started/configuration.md) - Complete setup guide
- [Environment Setup](../getting-started/environment-setup.md) - Development environment
- [Security Policy](../governance/security.md) - Security guidelines
- [Client API](client.md) - Client methods reference
