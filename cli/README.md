# Sofia CLI

Command-line interface for Sofia Core v5.0.0.

## Installation

```bash
pip install sofia-cli
```

Or from source:

```bash
cd cli
pip install -e .
```

## Usage

```bash
# Check health
sofia health

# Get system status
sofia status

# List services
sofia services

# Generate speech
sofia speak "Hello world" --language en --emotion warm

# Generate AI response
sofia generate "Explain quantum computing" --provider anthropic

# Get mesh topology
sofia mesh

# Get metrics
sofia metrics
```

## Commands

- **health** - Check system health
- **status** - Get detailed system status
- **services** - List all services
- **speak** - Text-to-speech synthesis
- **generate** - AI text generation
- **mesh** - Mesh network topology
- **metrics** - System metrics

## Configuration

Set base URL:

```bash
export SOFIA_BASE_URL=http://localhost:8000
```

## Requirements

- Python 3.11+
- Sofia Core v5.0.0 running

## License

MIT License
