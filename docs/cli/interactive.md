# Interactive CLI Tutorial

Sofia Core 6.5.0 introduces an interactive CLI for guided setup and configuration.

## Installation

The CLI is included with Sofia Core 6.5.0:

```bash
pip install sofia-core==6.5.0
```

## Quick Start

Launch the interactive CLI:

```bash
sofia-cli interactive
```

## Features

### Guided Setup

The interactive CLI walks you through:

1. **Configuration** - Set up API keys, database connections, and settings
2. **Integration Selection** - Choose which integrations to enable
3. **Deployment Options** - Configure for local, cloud, or enterprise deployment
4. **Testing** - Run health checks and verify setup

### Auto-Migration

The CLI automatically detects configuration issues and offers fixes:

```bash
sofia-cli interactive --auto-migrate
```

### Hot Reload

Enable development mode with automatic reload:

```bash
sofia-cli dev --hot-reload
```

## Commands

### `sofia-cli interactive`

Launch interactive setup wizard.

**Options:**
- `--auto-migrate` - Automatically fix configuration issues
- `--expert-mode` - Show advanced options
- `--config PATH` - Use custom configuration file

### `sofia-cli config`

Manage configuration:

```bash
# Validate configuration
sofia-cli config validate

# Show current configuration
sofia-cli config show

# Edit configuration
sofia-cli config edit
```

### `sofia-cli dev`

Development tools:

```bash
# Start with hot reload
sofia-cli dev --hot-reload

# Enable debug logging
sofia-cli dev --debug

# Run with profiling
sofia-cli dev --profile
```

### `sofia-cli test`

Run tests and health checks:

```bash
# Run all tests
sofia-cli test

# Test specific integration
sofia-cli test --integration huggingface

# Run health check
sofia-cli test --health-check
```

## Configuration Validation

The CLI validates your configuration and provides helpful suggestions:

```bash
sofia-cli config validate
```

Example output:
```
✓ Database connection: OK
✓ Redis connection: OK
⚠ OpenAI API key not set (optional)
✗ Invalid port number: must be 1024-65535

Suggestions:
1. Set OPENAI_API_KEY in .env for LLM features
2. Change PORT to a valid value (e.g., 8000)

Run 'sofia-cli config edit' to fix issues.
```

## Examples

### Initial Setup

```bash
$ sofia-cli interactive

Welcome to Sofia Core 6.5.0 Interactive Setup!

? Select deployment type: (Use arrow keys)
❯ Local Development
  Cloud Deployment
  Enterprise Deployment

? Enable integrations: (Space to select)
❯ ◉ Hugging Face Transformers
  ◯ Weights & Biases
  ◉ MLflow
  ◯ Prefect
  ◯ Dagster

Configuration saved to config.yaml
✓ Setup complete! Run 'sofia-cli dev' to start.
```

### Development Mode

```bash
$ sofia-cli dev --hot-reload

[2026-02-09 18:20:00] Sofia Core 6.5.0 starting...
[2026-02-09 18:20:01] ✓ Database connected
[2026-02-09 18:20:01] ✓ Redis connected
[2026-02-09 18:20:02] ✓ Hot reload enabled
[2026-02-09 18:20:02] Server running at http://localhost:8000

Watching for file changes...
```

### Troubleshooting

```bash
$ sofia-cli test --health-check

Running health checks...

✓ Server: OK (http://localhost:8000)
✓ Database: OK (PostgreSQL 15.2)
✓ Redis: OK (7.0.10)
✓ Memory: OK (380 MB / 8 GB)
✓ CPU: OK (12% usage)

Integrations:
✓ Hugging Face: Ready
⚠ W&B: Not configured (API key missing)
✓ MLflow: Ready

All critical systems operational.
```

## Best Practices

### 1. Use Configuration Files

Store configuration in files instead of environment variables:

```bash
sofia-cli config export > config.yaml
```

### 2. Enable Auto-Migration

Always use auto-migration for upgrades:

```bash
sofia-cli interactive --auto-migrate
```

### 3. Validate Before Deployment

```bash
sofia-cli config validate
sofia-cli test --health-check
```

### 4. Use Hot Reload in Development

```bash
sofia-cli dev --hot-reload --debug
```

## Keyboard Shortcuts

In interactive mode:

- `↑/↓` - Navigate options
- `Space` - Select/deselect
- `Enter` - Confirm
- `Ctrl+C` - Cancel
- `?` - Show help

## Configuration File Format

```yaml
# config.yaml
version: "6.5.0"

server:
  port: 8000
  host: "0.0.0.0"
  workers: 4

database:
  url: "postgresql://localhost/sofia"
  pool_size: 10

redis:
  url: "redis://localhost:6379"

integrations:
  huggingface:
    enabled: true
    cache: true
  wandb:
    enabled: true
    project: "sofia-experiments"
  mlflow:
    enabled: true
    tracking_uri: "http://localhost:5000"

logging:
  level: "INFO"
  format: "colored"
```

## Troubleshooting

### CLI Not Found

```bash
# Reinstall Sofia Core
pip install --upgrade --force-reinstall sofia-core==6.5.0
```

### Permission Issues

```bash
# Run with sudo (if needed)
sudo sofia-cli interactive
```

### Configuration Errors

```bash
# Reset to defaults
sofia-cli config reset

# Validate configuration
sofia-cli config validate
```

## Learn More

- [Configuration Reference](../configuration.md)
- [Troubleshooting Guide](../troubleshooting.md)
- [CLI Reference](./cli-reference.md)
