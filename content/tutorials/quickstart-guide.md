# Sofia Core v5.0.0 - Complete Quickstart Guide

## Prerequisites

- Docker 20.10+
- Python 3.11+
- 8GB RAM

## Installation (5 Minutes)

### Step 1: Download Sofia Core

```bash
wget https://github.com/emeraldorbit/sofia-core-backend/releases/download/v5.0.0/sofia-core-v5.0.0.zip
unzip sofia-core-v5.0.0.zip
cd sofia-core-v5.0.0
```

### Step 2: Start Services

```bash
./quick-start.sh
```

This will start all 10 services:
- Canonical Core (8000)
- 7 Domain Forks (8001-8007)
- Analytics (5000)
- Admin UI (3000)

### Step 3: Verify Installation

```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","version":"5.0.0"}
```

## Using the Python SDK

### Installation

```bash
pip install sofia-sdk
```

### Basic Usage

```python
from sofia_sdk import SofiaClient

# Initialize client
client = SofiaClient()

# Check health
print(client.health())

# Generate speech
audio = client.synthesize_speech("Hello world")
print(f"Audio URL: {audio['audio_url']}")

# Generate AI response
response = client.generate("What is quantum computing?")
print(response['response'])
```

## Using the CLI

### Installation

```bash
pip install sofia-cli
```

### Commands

```bash
# Check health
sofia health

# Get status
sofia status

# Generate speech
sofia speak "Hello world" --language en

# AI generation
sofia generate "Explain DNA computing"

# View services
sofia services
```

## Advanced Features

### DNA Computing

```python
result = client.dna_compute(
    sequence="ATCGATCGATCG",
    computation_type="parallel_search"
)
print(f"Parallel operations: {result['parallel_operations']}")
```

### Swarm Intelligence

```python
swarm = client.create_swarm(
    num_agents=100,
    coordination_strategy="consensus",
    objective="network_optimization"
)
print(f"Swarm ID: {swarm['swarm_id']}")
```

### Temporal Reasoning

```python
prediction = client.temporal_reasoning(
    query="Technology trends",
    time_context="last_decade",
    prediction_horizon=365
)
print(prediction['future_projection'])
```

## Next Steps

- [Explore the API Documentation](docs/API_REFERENCE.md)
- [Read the Architecture Guide](docs/ARCHITECTURE.md)
- [Join the Community Discord](https://discord.gg/sofia-core)

## Troubleshooting

### Services won't start:

```bash
# Check Docker
docker ps

# View logs
docker logs sofia_canonical_core
```

### Port conflicts:

```bash
# Stop all services
./stop-all.sh

# Free ports
lsof -ti:8000 | xargs kill -9

# Restart
./quick-start.sh
```

## Support

- **GitHub Issues**: github.com/emeraldorbit/sofia-core-backend/issues
- **Discord**: discord.gg/sofia-core
- **Email**: support@sofia-core.ai
