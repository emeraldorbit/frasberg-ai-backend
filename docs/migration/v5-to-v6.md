# Migration Guide: Sofia Core v5 to v6

## Overview

This guide helps you migrate from Sofia Core 5.x to 6.0.0. The new version includes breaking changes, new features, and performance improvements.

## Breaking Changes

### 1. Python Version Requirement

**v5.x:** Python 3.9, 3.10, 3.11
**v6.0.0:** Python 3.11+ only

**Action Required:**
```bash
# Check your Python version
python --version

# Upgrade if necessary (Ubuntu/Debian)
sudo apt update
sudo apt install python3.11

# Or use pyenv
pyenv install 3.11
pyenv global 3.11
```

### 2. API Endpoint Restructuring

**v5.x:** `/v1/` endpoints
**v6.0.0:** `/v2/` endpoints

**Changes:**
```python
# OLD (v5.x)
client = SofiaClient(base_url="https://api.sofia.io/v1")
client.dna_compute(...)

# NEW (v6.0.0)
client = SofiaClient(base_url="https://api.sofia.io/v2")
client.dna_compute(...)  # Same method, different endpoint
```

The client automatically uses v2 endpoints in 6.0.0. If you explicitly set URLs, update them:

```python
# Update explicit URLs
OLD: "https://api.sofia.io/v1/dna/compute"
NEW: "https://api.sofia.io/v2/dna/compute"
```

### 3. Authentication System

**v5.x:** Simple API key authentication
**v6.0.0:** RBAC-based authentication with JWT

**Migration:**

```python
# OLD (v5.x)
client = SofiaClient(api_key="your-api-key")

# NEW (v6.0.0) - API keys still work for backwards compatibility
client = SofiaClient(api_key="your-api-key")

# NEW (v6.0.0) - Recommended: JWT authentication
from sofia_core.auth import JWTManager

jwt_manager = JWTManager()
access_token = jwt_manager.create_access_token(user_id="your-user-id")

client = SofiaClient(access_token=access_token)
```

**Setup RBAC:**

```bash
# Create roles
sofia-cli rbac create-role data_scientist \
  --permissions "dna.compute.*" "swarm.*" "temporal.*"

# Assign role to user
sofia-cli rbac assign-role user@company.com data_scientist
```

### 4. Configuration File Format

**v5.x:** YAML/JSON format
**v6.0.0:** Enhanced format with additional fields

**Old config (v5.x):**
```yaml
# config_v5.yaml
api:
  host: localhost
  port: 8000
database:
  url: postgresql://localhost/sofia
redis:
  url: redis://localhost:6379
```

**New config (v6.0.0):**
```yaml
# config_v6.yaml
api:
  host: localhost
  port: 8000
  version: v2  # NEW

security:  # NEW
  rbac_enabled: true
  rate_limiting: true
  audit_logging: true

observability:  # NEW
  telemetry_enabled: true
  telemetry_exporter: jaeger
  metrics_port: 9090

database:
  url: postgresql://localhost/sofia
  sharding: false  # NEW
  connection_pool_size: 100  # NEW

redis:
  url: redis://localhost:6379
  cluster: false  # NEW
```

**Auto-migration:**
```bash
# Migrate config automatically
sofia-cli config migrate --from config_v5.yaml --to config_v6.yaml
```

## Automated Migration

The easiest way to migrate is using the CLI tool:

```bash
# Install Sofia Core 6.0.0
pip install --upgrade sofia-core==6.0.0

# Run migration tool
sofia-cli migrate --from=5.x --to=6.0.0

# Follow the interactive prompts
```

The migration tool will:
1. Check your Python version
2. Update configuration files
3. Migrate database schema
4. Update API endpoints
5. Setup RBAC (optional)
6. Configure observability (optional)

## Manual Migration Steps

### Step 1: Update Dependencies

```bash
# Update Sofia Core
pip install --upgrade sofia-core==6.0.0

# Update related packages
pip install --upgrade sofia-cli==6.0.0
pip install --upgrade sofia-sdk==6.0.0

# Install enterprise features (optional)
pip install sofia-core[enterprise]==6.0.0
```

### Step 2: Update Configuration

```bash
# Backup old config
cp sofia_config.yaml sofia_config_v5_backup.yaml

# Generate new config
sofia-cli config generate --version 6.0.0 > sofia_config.yaml

# Edit and customize as needed
nano sofia_config.yaml
```

### Step 3: Database Migration

```bash
# Backup database
pg_dump sofia > sofia_backup.sql

# Run migrations
sofia-cli db migrate --from 5.x --to 6.0.0

# Verify migration
sofia-cli db verify
```

### Step 4: Update Application Code

**Import changes:**
```python
# OLD (v5.x)
from sofia_core import SofiaClient

# NEW (v6.0.0) - Same, but with new features available
from sofia_core import SofiaClient
from sofia_core.security import RBACManager  # NEW
from sofia_core.observability import Telemetry  # NEW
from sofia_core.hybrid import NeuralDNAHybrid  # NEW
```

**Client initialization:**
```python
# OLD (v5.x)
client = SofiaClient(api_key="your-key")

# NEW (v6.0.0) - Backwards compatible
client = SofiaClient(api_key="your-key")

# NEW (v6.0.0) - With new features
client = SofiaClient(
    api_key="your-key",
    enable_telemetry=True,
    enable_rate_limiting=True
)
```

### Step 5: Update Tests

```python
# Update test imports
from sofia_core.testing import TestClient  # NEW in v6

# Update test client
class TestSofiaCore:
    def setup_method(self):
        self.client = TestClient()  # Uses v2 API
    
    def test_dna_compute(self):
        result = self.client.dna_compute(sequence="ATCG")
        assert result is not None
```

### Step 6: Update Deployment

**Docker:**
```dockerfile
# OLD (v5.x)
FROM emeraldorbit/sofia-core:5.0.0

# NEW (v6.0.0)
FROM emeraldorbit/sofia-core:6.0.0
```

**Docker Compose:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  sofia-core:
    image: emeraldorbit/sofia-core:6.0.0  # Updated
    environment:
      - SOFIA_VERSION=6.0.0  # NEW
      - RBAC_ENABLED=true  # NEW
      - TELEMETRY_ENABLED=true  # NEW
    ports:
      - "8000:8000"
      - "9090:9090"  # NEW: Prometheus metrics
```

**Kubernetes:**
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sofia-core
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: sofia-core
        image: emeraldorbit/sofia-core:6.0.0  # Updated
        env:
        - name: SOFIA_VERSION
          value: "6.0.0"
        - name: RBAC_ENABLED
          value: "true"
```

## Feature Adoption Guide

### Adopting Enterprise Features

```python
# Enable RBAC
from sofia_core.security import RBACManager

rbac = RBACManager()
rbac.create_role("data_scientist", permissions=["dna.compute.*", "swarm.*"])
rbac.assign_role("user@company.com", "data_scientist")

# Enable observability
from sofia_core.observability import Telemetry

telemetry = Telemetry()
telemetry.configure(exporter="jaeger", endpoint="http://jaeger:14268")

# Enable rate limiting
from sofia_core.middleware import RateLimiter

limiter = RateLimiter(requests_per_minute=100)
```

### Adopting Advanced AI Features

```python
# Try Neural-DNA Hybrid
from sofia_core.hybrid import NeuralDNAHybrid

hybrid = NeuralDNAHybrid(neural_layers=[256, 512, 256])
hybrid.train(dataset=training_data, epochs=100)

# Try federated learning
from sofia_core.federated import FederatedLearning

federated = FederatedLearning(nodes=["node1", "node2", "node3"])
federated.train(model=base_model)
```

### Adopting Ecosystem Integrations

```python
# LangChain integration
from langchain.agents import SofiaCoreAgent

agent = SofiaCoreAgent(sofia_client=client)

# LlamaIndex integration
from llama_index.retrievers import SofiaCoreRetriever

retriever = SofiaCoreRetriever(sofia_client=client)
```

## Rollback Plan

If you encounter issues, you can roll back:

```bash
# Rollback Sofia Core
pip install sofia-core==5.0.0

# Restore database
psql sofia < sofia_backup.sql

# Restore config
cp sofia_config_v5_backup.yaml sofia_config.yaml

# Restart services
sudo systemctl restart sofia-core
```

## Common Issues

### Issue 1: Python Version Mismatch

**Error:** `RuntimeError: Sofia Core 6.0.0 requires Python 3.11+`

**Solution:**
```bash
# Upgrade Python
sudo apt install python3.11
# Or use pyenv
pyenv install 3.11
```

### Issue 2: API Endpoint Not Found

**Error:** `404 Not Found: /v1/dna/compute`

**Solution:**
```python
# Update client to use v2 endpoints
client = SofiaClient(base_url="https://api.sofia.io/v2")
```

### Issue 3: Authentication Failed

**Error:** `401 Unauthorized: Invalid API key`

**Solution:**
```bash
# Regenerate API key
sofia-cli auth regenerate-key

# Or use JWT
sofia-cli auth generate-jwt --user-id your-user-id
```

### Issue 4: Database Migration Failed

**Error:** `Database schema mismatch`

**Solution:**
```bash
# Run migration manually
sofia-cli db migrate --from 5.x --to 6.0.0 --force

# Or restore and retry
psql sofia < sofia_backup.sql
sofia-cli db migrate --from 5.x --to 6.0.0
```

## Testing Checklist

After migration, verify:

- [ ] Application starts successfully
- [ ] API endpoints respond correctly
- [ ] Database queries work as expected
- [ ] Authentication/authorization functions properly
- [ ] Telemetry data is being collected (if enabled)
- [ ] Metrics are being exported (if enabled)
- [ ] All tests pass
- [ ] Performance is acceptable
- [ ] No errors in logs

## Performance Improvements

You should see these improvements after migration:

- **DNA Compute:** 10× faster
- **Memory Usage:** 50% reduction
- **API Response Time:** 30% faster
- **Database Queries:** 5× faster with sharding
- **Swarm Coordination:** 3× improvement

Run benchmarks to verify:

```bash
sofia-cli benchmark --compare-with 5.0.0
```

## Support

If you need help with migration:

- **Documentation:** https://docs.sofia-core.io/migration/v5-to-v6
- **Discord:** https://discord.gg/sofia-core
- **GitHub Issues:** https://github.com/emeraldorbit/sofia-core-backend/issues
- **Email:** support@sofia-core.io
- **Enterprise Support:** enterprise@sofia-core.io

## Next Steps

After successful migration:

1. [Explore Enterprise Features](../enterprise/README.md)
2. [Try Advanced AI Features](../advanced-ai/README.md)
3. [Setup Integrations](../integrations/README.md)
4. [Optimize Performance](../guides/performance-tuning.md)
5. [Join the Community](https://discord.gg/sofia-core)

---

**Migration completed?** Share your experience in our [Discord community](https://discord.gg/sofia-core)!
