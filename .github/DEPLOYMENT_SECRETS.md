# GitHub Actions Deployment Secrets Setup

## Required Secrets for GitHub Actions

Add these secrets to your GitHub repository settings:

### Docker Registry Credentials
```
DOCKER_USERNAME     - Your Docker Hub username
DOCKER_PASSWORD     - Your Docker Hub access token (not password)
```

### Server SSH Credentials
```
DEPLOY_KEY          - SSH private key for server access (paste full key)
DEPLOY_HOST         - Server hostname/IP (e.g., 1.2.3.4 or server.com)
DEPLOY_USER         - SSH user (e.g., ubuntu, root)
DEPLOY_PATH         - Deployment path (e.g., /opt/lookuply)
```

### Optional: Monitoring & Notifications
```
SLACK_WEBHOOK       - Slack webhook for notifications
SENTRY_DSN          - Sentry error tracking
```

---

## How to Generate SSH Key for Deployment

```bash
# Generate new SSH key (no passphrase for CI/CD)
ssh-keygen -t ed25519 -f lookuply-deploy -C "lookuply-ci" -N ""

# Copy public key to server
ssh-copy-id -i lookuply-deploy.pub user@server

# Get private key content (for GitHub secret)
cat lookuply-deploy
# Copy entire contents to DEPLOY_KEY secret
```

---

## How to Create Docker Hub Access Token

1. Go to Docker Hub: https://hub.docker.com/
2. Account Settings → Security → New Access Token
3. Create token with "Read, Write, Delete" permissions
4. Copy token to `DOCKER_PASSWORD` secret (NOT your Docker password)

---

## Docker Hub Setup

Create repositories:
```bash
# Login
docker login

# Create public repo for crawler
docker tag lookuply-crawler:latest yourusername/lookuply-crawler:latest
docker push yourusername/lookuply-crawler:latest

# Or create via web interface:
# https://hub.docker.com/repository/create
# Name: lookuply-crawler
# Visibility: Public
```

---

## Server Setup

### Prerequisites
```bash
# On deployment server as root/sudo
apt-get update
apt-get install -y docker.io docker-compose git

# Create deployment user
useradd -m -s /bin/bash deployer
usermod -aG docker deployer

# Create deployment directory
mkdir -p /opt/lookuply
chown deployer:deployer /opt/lookuply

# Clone repository
cd /opt/lookuply
git clone https://github.com/yourusername/lookuply.git .
chown -R deployer:deployer /opt/lookuply
```

### SSH Setup
```bash
# As deployer user
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add CI/CD public key
echo "your_ci_public_key" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Firewall Rules
```bash
# Allow GitHub Actions IPs (if using IP whitelist)
# GitHub Actions IPs: https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners

# Allow SSH
ufw allow 22/tcp

# Allow Docker ports
ufw allow 6379/tcp  # Redis
ufw allow 9200/tcp  # Elasticsearch
```

---

## Adding Secrets to GitHub

### Via GitHub Web UI
1. Go to: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret from the list above

### Via GitHub CLI
```bash
# Install GitHub CLI: https://cli.github.com

# Login
gh auth login

# Add secrets
gh secret set DOCKER_USERNAME --body "yourusername"
gh secret set DOCKER_PASSWORD --body "your-token-here"
gh secret set DEPLOY_KEY --body "$(cat lookuply-deploy)"
gh secret set DEPLOY_HOST --body "1.2.3.4"
gh secret set DEPLOY_USER --body "deployer"
gh secret set DEPLOY_PATH --body "/opt/lookuply"
```

---

## Verify Setup

```bash
# Test SSH access
ssh -i lookuply-deploy deployer@server "docker ps"

# Test Docker push
docker tag test yourusername/test:latest
docker push yourusername/test:latest

# Check GitHub Actions
# Go to: Actions → Test Crawler Configuration
# Should run on push to crawler/ files
```

---

## Troubleshooting

### "Permission denied (publickey)"
- Check SSH key is added to server's authorized_keys
- Verify key file permissions: `chmod 600 ~/.ssh/id_rsa`

### "docker: command not found"
- Install Docker on server: `apt-get install docker.io`
- Add user to docker group: `usermod -aG docker deployer`

### "Authentication required"
- Check Docker credentials
- Test: `docker login` on server

### GitHub Actions fails to connect
- Verify DEPLOY_KEY, DEPLOY_HOST, DEPLOY_USER in secrets
- Check server firewall allows SSH (port 22)
- Verify SSH key is added to authorized_keys

---

## Environment Variables

Create `.env.production` on server:

```bash
# Redis
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=your-secure-password

# Crawler
CONCURRENT_REQUESTS=32
DOWNLOAD_DELAY=1.5
MAX_DEPTH=3

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/crawler.log

# Monitoring
SENTRY_DSN=https://key@sentry.io/project-id
```

---

## Next Steps

1. ✅ Generate SSH key
2. ✅ Add public key to server
3. ✅ Create Docker Hub token
4. ✅ Add all 6 secrets to GitHub
5. ✅ Set up server with Docker
6. ✅ Test SSH connection
7. ✅ Push to GitHub to trigger first deployment
