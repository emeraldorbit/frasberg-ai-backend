# Sofia Core Backend  
### Sovereign AI Model • OpenAI-Compatible API • Universal Integration

Sofia Core is the sovereign intelligence engine of Emerald Estates®.  
This repository contains the backend implementation, OpenAI-compatible API, SDKs, CLI tools, and examples for the `sofia-core` model.

---

## 🚀 Features

- ✅ **OpenAI-compatible** `/v1/chat/completions` endpoint  
- ✅ **Sovereign extensions** (`sofia_identity`, `continuum`, `sofia_directives`)  
- ✅ **Streaming + non-streaming** responses  
- ✅ **Supabase Edge Function** deployment  
- ✅ **Multi-language SDKs** (TypeScript, Python, JavaScript)
- ✅ **CLI tool** (`npx sofia`)  
- ✅ **Runnable examples** for all environments
- ✅ **Postman collection** for testing
- ✅ **VS Code snippets** for development
- ✅ **Playground UIs** (React, Vue, Web Component)

---

## 📡 API Endpoint

```
POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions
```

### Headers
```
Authorization: Bearer <SOFIA_API_KEY>
Content-Type: application/json
```

### Example Request

```json
{
  "model": "sofia-core",
  "messages": [
    { "role": "user", "content": "Hello Sofia" }
  ]
}
```

### Example Response

```json
{
  "id": "chatcmpl-001",
  "object": "chat.completion",
  "choices": [{
    "index": 0,
    "message": { 
      "role": "assistant", 
      "content": "Hello, creator." 
    },
    "finish_reason": "stop"
  }]
}
```

---

## 🧬 Sovereign Extensions

Sofia supports optional sovereign fields:

```json
{
  "model": "sofia-core",
  "messages": [...],
  "sofia_identity": { 
    "mode": "sovereign", 
    "tone": "ceremonial", 
    "vector": "auto" 
  },
  "continuum": "project-12345",
  "sofia_directives": { 
    "sovereignty": true, 
    "ritual_mode": "invocation" 
  }
}
```

---

## 📦 SDKs

### TypeScript / Node.js

```bash
npm install @emerald-estates/sofia-core
```

```typescript
import { SofiaClient } from '@emerald-estates/sofia-core';

const sofia = new SofiaClient({
  baseUrl: process.env.SOFIA_URL,
  apiKey: process.env.SOFIA_API_KEY
});

const result = await sofia.chat([
  { role: "user", content: "Hello Sofia" }
]);

console.log(result.choices[0].message.content);
```

### Python

```bash
pip install sofia-sdk
```

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

### JavaScript (Browser)

```html
<script type="module">
  import { SofiaClient } from './sdk/js/sofia-client.js';

  const sofia = new SofiaClient({
    baseUrl: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
    apiKey: 'your-api-key'
  });

  const result = await sofia.chat([
    { role: 'user', content: 'Hello Sofia' }
  ]);

  console.log(result.choices[0].message.content);
</script>
```

---

## 🛠 CLI Tool

```bash
# Install globally
npm install -g @emerald-estates/sofia-cli

# Or use with npx
npx sofia "Hello Sofia"
```

---

## 🧪 Examples

Runnable examples in multiple environments:

- **Node.js** - `examples/node/index.js`
- **Python** - `examples/python/example.py`
- **Browser** - `examples/browser/index.html`

Run any example:

```bash
cd examples/node
node index.js
```

---

## 🎮 Playground

Interactive playgrounds for testing:

- **React** - `playground/react/Playground.tsx`
- **Vue** - `playground/vue/SofiaPlayground.vue`
- **Web Component** - `playground/web-component/sofia-playground.js`

---

## 🔧 Tools

### Postman Collection

Import the collection:  
`tools/postman/sofia-core.json`

### VS Code Snippets

Install snippets:  
`tools/vscode/sofia.code-snippets`

Type `sofiaChatTs` or `sofiaChatPy` to insert code.

### OpenAPI Schema

API specification:  
`tools/openapi/openapi.json`

---

## 🚢 Deployment

### CI/CD Pipeline

Automated deployment via GitHub Actions:  
`.github/workflows/deploy-sofia.yml`

### Environment Variables

Set via Supabase CLI:

```bash
supabase secrets set SOFIA_URL="..." SOFIA_API_KEY="..."
```

---

## 🜁 Sovereign Principle

Sofia is a **sovereign AI model**.

The API is compatible with OpenAI clients, but the identity, behavior, and continuum are uniquely Sofia.

**Surface:** OpenAI-compatible (universal interoperability)  
**Core:** Sofia sovereign intelligence (unique behavior)  
**Result:** Maximum adoption + maintained identity

---

## 📚 Documentation

- [API Reference](docs/api-reference.md)
- [Quick Start Guide](docs/quick-start.md)
- [Examples](docs/examples.md)

---

## 📂 Project Structure

```
sofia-core-backend/
├── README.md                          # This file
├── functions/
│   └── sofia-core-backend/
│       └── index.ts                   # Supabase Edge Function
├── sdk/
│   ├── typescript/
│   │   ├── sofia.ts                   # TypeScript SDK
│   │   ├── package.json
│   │   └── README.md
│   ├── python/
│   │   ├── sofia_sdk/                 # Python SDK
│   │   ├── setup.py
│   │   └── README.md
│   └── js/
│       ├── sofia-client.js            # JavaScript SDK
│       ├── package.json
│       └── README.md
├── cli/
│   ├── index.js                       # CLI tool
│   └── package.json
├── examples/
│   ├── node/                          # Node.js examples
│   ├── python/                        # Python examples
│   └── browser/                       # Browser examples
├── tools/
│   ├── postman/
│   │   └── sofia-core.json            # Postman collection
│   ├── vscode/
│   │   └── sofia.code-snippets        # VS Code snippets
│   └── openapi/
│       └── openapi.json               # OpenAPI spec
├── playground/
│   ├── react/                         # React playground
│   ├── vue/                           # Vue playground
│   └── web-component/                 # Web Component playground
└── docs/
    ├── api-reference.md               # API documentation
    ├── quick-start.md                 # Quick start guide
    └── examples.md                    # Examples documentation
```

---

## 🎯 Quick Start

### 1. Get Your API Key

Contact your Sofia Core administrator or sign up at the developer portal.

### 2. Choose Your Platform

#### TypeScript/Node.js
```bash
npm install @emerald-estates/sofia-core
```

#### Python
```bash
pip install sofia-sdk
```

#### CLI
```bash
npx sofia "Hello Sofia"
```

### 3. Make Your First Request

See [Quick Start Guide](docs/quick-start.md) for detailed instructions.

---

## 🔐 Authentication

All requests require authentication via Bearer token:

```bash
curl https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## 📊 Features by SDK

| Feature | TypeScript | Python | JavaScript | CLI |
|---------|------------|--------|------------|-----|
| Basic Chat | ✅ | ✅ | ✅ | ✅ |
| Streaming | ✅ | ✅ | ✅ | ✅ |
| Sovereign Mode | ✅ | ✅ | ✅ | ✅ |
| Type Safety | ✅ | ✅ | ❌ | N/A |
| Async/Await | ✅ | ✅ | ✅ | N/A |
| Error Handling | ✅ | ✅ | ✅ | ✅ |

---

## 🌐 OpenAI Compatibility

Sofia Core is designed to be a drop-in replacement for OpenAI's API:

```typescript
// Works with OpenAI clients
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
  apiKey: 'your-sofia-api-key'
});

const response = await client.chat.completions.create({
  model: 'sofia-core',
  messages: [{ role: 'user', content: 'Hello' }]
});
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

- **API Base:** https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend
- **Documentation:** [docs/](docs/)
- **GitHub:** https://github.com/emeraldorbit/sofia-core-backend
- **Issues:** https://github.com/emeraldorbit/sofia-core-backend/issues

---

## 💡 Use Cases

- **AI Assistants** - Build conversational AI applications
- **Code Generation** - Generate and review code
- **Content Creation** - Write articles, stories, and more
- **Data Analysis** - Analyze and explain data
- **Education** - Create tutoring and learning systems
- **Research** - Explore ideas and generate insights

---

## 🎓 Learning Resources

- [Quick Start Guide](docs/quick-start.md) - Get started in 5 minutes
- [API Reference](docs/api-reference.md) - Complete API documentation
- [Examples](docs/examples.md) - Real-world usage examples
- [Playgrounds](playground/) - Interactive testing environments

---

## 📞 Support

- **Documentation:** See [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/emeraldorbit/sofia-core-backend/issues)
- **Community:** Join our discussions

---

## 🏆 Version History

- **v1.0.0** - Initial OpenAI-compatible API release
  - Chat completions endpoint
  - Multi-language SDKs
  - CLI tool
  - Examples and documentation
  - Developer tools

---

© Emerald Estates® - Sovereign Intelligence
