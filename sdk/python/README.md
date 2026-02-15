# Sofia SDK for Python

Official Python SDK for Sofia Core - Includes OpenAI-compatible client.

## Installation

```bash
pip install sofia-sdk
```

## Quick Start

### OpenAI-Compatible Client

```python
from sofia_sdk import SofiaCoreClient

# Initialize client
client = SofiaCoreClient(
    base_url="https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend",
    api_key="your-api-key"
)

# Basic chat
result = client.chat([
    {"role": "user", "content": "Hello Sofia"}
])

print(result["choices"][0]["message"]["content"])
```

### Original Client (for v5.0.0 features)

```python
from sofia_sdk import SofiaClient

# Initialize client
client = SofiaClient(base_url="http://localhost:8000")

# Check health
health = client.health()
print(health)

# Generate speech
audio = client.synthesize_speech("Hello world", language="en")
print(audio['audio_url'])

# Generate AI response
response = client.generate("Explain quantum computing")
print(response['response'])

# Store memory
memory = client.store_memory(
    user_id="user123",
    content="User prefers technical explanations",
    memory_type="preference",
    importance=0.9
)

# Recall memories
memories = client.recall_memories(user_id="user123", query="preferences")
print(memories)
```

## Features

- **Health Monitoring**: Check system health and metrics
- **Voice**: Text-to-speech and speech-to-text
- **AI**: LLM generation, validation, reasoning
- **Memory**: Long-term memory storage and recall
- **Distributed**: Mesh network operations
- **Quantum**: Post-quantum cryptography
- **v5 Features**: Biological computing, swarm intelligence, temporal reasoning

## v5.0.0 New Features

### DNA Computing
```python
result = client.dna_compute(
    sequence="ATCGATCGATCG",
    computation_type="parallel_search"
)
```

### Swarm Intelligence
```python
swarm = client.create_swarm(
    num_agents=100,
    coordination_strategy="consensus",
    objective="network_optimization"
)
```

### Temporal Reasoning
```python
prediction = client.temporal_reasoning(
    query="Technology trends",
    time_context="last_decade",
    prediction_horizon=365
)
```

## Documentation

See full documentation at: https://docs.sofia-core.ai

## License

MIT License
