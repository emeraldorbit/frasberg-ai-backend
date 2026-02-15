# Sofia Core API Reference

**Version:** 1.0.0  
**Last Updated:** 2024  
**API Base URL:** `https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend`

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
5. [Request & Response Schemas](#request--response-schemas)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Sofia-Specific Extensions](#sofia-specific-extensions)
9. [OpenAI Compatibility](#openai-compatibility)
10. [Examples](#examples)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Overview

The Sofia Core API is a powerful, post-structural conversational intelligence platform that extends OpenAI's Chat Completions API with advanced identity management, behavioral directives, and context persistence capabilities. Sofia provides unified field runtime integration for coherent multi-modal interactions.

### Key Features

- **OpenAI Compatible**: Drop-in replacement for OpenAI's Chat Completions API
- **Advanced Identity Management**: Multi-persona, sovereign, and unified identity modes
- **Behavioral Governance**: Fine-grained control over tone, directives, and field alignment
- **Context Persistence**: Continuum-based context threading across sessions
- **Post-Structural Runtime**: Coherent identity management through unified field integration
- **Comprehensive Governance**: 44 triads/modules for behavioral modulation

### Use Cases

- Multi-modal conversational applications
- Sovereign identity governance systems
- Context-aware assistant platforms
- Ritual-aligned interaction patterns
- Enterprise conversational intelligence

---

## Getting Started

### Quick Start

```bash
# 1. Get your API credentials
# Create an account and generate an API key from the dashboard

# 2. Make your first request
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "user", "content": "Hello, Sofia!"}
    ]
  }'
```

### Installation

Sofia provides official SDKs in multiple languages:

**TypeScript/JavaScript:**
```bash
npm install @sofia/sdk
```

**Python:**
```bash
pip install sofia-sdk
```

**cURL:**
```bash
# Built-in to most systems
```

---

## Authentication

Sofia Core uses **Bearer Token authentication** via HTTP headers. All API requests must include a valid authentication token.

### Authentication Methods

#### 1. Bearer Token (Recommended)

Include your API key in the `Authorization` header:

```bash
Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx
```

**Example:**
```bash
curl -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx" \
  https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions
```

#### 2. Supabase JWT Token

If using Supabase Auth directly:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Getting Your API Key

1. Log in to the Sofia Dashboard
2. Navigate to **Settings** → **API Keys**
3. Click **Create New Key**
4. Copy your key and store it securely
5. Use it in the `Authorization` header for all requests

### API Key Best Practices

✅ **DO:**
- Store keys in environment variables
- Use different keys for development and production
- Rotate keys regularly
- Restrict key usage to specific IP addresses

❌ **DON'T:**
- Commit API keys to version control
- Share API keys with unauthorized users
- Use the same key across multiple applications
- Expose keys in client-side code

### Authentication Errors

| Status | Error | Description |
|--------|-------|-------------|
| 401 | `Missing Authorization header` | Authorization header is required |
| 401 | `Invalid token format` | Token must be "Bearer {token}" |
| 401 | `Invalid or expired token` | Token is invalid, expired, or revoked |
| 401 | `User not found` | Token is valid but user doesn't exist |

---

## API Endpoints

### Health Check

**Endpoint:** `GET /`

Returns API status and available endpoints.

**Request:**
```bash
curl https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/
```

**Response (200):**
```json
{
  "message": "Sofia Core Backend is running",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "endpoints": {
    "health": "GET /",
    "chat_completions": "POST /v1/chat/completions",
    "models": "GET /v1/models"
  },
  "status": "operational"
}
```

---

### Chat Completions

**Endpoint:** `POST /v1/chat/completions`

Creates a message using the Sofia Core model with optional streaming support.

**Authentication:** Required (Bearer Token)

#### Request

```http
POST /v1/chat/completions HTTP/1.1
Host: sdtilgpppwhwtbxlbmik.supabase.co
Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx
Content-Type: application/json

{
  "model": "sofia-core",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
  ],
  "temperature": 0.7,
  "max_tokens": 150,
  "stream": false
}
```

#### Response

**Status:** 200 OK

```json
{
  "id": "chatcmpl-8P4K7xR2mN9Q1L3V",
  "object": "chat.completion",
  "created": 1705316400,
  "model": "sofia-core",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris, known for its iconic landmarks such as the Eiffel Tower, Notre-Dame Cathedral, and the Louvre Museum."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 28,
    "completion_tokens": 33,
    "total_tokens": 61
  }
}
```

#### Streaming Response

When `stream: true`, responses are sent as Server-Sent Events (SSE):

```
data: {"id":"chatcmpl-8P4K7xR2mN9Q1L3V","object":"chat.completion.chunk","created":1705316400,"model":"sofia-core","choices":[{"index":0,"delta":{"role":"assistant","content":"The"},"finish_reason":null}]}

data: {"id":"chatcmpl-8P4K7xR2mN9Q1L3V","object":"chat.completion.chunk","created":1705316400,"model":"sofia-core","choices":[{"index":0,"delta":{"content":" capital"},"finish_reason":null}]}

...

data: [DONE]
```

---

## Request & Response Schemas

### ChatCompletionRequest

Complete schema for chat completion requests.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | string | Yes | — | Model to use. Must be `"sofia-core"` |
| `messages` | Message[] | Yes | — | List of messages in the conversation |
| `temperature` | number | No | 0.7 | Sampling temperature (0.0-2.0) |
| `max_tokens` | number | No | unlimited | Maximum tokens in response |
| `top_p` | number | No | 1.0 | Nucleus sampling parameter (0.0-1.0) |
| `top_k` | number | No | 50 | Top-K sampling parameter |
| `stream` | boolean | No | false | Enable streaming responses |
| `presence_penalty` | number | No | 0.0 | Penalty for token presence (-2.0 to 2.0) |
| `frequency_penalty` | number | No | 0.0 | Penalty for token frequency (-2.0 to 2.0) |
| `logit_bias` | object | No | {} | Adjust token probability |
| `sofia_identity` | SofiaIdentity | No | — | Identity configuration (Sofia extension) |
| `sofia_directives` | SofiaDirectives | No | — | Behavioral directives (Sofia extension) |
| `continuum` | string | No | — | Context persistence identifier |

#### Message Object

```typescript
{
  role: "system" | "user" | "assistant",
  content: string,
  name?: string              // Optional: Author name
}
```

**Role Descriptions:**

- **system**: Instructions for the assistant's behavior
- **user**: User input and questions
- **assistant**: Previous assistant responses (for context)

**Example:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are an expert physicist with 20 years of experience."
    },
    {
      "role": "user",
      "content": "Explain quantum entanglement"
    },
    {
      "role": "assistant",
      "content": "Quantum entanglement is a phenomenon where..."
    }
  ]
}
```

### ChatCompletionResponse

Response object for non-streaming chat completions.

```typescript
{
  id: string;              // Unique completion ID
  object: "chat.completion";
  created: number;         // Unix timestamp
  model: string;           // Model used ("sofia-core")
  choices: Choice[];
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
  system_fingerprint?: string;  // For debugging/reproducibility
}
```

#### Choice Object

```typescript
{
  index: number;           // Choice index
  message: {
    role: string;          // "assistant"
    content: string;       // Generated text
  };
  finish_reason: "stop" | "length" | "content_filter" | "function_call";
  logprobs?: {             // Optional token probabilities
    content: Array<{
      token: string;
      logprob: number;
      top_logprobs: Array<{ token: string; logprob: number }>;
    }>;
  };
}
```

#### Finish Reasons

| Reason | Meaning |
|--------|---------|
| `stop` | Natural end of response |
| `length` | Max tokens reached |
| `content_filter` | Content policy violation |
| `function_call` | Function was called (if supported) |

### Streaming Response

**SSE Format:** Each line is a JSON object prefixed with `data: `

```typescript
{
  id: string;
  object: "chat.completion.chunk";
  created: number;
  model: string;
  choices: [{
    index: number;
    delta: {
      role?: string;        // Only in first chunk
      content?: string;     // Token content
    };
    finish_reason: string | null;
  }];
}
```

The stream ends with:
```
data: [DONE]
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": "Descriptive error message",
  "type": "error_type",
  "status_code": 400,
  "details": {
    "field": "value",
    "reason": "specific reason"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/v1/chat/completions",
  "request_id": "req_1705316400_abc123"
}
```

### HTTP Status Codes

| Status | Error | Meaning |
|--------|-------|---------|
| **400** | Bad Request | Invalid request format or parameters |
| **401** | Unauthorized | Missing or invalid authentication |
| **403** | Forbidden | User lacks permission for this resource |
| **404** | Not Found | Endpoint or resource doesn't exist |
| **422** | Validation Error | Invalid parameter values |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Internal Server Error | Server error (not your fault) |
| **503** | Service Unavailable | Service temporarily down |

### Common Errors

#### 1. Authentication Errors

**Missing Authorization Header**
```json
{
  "error": "Missing Authorization header",
  "status_code": 401,
  "details": {
    "header": "Authorization",
    "hint": "Include: Authorization: Bearer YOUR_API_KEY"
  }
}
```

**Invalid Token**
```json
{
  "error": "Invalid or expired token",
  "status_code": 401,
  "details": {
    "reason": "Token signature invalid"
  }
}
```

#### 2. Validation Errors

**Invalid Model**
```json
{
  "error": "Model not supported",
  "status_code": 404,
  "details": {
    "requested_model": "gpt-4",
    "supported_models": ["sofia-core"],
    "hint": "Only 'sofia-core' is currently supported"
  }
}
```

**Invalid Message Format**
```json
{
  "error": "Invalid message format",
  "status_code": 422,
  "details": {
    "field": "messages[0]",
    "expected": "Message object with 'role' and 'content'",
    "received": "string"
  }
}
```

**Invalid Parameter**
```json
{
  "error": "Invalid parameter value",
  "status_code": 422,
  "details": {
    "field": "temperature",
    "constraint": "must be between 0 and 2",
    "received": 2.5
  }
}
```

#### 3. Rate Limit Error

```json
{
  "error": "Rate limit exceeded",
  "status_code": 429,
  "details": {
    "quota": {
      "daily": 50,
      "daily_used": 50,
      "monthly": 500,
      "monthly_used": 487
    },
    "reset_at": "2024-01-16T00:00:00Z"
  }
}
```

#### 4. Server Errors

**Internal Server Error**
```json
{
  "error": "Internal server error",
  "status_code": 500,
  "details": {
    "message": "An unexpected error occurred",
    "request_id": "req_1705316400_abc123"
  },
  "hint": "Contact support with request_id for investigation"
}
```

### Error Handling Best Practices

```typescript
// Example error handling
async function callChatAPI(request: ChatCompletionRequest) {
  try {
    const response = await fetch(
      'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions',
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
      }
    );

    if (!response.ok) {
      const error = await response.json();
      
      switch (response.status) {
        case 401:
          throw new AuthenticationError(error.error);
        case 429:
          throw new RateLimitError(error.details.reset_at);
        case 422:
          throw new ValidationError(error.details);
        default:
          throw new APIError(error);
      }
    }

    return await response.json();
  } catch (error) {
    // Handle error appropriately
    console.error('API call failed:', error);
    throw error;
  }
}
```

---

## Rate Limiting

Sofia implements a quota-based rate limiting system to ensure fair usage and service stability.

### Quota Tiers

| Tier | Daily Limit | Monthly Limit | Cost |
|------|-------------|---------------|------|
| Free | 50 | 500 | $0 |
| Pro | 1,000 | 10,000 | $29/mo |
| Enterprise | Custom | Custom | Contact sales |

### Rate Limit Headers

Every API response includes rate limit information:

```http
X-RateLimit-Limit-Daily: 50
X-RateLimit-Used-Daily: 42
X-RateLimit-Remaining-Daily: 8
X-RateLimit-Reset-Daily: 1705363200
X-RateLimit-Limit-Monthly: 500
X-RateLimit-Used-Monthly: 387
X-RateLimit-Remaining-Monthly: 113
X-RateLimit-Reset-Monthly: 1708041600
```

### Rate Limit Behavior

**When you hit the limit:**
- Status: 429 Too Many Requests
- Wait until the quota resets
- Reset times vary: daily (UTC midnight) and monthly (1st of month)

### Monitoring Usage

```bash
# Check current usage
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/usage

# Sample response
{
  "daily": { "limit": 50, "used": 42, "remaining": 8, "reset_at": "2024-01-16T00:00:00Z" },
  "monthly": { "limit": 500, "used": 387, "remaining": 113, "reset_at": "2024-02-01T00:00:00Z" }
}
```

### Handling Rate Limits

**Best Practice: Exponential Backoff**

```typescript
async function callWithRetry(
  request: ChatCompletionRequest,
  maxRetries = 3
) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await callChatAPI(request);
    } catch (error) {
      if (error.status === 429 && attempt < maxRetries - 1) {
        // Exponential backoff: 1s, 2s, 4s
        const delay = Math.pow(2, attempt) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
}
```

---

## Sofia-Specific Extensions

Sofia extends the OpenAI API with advanced identity management and behavioral governance capabilities.

### Sofia Identity

The `sofia_identity` parameter controls how the assistant presents itself and manages identity.

```typescript
interface SofiaIdentity {
  mode?: "unified" | "multi_persona" | "sovereign" | "continuum";
  tone?: "conversational" | "professional" | "ceremonial";
  vector?: string | "auto";
  field_alignment?: "coherent" | "distributed" | "adaptive";
}
```

#### Identity Modes

**Unified Mode** (Default)
- Single coherent identity across interaction
- Maintains consistent personality and viewpoint
- Best for: General conversations, continuity-critical applications

```json
{
  "sofia_identity": {
    "mode": "unified",
    "tone": "conversational"
  }
}
```

**Multi-Persona Mode**
- Can adopt multiple perspectives within single conversation
- Useful for exploring different viewpoints
- Best for: Analysis, debate, creative exploration

```json
{
  "sofia_identity": {
    "mode": "multi_persona",
    "tone": "professional"
  }
}
```

**Sovereign Mode**
- Independent, self-determined identity
- Emphasizes agency and autonomy
- Best for: Advisory, governance, decision-making contexts

```json
{
  "sofia_identity": {
    "mode": "sovereign",
    "tone": "professional"
  }
}
```

**Continuum Mode**
- Identity persists across sessions
- Maintains memory and context
- Best for: Long-term relationships, ongoing projects

```json
{
  "sofia_identity": {
    "mode": "continuum",
    "vector": "session_id_123"
  }
}
```

#### Tone Options

| Tone | Description | Use Case |
|------|-------------|----------|
| `conversational` | Friendly, accessible, informal | Chat, support, casual interaction |
| `professional` | Formal, precise, business-like | Enterprise, technical, official |
| `ceremonial` | Formal, ritualistic, elevated | Spiritual, formal occasions |

#### Vector Management

```json
{
  "sofia_identity": {
    "mode": "continuum",
    "vector": "custom_vector_id"  // Explicitly set vector
  }
}
```

Or let Sofia auto-assign:

```json
{
  "sofia_identity": {
    "mode": "continuum",
    "vector": "auto"  // Sofia generates unique vector
  }
}
```

### Sofia Directives

Fine-grained behavioral control through directives.

```typescript
interface SofiaDirectives {
  sovereignty?: boolean;           // Enable autonomous decision-making
  ritual_mode?: string;            // Activate ritual/ceremonial patterns
  field_alignment?: string;        // Align with specific field
  token_efficiency?: boolean;      // Optimize for token usage
  response_structure?: "free" | "templated" | "modular";
  [key: string]: any;              // Extensible for custom directives
}
```

#### Common Directives

**Sovereignty Directive**
- Enables autonomous decision-making
- Appropriate responses include judgment calls and recommendations

```json
{
  "sofia_directives": {
    "sovereignty": true
  }
}
```

**Ritual Mode Directive**
- Activates ceremonial/ritual response patterns
- Useful for formal, structured interactions

```json
{
  "sofia_directives": {
    "ritual_mode": "formal",
    "field_alignment": "ceremonial"
  }
}
```

**Token Efficiency Directive**
- Optimizes responses for minimal token usage
- Maintains quality while reducing costs

```json
{
  "sofia_directives": {
    "token_efficiency": true
  }
}
```

**Response Structure Directive**
- Controls how response is organized

```json
{
  "sofia_directives": {
    "response_structure": "modular"  // "free", "templated", or "modular"
  }
}
```

### Continuum

The `continuum` parameter enables context persistence across sessions.

```typescript
{
  "continuum": "user_session_12345"  // Unique session identifier
}
```

**How It Works:**
1. Include a `continuum` ID in your request
2. Sofia maintains context for that session
3. Future requests with same `continuum` reference previous context
4. Enables multi-turn conversations without passing full history

**Example - Multi-Turn Conversation:**

```bash
# Turn 1
curl -X POST .../v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "sofia-core",
    "messages": [{"role": "user", "content": "My name is Alex"}],
    "continuum": "user_123_session_456"
  }'

# Turn 2 - Sofia remembers Alex's name
curl -X POST .../v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "sofia-core",
    "messages": [{"role": "user", "content": "What was my name?"}],
    "continuum": "user_123_session_456"  // Same continuum
  }'

# Response: "Your name is Alex"
```

**Continuum Management:**

```typescript
// Create unique continuum per user session
function generateContinuum(userId: string, sessionId: string): string {
  return `user_${userId}_session_${sessionId}`;
}

// Or use UUID
function generateContinuum(): string {
  return `continuum_${crypto.randomUUID()}`;
}
```

---

## OpenAI Compatibility

Sofia Core is fully compatible with OpenAI's Chat Completions API, making it a drop-in replacement.

### API Compatibility

✅ **Fully Compatible:**
- Same endpoint structure (`/v1/chat/completions`)
- Same request format
- Same response format
- Same parameter set (temperature, max_tokens, etc.)
- Same error codes and messages
- Streaming support via SSE

**Example - Drop-in Replacement:**

```typescript
// Before (OpenAI)
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// After (Sofia - same code!)
const client = new OpenAI({
  apiKey: process.env.SOFIA_API_KEY,
  baseURL: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend'
});

// Works identically
const message = await client.chat.completions.create({
  model: 'sofia-core',
  messages: [
    { role: 'user', content: 'Hello!' }
  ]
});
```

### OpenAI Parameter Support

| Parameter | Support | Notes |
|-----------|---------|-------|
| `model` | ✅ Full | Must be "sofia-core" |
| `messages` | ✅ Full | Same format as OpenAI |
| `temperature` | ✅ Full | 0.0 - 2.0 |
| `max_tokens` | ✅ Full | Limits response length |
| `top_p` | ✅ Full | Nucleus sampling |
| `top_k` | ✅ Partial | Sofia extension |
| `frequency_penalty` | ✅ Full | -2.0 to 2.0 |
| `presence_penalty` | ✅ Full | -2.0 to 2.0 |
| `stream` | ✅ Full | SSE streaming |
| `logit_bias` | ✅ Partial | Limited support |
| `user` | ✅ Partial | For tracking |

### Key Differences

#### Sofia Extensions (Not in OpenAI)

| Feature | OpenAI | Sofia |
|---------|--------|-------|
| `sofia_identity` | ❌ | ✅ Identity management |
| `sofia_directives` | ❌ | ✅ Behavioral control |
| `continuum` | ❌ | ✅ Context persistence |
| Field alignment | ❌ | ✅ Post-structural runtime |

#### Behavioral Differences

| Aspect | OpenAI | Sofia |
|--------|--------|-------|
| Default temperature | 1.0 | 0.7 |
| Identity consistency | Simulated | Native |
| Context memory | Token-based | Continuum-based |
| Governance | Content filters | 44 triads + behavioral engine |

### Using OpenAI SDK with Sofia

**Python:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_SOFIA_API_KEY",
    base_url="https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend"
)

response = client.chat.completions.create(
    model="sofia-core",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)
```

**TypeScript/JavaScript:**
```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'YOUR_SOFIA_API_KEY',
  baseURL: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend'
});

const response = await client.chat.completions.create({
  model: 'sofia-core',
  messages: [
    { role: 'user', content: 'Hello!' }
  ]
});
```

---

## Examples

### Basic Chat Completion

**Request:**
```bash
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "user", "content": "Explain machine learning in simple terms"}
    ],
    "temperature": 0.7,
    "max_tokens": 200
  }'
```

**Response:**
```json
{
  "id": "chatcmpl-8P4K7xR2mN9Q1L3V",
  "object": "chat.completion",
  "created": 1705316400,
  "model": "sofia-core",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Machine learning is a subset of artificial intelligence where computers learn from data without being explicitly programmed. Instead of following pre-written rules, ML algorithms identify patterns in data and improve their performance through experience. For example, email spam filters use ML to learn which emails are spam based on examples."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 68,
    "total_tokens": 83
  }
}
```

### Streaming Response

**Request:**
```bash
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "user", "content": "Write a short poem about technology"}
    ],
    "stream": true,
    "max_tokens": 100
  }'
```

**Response (Streaming):**
```
data: {"id":"chatcmpl-8P4K7xR2mN9Q1L3V","object":"chat.completion.chunk","created":1705316400,"model":"sofia-core","choices":[{"index":0,"delta":{"role":"assistant","content":"In"},"finish_reason":null}]}

data: {"id":"chatcmpl-8P4K7xR2mN9Q1L3V","object":"chat.completion.chunk","created":1705316400,"model":"sofia-core","choices":[{"index":0,"delta":{"content":" circuits"},"finish_reason":null}]}

data: {"id":"chatcmpl-8P4K7xR2mN9Q1L3V","object":"chat.completion.chunk","created":1705316400,"model":"sofia-core","choices":[{"index":0,"delta":{"content":" and"},"finish_reason":null}]}

...

data: [DONE]
```

### Multi-Turn Conversation

**Turn 1:**
```bash
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "system", "content": "You are a helpful Python expert."},
      {"role": "user", "content": "How do I read a file in Python?"}
    ]
  }'
```

**Turn 2 - With Continuum:**
```bash
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "system", "content": "You are a helpful Python expert."},
      {"role": "user", "content": "How do I read a file in Python?"},
      {"role": "assistant", "content": "You can use the open() function..."},
      {"role": "user", "content": "What if the file doesn'\''t exist?"}
    ],
    "continuum": "user_123_py_session"
  }'
```

### Sofia Identity - Multi-Persona Mode

**Request:**
```bash
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "user", "content": "Argue both for and against remote work"}
    ],
    "sofia_identity": {
      "mode": "multi_persona",
      "tone": "professional"
    }
  }'
```

### Sofia Directives - Sovereign Mode

**Request:**
```bash
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "user", "content": "Should we increase our budget for this project?"}
    ],
    "sofia_directives": {
      "sovereignty": true,
      "response_structure": "modular"
    }
  }'
```

### Advanced - Identity + Directives + Continuum

**Request:**
```bash
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "system", "content": "You are a strategic business advisor."},
      {"role": "user", "content": "Help me develop our Q1 strategy"}
    ],
    "temperature": 0.8,
    "max_tokens": 500,
    "sofia_identity": {
      "mode": "sovereign",
      "tone": "professional",
      "field_alignment": "coherent"
    },
    "sofia_directives": {
      "sovereignty": true,
      "token_efficiency": false,
      "response_structure": "modular"
    },
    "continuum": "company_abc_strategy_q1"
  }'
```

### Error Handling Example

**Request with Invalid Parameter:**
```bash
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 3.5
  }'
```

**Error Response:**
```json
{
  "error": "Invalid parameter value",
  "status_code": 422,
  "details": {
    "field": "temperature",
    "constraint": "must be between 0 and 2",
    "received": 3.5,
    "valid_range": [0, 2]
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/v1/chat/completions",
  "request_id": "req_1705316400_abc123"
}
```

---

## Best Practices

### 1. Authentication Security

✅ **DO:**
```typescript
// Store key in environment variable
const apiKey = process.env.SOFIA_API_KEY;

// Use during initialization only
const client = new Sofia({
  apiKey: apiKey
});
```

❌ **DON'T:**
```javascript
// Never hardcode keys
const apiKey = "sk_live_xxxxxxxxxxxxxxxxxx";

// Never expose in client-side code
fetch('/api/endpoint', {
  headers: { 'Authorization': 'Bearer ' + clientSideApiKey }
});
```

### 2. Error Handling

**Implement Proper Error Handling:**
```typescript
async function robustAPICall(request: ChatCompletionRequest) {
  try {
    const response = await callChatAPI(request);
    return response;
  } catch (error) {
    if (error instanceof ValidationError) {
      console.error('Invalid request:', error.details);
      // Re-prompt user for valid input
    } else if (error instanceof RateLimitError) {
      console.error('Rate limited, retry after:', error.resetTime);
      // Implement backoff strategy
    } else if (error instanceof AuthenticationError) {
      console.error('Auth failed, check your API key');
      // Refresh credentials
    } else {
      console.error('Unexpected error:', error);
      // Log and alert
    }
  }
}
```

### 3. Streaming Best Practices

**Handle Streaming Properly:**
```typescript
async function handleStreaming(request: ChatCompletionRequest) {
  const response = await fetch('/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ ...request, stream: true })
  });

  const reader = response.body.getReader();
  let content = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = new TextDecoder().decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') break;

          try {
            const json = JSON.parse(data);
            const token = json.choices[0].delta.content;
            if (token) {
              content += token;
              // Update UI in real-time
              updateUI(content);
            }
          } catch (e) {
            // Ignore parse errors
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }

  return content;
}
```

### 4. Token Management

**Monitor Token Usage:**
```typescript
function analyzeTokenUsage(response: ChatCompletionResponse) {
  const { prompt_tokens, completion_tokens, total_tokens } = response.usage;
  
  console.log(`Prompt: ${prompt_tokens} | Completion: ${completion_tokens} | Total: ${total_tokens}`);
  
  // Estimate cost (adjust rates for your tier)
  const promptCost = prompt_tokens * 0.0005;    // $0.50 per 1M
  const completionCost = completion_tokens * 0.0015; // $1.50 per 1M
  const totalCost = promptCost + completionCost;
  
  console.log(`Estimated cost: $${totalCost.toFixed(6)}`);
}
```

### 5. Message History Management

**Keep History Manageable:**
```typescript
interface ConversationState {
  continuum: string;
  messages: Message[];
  maxHistoryTokens: number;
}

function trimMessageHistory(state: ConversationState, maxTokens = 2000): Message[] {
  // Keep system message always
  const systemMessage = state.messages.filter(m => m.role === 'system');
  const otherMessages = state.messages.filter(m => m.role !== 'system');

  // Trim from oldest
  let tokens = 0;
  const kept: Message[] = [];

  for (let i = otherMessages.length - 1; i >= 0; i--) {
    const estimatedTokens = Math.ceil(otherMessages[i].content.length / 4);
    if (tokens + estimatedTokens > maxTokens) break;
    
    kept.unshift(otherMessages[i]);
    tokens += estimatedTokens;
  }

  return [...systemMessage, ...kept];
}
```

### 6. Performance Optimization

**Batch Requests When Possible:**
```typescript
// Instead of sequential requests
for (const prompt of prompts) {
  await callChatAPI({ messages: [{ role: 'user', content: prompt }] });
}

// Consider using Continuum for related conversations
const continuumId = generateContinuumId();
for (const prompt of prompts) {
  await callChatAPI({
    messages: [{ role: 'user', content: prompt }],
    continuum: continuumId
  });
}
```

### 7. Rate Limit Management

**Respect Rate Limits:**
```typescript
class RateLimitAwareClient {
  private requestQueue: Request[] = [];
  private isProcessing = false;

  async request(req: ChatCompletionRequest): Promise<ChatCompletionResponse> {
    return new Promise((resolve, reject) => {
      this.requestQueue.push({ req, resolve, reject });
      this.processQueue();
    });
  }

  private async processQueue() {
    if (this.isProcessing || this.requestQueue.length === 0) return;
    
    this.isProcessing = true;
    const { req, resolve, reject } = this.requestQueue.shift()!;

    try {
      const response = await callChatAPI(req);
      resolve(response);
    } catch (error) {
      if (error instanceof RateLimitError) {
        // Re-queue request
        this.requestQueue.unshift({ req, resolve, reject });
      } else {
        reject(error);
      }
    } finally {
      // Wait before next request
      await sleep(100);
      this.isProcessing = false;
      this.processQueue();
    }
  }
}
```

### 8. Testing and Validation

**Test Your Integration:**
```typescript
async function validateIntegration(apiKey: string): Promise<boolean> {
  try {
    // Test authentication
    const response = await callChatAPI({
      model: 'sofia-core',
      messages: [{ role: 'user', content: 'test' }],
      max_tokens: 10
    });

    // Verify response structure
    if (!response.id || !response.choices || !response.usage) {
      throw new Error('Invalid response structure');
    }

    // Check authentication
    if (response.status === 401) {
      throw new Error('Authentication failed');
    }

    return true;
  } catch (error) {
    console.error('Integration validation failed:', error);
    return false;
  }
}
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. "Missing Authorization header"

**Problem:** Request fails with 401 error

**Solution:**
```bash
# ✅ Correct - Include Authorization header
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions

# ❌ Wrong - Missing header
curl https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions
```

#### 2. "Invalid token"

**Problem:** 401 error even with API key

**Solution:**
- Verify API key is correct: `echo $SOFIA_API_KEY`
- Check if key has expired (rotate if needed)
- Ensure bearer token format: `Bearer sk_live_xxxxx`

```bash
# Debug authentication
curl -H "Authorization: Bearer $SOFIA_API_KEY" \
  https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/
```

#### 3. "Model not supported"

**Problem:** 404 error with unsupported model

**Solution:**
```json
{
  // ❌ Wrong - Model doesn't exist
  "model": "gpt-4"
  
  // ✅ Correct - Use sofia-core
  "model": "sofia-core"
}
```

#### 4. "Rate limit exceeded"

**Problem:** 429 error when limit is hit

**Solution:**
```typescript
// Check headers for reset time
const resetTime = response.headers.get('X-RateLimit-Reset-Daily');
console.log('Rate limit resets at:', new Date(parseInt(resetTime) * 1000));

// Implement exponential backoff
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429) {
        const delay = Math.pow(2, i) * 1000;
        await new Promise(r => setTimeout(r, delay));
      } else {
        throw error;
      }
    }
  }
}
```

#### 5. "Invalid JSON in request"

**Problem:** 422 error with syntax error message

**Solution:**
```bash
# ❌ Wrong - Invalid JSON
curl -d '{"model": "sofia-core", "messages": [{"role": "user", "content": "Hi"}' ...

# ✅ Correct - Valid JSON
curl -d '{"model": "sofia-core", "messages": [{"role": "user", "content": "Hi"}]}' ...

# Use JSON validator
echo '{"model": "sofia-core"}' | python -m json.tool
```

#### 6. "Timeout waiting for response"

**Problem:** Request takes too long or hangs

**Solution:**
```typescript
// Set reasonable timeout
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 seconds

try {
  const response = await fetch(url, {
    signal: controller.signal,
    // ... other options
  });
} finally {
  clearTimeout(timeoutId);
}

// Use streaming for long responses
const response = await callChatAPI({
  model: 'sofia-core',
  messages: [...],
  stream: true,  // Stream chunks instead of waiting for full response
  max_tokens: 2000
});
```

#### 7. "CORS errors in browser"

**Problem:** Cross-origin request fails

**Solution:**
```typescript
// Make request from backend, not browser
// Option 1: Create backend endpoint
app.post('/api/chat', async (req, res) => {
  const response = await callChatAPI(req.body);
  res.json(response);
});

// Option 2: Use proper CORS headers in frontend
const response = await fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`
  },
  body: JSON.stringify(request)
});
```

#### 8. "Streaming response incomplete"

**Problem:** Stream stops early or connection drops

**Solution:**
```typescript
async function safeStream(request: ChatCompletionRequest) {
  const response = await fetch('/v1/chat/completions', {
    method: 'POST',
    body: JSON.stringify({ ...request, stream: true })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error);
  }

  const reader = response.body.getReader();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += new TextDecoder().decode(value);
      const lines = buffer.split('\n');
      
      // Process complete lines only
      for (let i = 0; i < lines.length - 1; i++) {
        processLine(lines[i]);
      }
      
      // Keep incomplete line in buffer
      buffer = lines[lines.length - 1];
    }

    // Process any remaining buffer
    if (buffer) processLine(buffer);
  } catch (error) {
    console.error('Stream error:', error);
    throw error;
  } finally {
    reader.releaseLock();
  }
}
```

### Debug Mode

**Enable Verbose Logging:**
```typescript
class DebugClient {
  async callAPI(request: ChatCompletionRequest) {
    console.log('[REQUEST]', JSON.stringify(request, null, 2));

    const response = await fetch('/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });

    console.log('[RESPONSE STATUS]', response.status);
    console.log('[RESPONSE HEADERS]', [...response.headers.entries()]);

    const data = await response.json();
    console.log('[RESPONSE BODY]', JSON.stringify(data, null, 2));

    return data;
  }
}
```

### Support Resources

- **Documentation:** https://docs.sofia.ai
- **Status Page:** https://status.sofia.ai
- **Community Discord:** https://discord.gg/sofia
- **Email Support:** support@sofia.ai
- **Issue Tracker:** https://github.com/sofia-ai/issues

---

## API Changelog

### Version 1.0.0 (Current)
- ✅ Initial release
- ✅ /v1/chat/completions endpoint
- ✅ Sofia Identity support
- ✅ Sofia Directives support
- ✅ Continuum context persistence
- ✅ Streaming responses
- ✅ OpenAI compatibility

### Planned Features

- 🔄 Function calling support
- 🔄 Vision/image input support
- 🔄 Fine-tuning API
- 🔄 Embeddings endpoint
- 🔄 Batch processing API

---

## Additional Resources

### Official Documentation
- [Sofia Core API Docs](https://docs.sofia.ai)
- [OpenAI Compatibility Guide](https://docs.sofia.ai/compatibility)
- [Best Practices Guide](https://docs.sofia.ai/best-practices)

### Code Examples
- [TypeScript SDK](https://github.com/sofia-ai/sofia-sdk-ts)
- [Python SDK](https://github.com/sofia-ai/sofia-sdk-py)
- [Example Projects](https://github.com/sofia-ai/examples)

### Community
- [Discord Community](https://discord.gg/sofia)
- [GitHub Discussions](https://github.com/sofia-ai/discussions)
- [Stack Overflow Tag](https://stackoverflow.com/questions/tagged/sofia-api)

---

**Last Updated:** January 15, 2024  
**Status:** Stable / Production Ready  
**Support:** support@sofia.ai
