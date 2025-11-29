# Lookuply Crawler - Deployment Guide

Complete guide for deploying the Lookuply web crawler using GitHub Actions and Docker.

## Overview

```
Code Push (GitHub)
       ↓
   Tests Run (GitHub Actions)
       ↓
   Docker Image Built & Pushed
       ↓
   Deployed to Server (SSH)
       ↓
   docker-compose up -d
       ↓
   Crawler Running
```

## Quick Start (5 minutes)

### Step 1: Setup Server
```bash
# SSH to your server
ssh user@your-server.com

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create deployment directory
sudo mkdir -p /opt/lookuply
sudo chown $USER:$USER /opt/lookuply
cd /opt/lookuply

# Clone repository
git clone https://github.com/yourusername/lookuply.git .
```

### Step 2: Setup GitHub Secrets

Go to: GitHub → Repository → Settings → Secrets and variables → Actions

Add these 6 secrets:
```
DOCKER_USERNAME = your-docker-username
DOCKER_PASSWORD = your-docker-token (from Docker Hub)
DEPLOY_KEY = ssh-private-key-content
DEPLOY_HOST = your-server-ip-or-domain
DEPLOY_USER = your-ssh-username
DEPLOY_PATH = /opt/lookuply
```

### Step 3: Push to GitHub
```bash
git add .
git commit -m "Add GitHub Actions deployment"
git push origin master

# GitHub Actions will automatically:
# 1. Run tests
# 2. Build Docker image
# 3. Push to Docker Hub
# 4. Deploy to your server
```

---

## Detailed Setup

### 1. Server Preparation

#### Minimum Requirements
- OS: Ubuntu 20.04+ or similar Linux
- CPU: 2+ cores
- RAM: 4GB+
- Disk: 50GB+ (depends on crawl size)
- Network: Stable internet connection

#### Installation Steps

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

### 2. Generate SSH Deployment Key

```bash
# Generate key (no passphrase!)
ssh-keygen -t ed25519 -f ~/.ssh/lookuply-deploy -C "github-actions" -N ""

# Copy public key to authorized_keys
cat ~/.ssh/lookuply-deploy.pub >> ~/.ssh/authorized_keys

# Get private key for GitHub secret
cat ~/.ssh/lookuply-deploy
# Copy entire output to DEPLOY_KEY secret

# Secure permissions
chmod 600 ~/.ssh/lookuply-deploy
chmod 700 ~/.ssh
```

### 3. Docker Hub Setup

```bash
# Create account at: https://hub.docker.com

# Login locally
docker login

# Create access token:
# Profile → Account Settings → Security → New Access Token
# Permissions: Read, Write, Delete
# Copy token to DOCKER_PASSWORD secret (NOT your password!)

# Create repository (or via web interface)
docker tag lookuply-crawler:latest yourusername/lookuply-crawler:latest
docker push yourusername/lookuply-crawler:latest
```

### 4. GitHub Secrets Configuration

#### Via Web UI
1. Go to: Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret:

```
Name: DOCKER_USERNAME
Value: your-docker-hub-username

Name: DOCKER_PASSWORD
Value: your-docker-access-token

Name: DEPLOY_KEY
Value: (content of ~/.ssh/lookuply-deploy)

Name: DEPLOY_HOST
Value: your.server.ip.address

Name: DEPLOY_USER
Value: ubuntu (or your ssh username)

Name: DEPLOY_PATH
Value: /opt/lookuply
```

#### Via GitHub CLI
```bash
# Install: https://cli.github.com
gh auth login

gh secret set DOCKER_USERNAME --body "yourusername"
gh secret set DOCKER_PASSWORD --body "your-token"
gh secret set DEPLOY_KEY --body "$(cat ~/.ssh/lookuply-deploy)"
gh secret set DEPLOY_HOST --body "your.server.com"
gh secret set DEPLOY_USER --body "ubuntu"
gh secret set DEPLOY_PATH --body "/opt/lookuply"
```

### 5. Test Deployment

```bash
# Make a test commit
git commit --allow-empty -m "Test deployment"
git push origin master

# Watch GitHub Actions:
# Repository → Actions → "Test Crawler Configuration"
# Should show:
# ✓ Set up Python
# ✓ Install dependencies
# ✓ Run tests
# ✓ Build Docker image
# ✓ Deploy to server
```

---

## Deployment Workflows

### Automatic Deployment (on push to master)
```
Push to master → Tests run → Build Docker → Deploy to server
```

### Manual Deployment (via GitHub UI)
1. Go to: Actions → "Deploy Crawler to Server"
2. Click: "Run workflow"
3. Select: staging or production
4. Click: "Run workflow"

### What Happens
1. **Test Phase** (5 min)
   - Run all crawler tests
   - Verify fastText model
   - Check configuration

2. **Build Phase** (5-10 min)
   - Build Docker image
   - Push to Docker Hub
   - Tag with commit SHA and latest

3. **Deploy Phase** (5 min)
   - SSH to server
   - Pull latest code
   - Pull Docker images
   - Run `docker-compose up -d`
   - Show status and logs

---

## Monitoring Deployment

### Watch Deployment Progress
```bash
# Via GitHub UI
Repository → Actions → Latest workflow run

# Via SSH
ssh user@server
cd /opt/lookuply
docker-compose logs -f
```

### Check Service Status
```bash
docker-compose ps

# Should show:
# NAME              STATUS
# lookuply-redis    Up (healthy)
# lookuply-crawler-en  Up (healthy)
# lookuply-crawler-de  Up (healthy)
# ...
```

### View Logs
```bash
# All containers
docker-compose logs --tail=50

# Specific service
docker-compose logs crawler-en

# Follow in real-time
docker-compose logs -f

# Search for errors
docker-compose logs | grep ERROR
```

### Health Check
```bash
# Redis
docker-compose exec redis redis-cli ping
# Should respond: PONG

# Crawler health
docker-compose ps
# Look for "Up (healthy)" status
```

---

## Common Tasks

### Scale Crawler to Multiple Languages
```bash
# Scale English crawler to 3 instances
docker-compose up -d --scale crawler-en=3

# Check
docker-compose ps
```

### Update Crawler Configuration
```bash
cd /opt/lookuply

# Edit configuration
nano crawler/config_languages.py

# Commit changes
git add .
git commit -m "Update crawler config"
git push origin master

# GitHub Actions will auto-deploy
```

### Roll Back Deployment
```bash
# Via git
git log --oneline
git revert <commit-hash>
git push origin master

# GitHub Actions redeploys previous version
```

### Stop Crawler Temporarily
```bash
docker-compose down
# Or pause service
docker-compose pause crawler-en
```

### Resume Crawler
```bash
docker-compose up -d
# Or unpause
docker-compose unpause crawler-en
```

---

## Environment Variables

Create `.env` file on server:

```bash
# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Crawler Settings
CONCURRENT_REQUESTS=32
DOWNLOAD_DELAY=1.5
USER_AGENT=Mozilla/5.0 (compatible; LookuplyBot/1.0)

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/crawler.log

# Languages to crawl (comma-separated)
LANGUAGES=en,de,fr
```

Then reference in `docker-compose.yml`:
```yaml
env_file:
  - .env
```

---

## Troubleshooting

### Deployment Fails with "Permission denied"
```bash
# Check SSH key
ls -la ~/.ssh/lookuply-deploy
# Should be: -rw------- (600)

# Verify on server
cat ~/.ssh/authorized_keys | grep github-actions
# Should contain your public key

# Fix permissions
chmod 600 ~/.ssh/lookuply-deploy
```

### Docker Push Fails with "Authentication required"
```bash
# Verify credentials
echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin

# Check token has Write permissions
# Docker Hub → Account Settings → Security → token-name
```

### Crawler Container Won't Start
```bash
# Check logs
docker-compose logs crawler-en

# Common issues:
# - fastText model not downloaded
# - Missing dependencies
# - Network issues

# Rebuild image
docker-compose build --no-cache crawler-en
docker-compose up -d crawler-en
```

### Redis Connection Error
```bash
# Check Redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping

# Restart if needed
docker-compose restart redis
```

### Out of Disk Space
```bash
# Check disk usage
docker system df

# Clean up unused images/containers
docker system prune -a --volumes

# Check log size
du -sh /var/lib/docker/containers
```

---

## Security Best Practices

1. **SSH Key**
   - Use ed25519 (more secure than RSA)
   - No passphrase (for CI/CD automation)
   - Restrict permissions: `chmod 600`

2. **Docker Hub Token**
   - Use token, not password
   - Grant minimal permissions needed
   - Rotate regularly

3. **GitHub Secrets**
   - Never log secrets in CI/CD output
   - Limit who can view secrets
   - Use branch protection rules

4. **Server Firewall**
   - Only allow SSH from trusted IPs
   - Close unused ports
   - Use VPC/Private network if available

5. **SSL/HTTPS**
   - Use SSL certificates for web services
   - Renew before expiration
   - Redirect HTTP to HTTPS

---

## Performance Optimization

### Docker Image Size
```bash
# Check image size
docker images lookuply-crawler

# Reduce by:
# - Using slim base image (done: python:3.11-slim)
# - Multi-stage builds
# - Cleaning package managers
# - Removing unnecessary files
```

### Memory Usage
```bash
# Monitor memory
docker stats

# If high memory:
# - Reduce CONCURRENT_REQUESTS
# - Limit links per page
# - Implement pagination/batching
```

### Network Bandwidth
```bash
# Monitor network
docker stats

# If high bandwidth:
# - Increase DOWNLOAD_DELAY
# - Reduce concurrent requests
# - Implement smart rate limiting
```

---

## Monitoring & Logging

### Sentry Integration (Optional)
```bash
# Add to GitHub secrets
SENTRY_DSN=https://key@sentry.io/12345

# Add to docker-compose.yml
environment:
  - SENTRY_DSN=${SENTRY_DSN}

# Crawler will auto-report errors
```

### Slack Notifications (Optional)
```bash
# Add to GitHub secrets
SLACK_WEBHOOK=https://hooks.slack.com/services/...

# GitHub Actions will notify on deploy success/failure
```

---

## Next Steps

1. ✅ Follow "Quick Start" section above
2. ✅ Test deployment with test commit
3. ✅ Monitor logs: `docker-compose logs -f`
4. ✅ Verify crawling: `docker ps`
5. ✅ Check health: `docker-compose ps`
6. ✅ Scale crawlers: `docker-compose up -d --scale crawler-en=3`
7. ✅ Review logs daily for errors

---

## Support

For issues:
1. Check logs: `docker-compose logs`
2. See Troubleshooting section above
3. Check GitHub Actions workflow
4. Test locally first: `python crawler/test_crawler_config.py`

---

**Lookuply Crawler Deployment**
Last Updated: 2025-11-29
