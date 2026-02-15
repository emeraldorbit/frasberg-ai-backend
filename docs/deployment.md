# Sofia Core Backend - Deployment Guide

This guide provides comprehensive instructions for deploying the Sofia Core Backend to Supabase using GitHub Actions or manual deployment methods.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [GitHub Actions CI/CD Setup](#github-actions-cicd-setup)
3. [Manual Deployment](#manual-deployment)
4. [Testing Procedures](#testing-procedures)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying Sofia Core Backend, ensure you have:

- **Supabase Account**: Active Supabase project with project reference ID
- **GitHub Repository**: Access to the repository with admin/maintainer privileges
- **API Keys**: Sofia API credentials (SOFIA_URL and SOFIA_API_KEY)
- **Supabase CLI**: Installed globally (for manual deployment)

### Required Tools

```bash
# Install Supabase CLI
npm install -g supabase

# Verify installation
supabase --version
```

## GitHub Actions CI/CD Setup

The Sofia Core Backend uses GitHub Actions for automated deployment. The workflow is defined in `.github/workflows/deploy-sofia.yml`.

### Step 1: Configure GitHub Secrets

Navigate to your repository settings and add the following secrets:

**Repository Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SUPABASE_ACCESS_TOKEN` | Your Supabase access token | `sbp_...` |
| `SOFIA_URL` | Sofia API endpoint URL | `https://api.sofia.example.com` |
| `SOFIA_API_KEY` | Sofia API authentication key | `sk_...` |

#### Obtaining Supabase Access Token

1. Log in to [Supabase Dashboard](https://app.supabase.com)
2. Click on your profile icon (top-right)
3. Select "Account Settings"
4. Navigate to "Access Tokens"
5. Click "Generate new token"
6. Name it (e.g., "GitHub Actions Deploy")
7. Copy the token (starts with `sbp_`)
8. Add it to GitHub Secrets as `SUPABASE_ACCESS_TOKEN`

### Step 2: Verify Workflow Configuration

The deployment workflow is triggered by:

- **Push to main branch** with changes to:
  - `functions/**`
  - `.github/workflows/deploy-sofia.yml`
- **Manual trigger** via GitHub Actions UI

### Step 3: Enable GitHub Actions

1. Go to repository **Settings → Actions → General**
2. Under "Actions permissions", select **"Allow all actions and reusable workflows"**
3. Scroll to "Workflow permissions"
4. Select **"Read and write permissions"**
5. Click **Save**

### Step 4: Trigger Deployment

#### Automatic Deployment

Push changes to the `main` branch affecting `functions/**`:

```bash
git add supabase/functions/
git commit -m "Update Sofia Core functions"
git push origin main
```

#### Manual Deployment

1. Go to **Actions** tab in GitHub
2. Select **"Deploy Sofia Core Backend"** workflow
3. Click **"Run workflow"**
4. Select branch (usually `main`)
5. Click **"Run workflow"**

### Step 5: Monitor Deployment

1. Navigate to **Actions** tab
2. Click on the running workflow
3. Monitor deployment progress in real-time
4. Check for ✅ success indicator

Expected output:
```
✅ Sofia Core Backend deployed successfully
🌐 Endpoint: https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend
```

## Manual Deployment

For manual deployment or local testing, follow these steps:

### Step 1: Authenticate with Supabase

```bash
# Login to Supabase
supabase login

# Follow the browser prompt to authenticate
```

### Step 2: Link Your Project

```bash
# Link to your Supabase project
supabase link --project-ref sdtilgpppwhwtbxlbmik

# You'll be prompted to enter your database password
```

### Step 3: Set Environment Secrets

```bash
# Set required secrets
supabase secrets set SOFIA_URL="https://api.sofia.example.com"
supabase secrets set SOFIA_API_KEY="sk_your_api_key_here"

# Verify secrets are set (will show names only, not values)
supabase secrets list
```

### Step 4: Deploy Functions

```bash
# Deploy all functions
supabase functions deploy

# Or deploy specific function
supabase functions deploy sofia-core-backend

# Or deploy with verification
supabase functions deploy --verify-jwt
```

### Step 5: Verify Deployment

```bash
# Get function URL
supabase functions list

# Test function
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "user", "content": "Hello, Sofia!"}
    ]
  }'
```

## Testing Procedures

### Local Testing with Supabase CLI

```bash
# Start Supabase locally
supabase start

# Serve functions locally
supabase functions serve sofia-core-backend --env-file .env.local

# Test locally
curl -X POST http://localhost:54321/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer YOUR_LOCAL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [{"role": "user", "content": "Test message"}]
  }'
```

### Production Testing

#### Test Chat Completions

```bash
curl -X POST https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/v1/chat/completions \
  -H "Authorization: Bearer YOUR_PRODUCTION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sofia-core",
    "messages": [
      {"role": "system", "content": "You are Sofia, a helpful AI assistant."},
      {"role": "user", "content": "What is your purpose?"}
    ],
    "sofia_identity": {
      "mode": "unified",
      "tone": "conversational"
    }
  }'
```

Expected response:
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "..."
      },
      "finish_reason": "stop"
    }
  ]
}
```

### Integration Testing

Use the provided playgrounds for visual testing:

1. **React Playground**: `playground/react/Playground.tsx`
2. **Vue Playground**: `playground/vue/SofiaPlayground.vue`
3. **Web Component**: `playground/web-component/sofia-playground.js`

#### Using Web Component

```html
<!DOCTYPE html>
<html>
<head>
  <title>Sofia Core Test</title>
  <script src="./playground/web-component/sofia-playground.js"></script>
</head>
<body>
  <sofia-playground></sofia-playground>
</body>
</html>
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Deployment Fails: "Unauthorized"

**Problem**: GitHub Actions cannot authenticate with Supabase.

**Solution**:
```bash
# Verify SUPABASE_ACCESS_TOKEN is set correctly
# Generate new token from Supabase dashboard
# Update GitHub secret with new token
```

#### 2. Function Not Found

**Problem**: Function URL returns 404.

**Solution**:
```bash
# Check function is deployed
supabase functions list

# Redeploy if missing
supabase functions deploy sofia-core-backend

# Verify function name matches
```

#### 3. Secrets Not Available

**Problem**: Environment variables undefined in function.

**Solution**:
```bash
# List current secrets
supabase secrets list

# Set missing secrets
supabase secrets set SOFIA_URL="your_url"
supabase secrets set SOFIA_API_KEY="your_key"

# Redeploy function after setting secrets
supabase functions deploy sofia-core-backend
```

#### 4. CORS Errors

**Problem**: Browser shows CORS policy errors.

**Solution**:
- Ensure function returns proper CORS headers
- Add OPTIONS method handler for preflight requests
- Check `_shared/cors.ts` configuration

```typescript
// In your function
import { corsHeaders } from '../_shared/cors.ts';

// Return CORS headers in response
return new Response(JSON.stringify(data), {
  headers: { ...corsHeaders, 'Content-Type': 'application/json' }
});
```

#### 5. GitHub Actions: "Permission Denied"

**Problem**: Workflow fails with permission errors.

**Solution**:
1. Go to **Settings → Actions → General**
2. Under "Workflow permissions", select **"Read and write permissions"**
3. Enable **"Allow GitHub Actions to create and approve pull requests"**
4. Click **Save**

#### 6. Local Development: Port Already in Use

**Problem**: Cannot start local Supabase.

**Solution**:
```bash
# Stop existing Supabase instances
supabase stop

# Or stop all Docker containers
docker stop $(docker ps -q)

# Restart Supabase
supabase start
```

#### 7. Rate Limiting

**Problem**: Too many requests error.

**Solution**:
- Implement request throttling in client code
- Use proper authentication tokens
- Check Supabase project limits
- Consider upgrading Supabase plan if needed

### Debugging Tips

#### Enable Verbose Logging

```bash
# Deploy with debug logs
supabase functions deploy sofia-core-backend --debug

# View function logs
supabase functions logs sofia-core-backend --follow
```

#### Check Function Logs

```bash
# View recent logs
supabase functions logs sofia-core-backend

# Follow logs in real-time
supabase functions logs sofia-core-backend --follow

# Filter logs by level
supabase functions logs sofia-core-backend --level error
```

#### Test Authentication

```bash
# Verify JWT token is valid
supabase auth verify YOUR_TOKEN

# Get new token for testing
supabase auth create-user test@example.com password123
```

### Getting Help

If you encounter issues not covered here:

1. **Check Supabase Status**: https://status.supabase.com
2. **Review Function Logs**: `supabase functions logs sofia-core-backend`
3. **GitHub Issues**: https://github.com/emeraldorbit/sofia-core-backend/issues
4. **Supabase Docs**: https://supabase.com/docs/guides/functions
5. **Community Support**: https://github.com/emeraldorbit/sofia-core-backend/discussions

## Advanced Configuration

### Custom Domain Setup

To use a custom domain:

1. Go to Supabase Dashboard → Settings → API
2. Add custom domain under "Custom domains"
3. Update DNS records as instructed
4. Update `apiUrl` in playground files

### Environment-Specific Deployments

For staging/production environments:

```bash
# Set environment-specific secrets
supabase secrets set ENVIRONMENT="production"
supabase secrets set LOG_LEVEL="info"

# Deploy with specific configuration
supabase functions deploy sofia-core-backend --project-ref YOUR_STAGING_REF
```

### Rollback Procedure

If deployment causes issues:

```bash
# List function versions
supabase functions list --with-versions

# Rollback to previous version
supabase functions deploy sofia-core-backend --version PREVIOUS_VERSION_ID
```

## Monitoring and Maintenance

### Health Checks

Set up monitoring with:

```bash
# Create health check endpoint
curl https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend/health

# Expected response
{"status": "healthy", "version": "1.0.0"}
```

### Performance Monitoring

- Monitor function execution times in Supabase Dashboard
- Set up alerts for error rates
- Track API usage and rate limits

## Security Best Practices

1. **Never commit secrets** to version control
2. **Rotate API keys** regularly
3. **Use environment variables** for all sensitive data
4. **Enable rate limiting** on production endpoints
5. **Monitor logs** for suspicious activity
6. **Keep dependencies updated** regularly
7. **Use HTTPS only** for all API calls

## Next Steps

After successful deployment:

1. Test all endpoints with provided playgrounds
2. Set up monitoring and alerting
3. Configure custom domains (optional)
4. Review and optimize function performance
5. Set up automated backups
6. Document any custom configurations

For more information, see:
- [OpenAPI Schema](../openapi/sofia-core.json)
- [React Playground](../playground/react/Playground.tsx)
- [Vue Playground](../playground/vue/SofiaPlayground.vue)
- [Web Component](../playground/web-component/sofia-playground.js)
