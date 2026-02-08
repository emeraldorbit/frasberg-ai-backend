# Sofia Core Provider Architecture

## Executive Summary

The Sofia Core Provider Architecture establishes Sofia Core as the **sole, sovereign AI/LLM provider** for all AI operations across the Emerald Estates ecosystem. This architecture eliminates external dependencies, ensures full control over AI capabilities, and enforces a unified, identity-preserving approach to conversational AI.

## Table of Contents

- [Overview](#overview)
- [Core Principles](#core-principles)
- [Architecture Components](#architecture-components)
- [Configuration System](#configuration-system)
- [SDK Implementation](#sdk-implementation)
- [Security & Governance](#security--governance)
- [Integration Guide](#integration-guide)
- [Enforcement Mechanisms](#enforcement-mechanisms)
- [API Reference](#api-reference)
- [Operational Guidelines](#operational-guidelines)

---

## Overview

### Purpose

The Sofia Core Provider Architecture serves to:

1. **Establish Sovereignty**: Ensure complete control over AI operations
2. **Enforce Identity Preservation**: Maintain Sofia's behavioral governance
3. **Eliminate External Dependencies**: Remove reliance on third-party AI providers
4. **Unify Provider Interface**: Create a consistent API for all AI operations
5. **Enable Governance**: Enforce tonal modulation and membrane protocols

### Scope

This architecture covers:

- **Text Generation**: Natural language processing and conversation
- **Image Generation**: Visual content creation
- **Video Generation**: Motion graphics and video synthesis
- **Configuration Management**: System-wide provider configuration
- **API Key Management**: Secure credential handling via GitHub Secrets and Supabase Vault

---

## Core Principles

### 1. Sofia Core Exclusivity

**Principle**: Sofia Core is the only permitted AI provider.

**Enforcement**:
- Configuration explicitly sets `provider: "sofia-core"` for all operations
- External providers are explicitly disabled
- No fallback mechanisms exist
- Runtime validation ensures compliance

**Rationale**:
- Full control over AI behavior and outputs
- Consistent identity preservation across all operations
- No external dependencies that could introduce variance
- Simplified security model

### 2. Zero Fallback Policy

**Principle**: No fallback providers or external alternatives are allowed.

**Enforcement**:
- `fallbackProviders: []` in all configurations
- `allowExternalProviders: false` flag enforced
- Disabled providers list explicitly blocks alternatives

**Rationale**:
- Prevents accidental external API calls
- Ensures consistent behavior
- Eliminates mixed-provider scenarios
- Simplifies debugging and monitoring

### 3. Centralized Configuration

**Principle**: Single source of truth for provider configuration.

**Enforcement**:
- Configuration loaded from `config/sofia-provider.json`
- Environment variables provide runtime values
- TypeScript types enforce schema compliance
- Configuration validated at startup

**Rationale**:
- Easy to audit and verify provider settings
- Consistent across all environments
- Type-safe configuration prevents errors
- Clear separation of concerns

### 4. Secure Key Management

**Principle**: API keys stored securely, never in code.

**Enforcement**:
- GitHub Secrets for CI/CD and deployed environments
- Supabase Vault for runtime key storage
- Environment variables for local development
- `.env` files excluded from version control

**Rationale**:
- Prevents credential leakage
- Enables key rotation
- Supports different keys per environment
- Maintains audit trail

---

## Architecture Components

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  (Frontend, Backend Services, API Endpoints)                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ imports & uses
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Sofia Core SDK                             │
│  (@sofia/core-sdk)                                           │
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │ createSofiaClient│  │ loadSofiaConfig  │                 │
│  └──────────────────┘  └──────────────────┘                 │
│                                                               │
│  ┌──────────────────────────────────────────┐               │
│  │   SofiaClient                             │               │
│  │   - generateText(input)                   │               │
│  │   - generateImage(prompt)                 │               │
│  │   - generateVideo(prompt)                 │               │
│  └──────────────────────────────────────────┘               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ API calls (HTTPS)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Sofia Core API                             │
│  (https://api.sofia-core.yourdomain.com)                     │
│                                                               │
│  Endpoints:                                                   │
│  - POST /v1/text      (text generation)                      │
│  - POST /v1/image     (image generation)                     │
│  - POST /v1/video     (video generation)                     │
└─────────────────────────────────────────────────────────────┘
```


### Component Overview

#### 1. Configuration Layer

**Location**: `config/sofia-provider.json`

**Purpose**: System-wide provider policy enforcement

**Key Settings**:
```json
{
  "ai": { "provider": "sofia-core", ... },
  "imageGeneration": { "provider": "sofia-core", ... },
  "videoGeneration": { "provider": "sofia-core", ... },
  "disabledProviders": ["openai", "anthropic", ...]
}
```

#### 2. SDK Layer

**Location**: `sofia-core-sdk/`

**Purpose**: Type-safe client library for Sofia Core

**Key Exports**:
- `createSofiaClient()`: Factory for client instances
- `loadSofiaConfig()`: Configuration loader
- `SofiaClient`: Client interface
- `SofiaSystemConfig`: Configuration types

#### 3. Client Layer

**Location**: `sofia-core-sdk/src/client/`

**Purpose**: API interaction and request handling

**Capabilities**:
- Text generation via `/v1/text`
- Image generation via `/v1/image`
- Video generation via `/v1/video`
- Error handling and validation
- Authentication via Bearer token

#### 4. Configuration Management

**Location**: `sofia-core-sdk/src/config/`

**Purpose**: Load and validate configuration

**Features**:
- Environment variable parsing
- Required field validation
- Type enforcement
- Runtime error handling

---

## Configuration System

See `.env.example` and `config/sofia-provider.json` for complete configuration details.

---

## SDK Implementation

The Sofia Core SDK is located in `sofia-core-sdk/` and provides a type-safe TypeScript interface for all Sofia Core operations.

### Installation

```bash
npm install @sofia/core-sdk
```

### Usage

```typescript
import { createSofiaClient } from '@sofia/core-sdk';

const client = createSofiaClient();
const text = await client.generateText('Hello, Sofia!');
```

See `sofia-core-sdk/README.md` for complete SDK documentation.

---

## Security & Governance

### API Key Management

**GitHub Secrets**: Store `SOFIA_CORE_API_KEY` in repository secrets for CI/CD

**Supabase Vault**: Store runtime keys in Supabase Vault for production

**Environment Variables**: Use `.env` files for local development (never commit)

### Security Best Practices

1. Never commit API keys to version control
2. Rotate keys every 90 days
3. Use HTTPS exclusively
4. Implement rate limiting
5. Monitor for unusual usage patterns

See `sofia-core-sdk/SECURITY.md` for comprehensive security guidelines.

---

## Integration Guide

### Quick Start

1. Install SDK: `npm install @sofia/core-sdk`
2. Set environment variables (see `.env.example`)
3. Import and create client: `import { createSofiaClient } from '@sofia/core-sdk'`
4. Use client methods for text, image, and video generation

### Migration from External Providers

The SDK provides a unified interface replacing OpenAI, Anthropic, and other external providers.

**Before (OpenAI)**:
```typescript
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const completion = await openai.chat.completions.create({...});
```

**After (Sofia Core)**:
```typescript
const client = createSofiaClient();
const text = await client.generateText('...');
```

---

## Enforcement Mechanisms

### Compile-Time Enforcement

TypeScript types ensure only Sofia Core can be configured as a provider.

### Runtime Validation

Configuration loader validates all required environment variables at startup.

### CI/CD Enforcement

GitHub Actions workflows validate configuration and run type checks before deployment.

### Code Review

All changes require review by designated code owners (@emeraldorbit).

---

## API Reference

See `sofia-core-sdk/README.md` for complete API documentation.

### Key Methods

- `createSofiaClient()`: Create Sofia Core client
- `generateText(input)`: Generate text
- `generateImage(prompt)`: Generate image
- `generateVideo(prompt)`: Generate video
- `loadSofiaConfig()`: Load configuration

---

## Operational Guidelines

### Development

1. Copy `.env.example` to `.env`
2. Set development API key
3. Install dependencies: `npm install`
4. Build SDK: `npm run build`
5. Run tests: `npm test`

### Deployment

1. Store production API key in GitHub Secrets or Supabase Vault
2. Set `SOFIA_CORE_API_URL` to production endpoint
3. Deploy with environment variables set
4. Monitor API usage and error rates

### Monitoring

Track key metrics:
- API response time
- Error rate
- Usage volume
- Key authentication status

---

## Conclusion

The Sofia Core Provider Architecture ensures complete sovereignty over AI operations while providing a simple, type-safe interface for developers. By enforcing Sofia Core as the exclusive provider, we maintain identity preservation, eliminate external dependencies, and enable full governance over all AI-powered features.

**Version**: 1.0.0  
**Last Updated**: 2026-02-04  
**Maintained By**: Emerald Estates® and Mr. Clayton-M. Bernard-Ex.
