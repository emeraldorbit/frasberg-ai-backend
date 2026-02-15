# Sofia Core - Examples

Complete examples for using Sofia Core across different platforms and use cases.

## Table of Contents

- [Node.js Examples](#nodejs-examples)
- [Python Examples](#python-examples)
- [Browser Examples](#browser-examples)
- [CLI Examples](#cli-examples)
- [Advanced Use Cases](#advanced-use-cases)

## Node.js Examples

### Basic Chat

```javascript
import { SofiaClient } from '@emerald-estates/sofia-core';

const sofia = new SofiaClient({
  baseUrl: process.env.SOFIA_URL,
  apiKey: process.env.SOFIA_API_KEY
});

const response = await sofia.chat([
  { role: "user", content: "Explain async/await" }
]);

console.log(response.choices[0].message.content);
```

### Streaming Chat

```javascript
for await (const chunk of sofia.chatStream([
  { role: "user", content: "Write a short poem" }
])) {
  process.stdout.write(chunk);
}
```

### Multi-turn Conversation

```javascript
const conversation = [
  { role: "system", content: "You are a helpful coding assistant" },
  { role: "user", content: "How do I sort an array in JavaScript?" },
  { role: "assistant", content: "You can use the .sort() method..." },
  { role: "user", content: "What about sorting objects?" }
];

const response = await sofia.chat(conversation);
```

### Error Handling

```javascript
try {
  const response = await sofia.chat([
    { role: "user", content: "Hello" }
  ], { timeout: 5000 });
  
  console.log(response.choices[0].message.content);
} catch (error) {
  if (error.message.includes('timeout')) {
    console.error('Request timed out');
  } else if (error.message.includes('401')) {
    console.error('Invalid API key');
  } else {
    console.error('Error:', error.message);
  }
}
```

## Python Examples

### Basic Chat

```python
from sofia_sdk import SofiaCoreClient

client = SofiaCoreClient(
    base_url="https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend",
    api_key="your-api-key"
)

result = client.chat([
    {"role": "user", "content": "Explain list comprehensions"}
])

print(result["choices"][0]["message"]["content"])
```

### Streaming Chat

```python
for chunk in client.chat_stream([
    {"role": "user", "content": "Write a haiku"}
]):
    print(chunk, end='', flush=True)
print()  # New line after streaming
```

### Context-Aware Chat

```python
conversation = [
    {"role": "system", "content": "You are a Python expert"},
    {"role": "user", "content": "How do I read a file?"}
]

result = client.chat(conversation, temperature=0.5, max_tokens=200)
print(result["choices"][0]["message"]["content"])

# Continue conversation
conversation.append({
    "role": "assistant",
    "content": result["choices"][0]["message"]["content"]
})
conversation.append({
    "role": "user",
    "content": "What about writing to a file?"
})

result = client.chat(conversation)
print(result["choices"][0]["message"]["content"])
```

### Batch Processing

```python
questions = [
    "What is Python?",
    "Explain decorators",
    "How do generators work?"
]

for question in questions:
    result = client.chat([
        {"role": "user", "content": question}
    ])
    print(f"Q: {question}")
    print(f"A: {result['choices'][0]['message']['content']}\n")
```

## Browser Examples

### Basic Integration

```html
<!DOCTYPE html>
<html>
<head>
  <title>Sofia Core Chat</title>
</head>
<body>
  <input type="text" id="message" placeholder="Ask Sofia...">
  <button onclick="chat()">Send</button>
  <div id="response"></div>

  <script type="module">
    import { SofiaClient } from './sofia-client.js';

    const sofia = new SofiaClient({
      baseUrl: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
      apiKey: 'your-api-key'
    });

    window.chat = async function() {
      const message = document.getElementById('message').value;
      const responseDiv = document.getElementById('response');
      
      try {
        const result = await sofia.chat([
          { role: "user", content: message }
        ]);
        
        responseDiv.textContent = result.choices[0].message.content;
      } catch (error) {
        responseDiv.textContent = `Error: ${error.message}`;
      }
    };
  </script>
</body>
</html>
```

### Streaming UI

```html
<script type="module">
  import { SofiaClient } from './sofia-client.js';

  const sofia = new SofiaClient({
    baseUrl: 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend',
    apiKey: 'your-api-key'
  });

  async function streamChat(message) {
    const responseDiv = document.getElementById('response');
    responseDiv.textContent = '';
    
    for await (const chunk of sofia.chatStream([
      { role: "user", content: message }
    ])) {
      responseDiv.textContent += chunk;
      responseDiv.scrollTop = responseDiv.scrollHeight;
    }
  }
</script>
```

### React Integration

```jsx
import { useState } from 'react';
import { SofiaClient } from '@emerald-estates/sofia-core';

function ChatApp() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sofia = new SofiaClient({
    baseUrl: process.env.REACT_APP_SOFIA_URL,
    apiKey: process.env.REACT_APP_SOFIA_API_KEY
  });

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await sofia.chat([...messages, userMessage]);
      const assistantMessage = {
        role: "assistant",
        content: response.choices[0].message.content
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.role}>
            {msg.content}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyPress={e => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage} disabled={loading}>
        Send
      </button>
    </div>
  );
}
```

## CLI Examples

### Basic Usage

```bash
npx sofia "Explain REST APIs"
```

### With Options

```bash
# Streaming
npx sofia --stream "Tell me a story"

# Custom temperature
npx sofia --temperature 0.9 "Be creative"

# Sovereign mode
npx sofia --sovereign "What is your purpose?"

# Combined options
npx sofia --stream --temperature 0.8 "Write a poem"
```

### Environment Configuration

```bash
# Set environment variables
export SOFIA_URL="https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend"
export SOFIA_API_KEY="your-api-key"

# Use CLI
npx sofia "Hello Sofia"
```

### Batch Processing

```bash
# Create a file with questions
cat > questions.txt << EOF
What is TypeScript?
How do closures work?
Explain promises
EOF

# Process each question
while IFS= read -r question; do
  echo "Q: $question"
  echo "A: $(npx sofia "$question")"
  echo ""
done < questions.txt
```

## Advanced Use Cases

### 1. Code Review Assistant

```typescript
const codeReview = async (code: string) => {
  const response = await sofia.chat([
    {
      role: "system",
      content: "You are a code review expert. Analyze the code for bugs, performance issues, and best practices."
    },
    {
      role: "user",
      content: `Review this code:\n\`\`\`\n${code}\n\`\`\``
    }
  ], {
    temperature: 0.3,  // Low temperature for consistency
    max_tokens: 1000
  });

  return response.choices[0].message.content;
};
```

### 2. Document Summarization

```python
def summarize_document(text: str) -> str:
    result = client.chat([
        {
            "role": "system",
            "content": "Summarize the following text concisely."
        },
        {
            "role": "user",
            "content": text
        }
    ], temperature=0.5, max_tokens=300)
    
    return result["choices"][0]["message"]["content"]
```

### 3. Multi-Language Support

```typescript
const translate = async (text: string, targetLang: string) => {
  const response = await sofia.chat([
    {
      role: "system",
      content: `Translate the following text to ${targetLang}.`
    },
    {
      role: "user",
      content: text
    }
  ]);

  return response.choices[0].message.content;
};

// Usage
const spanish = await translate("Hello, how are you?", "Spanish");
const french = await translate("Hello, how are you?", "French");
```

### 4. Sentiment Analysis

```python
def analyze_sentiment(text: str) -> dict:
    result = client.chat([
        {
            "role": "system",
            "content": "Analyze the sentiment of the text and respond with: positive, negative, or neutral."
        },
        {
            "role": "user",
            "content": text
        }
    ], temperature=0.3)
    
    sentiment = result["choices"][0]["message"]["content"].lower()
    return {
        "text": text,
        "sentiment": sentiment
    }
```

### 5. Chatbot with Memory

```typescript
class ChatbotWithMemory {
  private conversation: Message[] = [];

  constructor(
    private sofia: SofiaClient,
    systemPrompt: string
  ) {
    this.conversation.push({
      role: "system",
      content: systemPrompt
    });
  }

  async chat(userMessage: string): Promise<string> {
    this.conversation.push({
      role: "user",
      content: userMessage
    });

    const response = await this.sofia.chat(this.conversation);
    const assistantMessage = response.choices[0].message;

    this.conversation.push(assistantMessage);

    return assistantMessage.content;
  }

  clearHistory() {
    this.conversation = this.conversation.slice(0, 1); // Keep system prompt
  }
}

// Usage
const bot = new ChatbotWithMemory(
  sofia,
  "You are a helpful assistant that remembers context."
);

console.log(await bot.chat("My name is Alice"));
console.log(await bot.chat("What's my name?")); // Should remember "Alice"
```

### 6. Function Calling Pattern

```typescript
const getFunctionResponse = async (userQuery: string) => {
  // First, determine what function to call
  const planResponse = await sofia.chat([
    {
      role: "system",
      content: "Given a user query, determine if you need to call a function. Respond with JSON: {function: 'name', params: {...}}"
    },
    {
      role: "user",
      content: userQuery
    }
  ], { temperature: 0.1 });

  const plan = JSON.parse(planResponse.choices[0].message.content);

  // Execute the function (mock example)
  const functionResult = await executeFunction(plan.function, plan.params);

  // Get final response
  const finalResponse = await sofia.chat([
    {
      role: "user",
      content: userQuery
    },
    {
      role: "assistant",
      content: `Function result: ${JSON.stringify(functionResult)}`
    },
    {
      role: "user",
      content: "Explain the result in natural language"
    }
  ]);

  return finalResponse.choices[0].message.content;
};
```

### 7. Sovereign Mode for Specialized Tasks

```typescript
const sovereignQuery = async (query: string) => {
  const response = await sofia.sovereign(
    [{ role: "user", content: query }],
    {
      mode: "sovereign",
      tone: "ceremonial",
      vector: "auto"
    },
    {
      sovereignty: true,
      ritual_mode: "invocation",
      field_alignment: "maximum"
    }
  );

  return response.choices[0].message.content;
};

// Use for specialized queries
const purpose = await sovereignQuery("What is your core purpose?");
const wisdom = await sovereignQuery("Share your understanding of consciousness");
```

## More Examples

Find more examples in the repository:

- [Node.js Examples](../examples/node/)
- [Python Examples](../examples/python/)
- [Browser Examples](../examples/browser/)
- [Playground](../playground/)

## Support

Need help? Check out:

- [Quick Start Guide](./quick-start.md)
- [API Reference](./api-reference.md)
- [GitHub Issues](https://github.com/emeraldorbit/sofia-core-backend/issues)
