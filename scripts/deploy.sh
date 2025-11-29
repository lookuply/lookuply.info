#!/bin/bash

# Lookuply Crawler Deployment Script
# Usage: ./scripts/deploy.sh [staging|production] [en|de|fr|all]

set -e

ENVIRONMENT=${1:-staging}
LANGUAGE=${2:-en}
DEPLOY_PATH="/opt/lookuply"
DOCKER_REGISTRY="docker.io"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Lookuply Crawler Deployment${NC}"
echo "Environment: $ENVIRONMENT"
echo "Language(s): $LANGUAGE"
echo ""

# Verify environment
if [[ "$ENVIRONMENT" != "staging" && "$ENVIRONMENT" != "production" ]]; then
    echo -e "${RED}❌ Invalid environment. Use 'staging' or 'production'${NC}"
    exit 1
fi

# Load environment variables
if [ -f ".env.$ENVIRONMENT" ]; then
    echo -e "${GREEN}✓ Loading .env.$ENVIRONMENT${NC}"
    source ".env.$ENVIRONMENT"
else
    echo -e "${RED}❌ .env.$ENVIRONMENT not found${NC}"
    exit 1
fi

# Functions
deploy_language() {
    local lang=$1
    echo -e "${YELLOW}📦 Deploying language: $lang${NC}"

    # Build image
    docker build \
        --target crawler-$lang \
        -t $DOCKER_REGISTRY/$DOCKER_USERNAME/lookuply-crawler:$lang \
        -f crawler/Dockerfile.multi \
        .

    # Push image
    docker push $DOCKER_REGISTRY/$DOCKER_USERNAME/lookuply-crawler:$lang

    # Deploy via SSH
    ssh -i "$DEPLOY_KEY" $DEPLOY_USER@$DEPLOY_HOST << EOF
        cd $DEPLOY_PATH
        docker pull $DOCKER_REGISTRY/$DOCKER_USERNAME/lookuply-crawler:$lang
        docker-compose -f docker-compose.$ENVIRONMENT.yml up -d crawler-$lang
        echo "Waiting for container to be healthy..."
        sleep 5
        docker-compose -f docker-compose.$ENVIRONMENT.yml ps
    EOF

    echo -e "${GREEN}✓ $lang deployed${NC}"
}

# Main deployment
echo -e "${YELLOW}Step 1: Testing${NC}"
python crawler/test_crawler_config.py || { echo -e "${RED}❌ Tests failed${NC}"; exit 1; }
echo -e "${GREEN}✓ All tests passed${NC}"

echo ""
echo -e "${YELLOW}Step 2: Building Docker images${NC}"
docker build -t $DOCKER_REGISTRY/$DOCKER_USERNAME/lookuply-crawler:latest crawler/

echo ""
echo -e "${YELLOW}Step 3: Pushing to registry${NC}"
docker push $DOCKER_REGISTRY/$DOCKER_USERNAME/lookuply-crawler:latest

echo ""
echo -e "${YELLOW}Step 4: Deploying to server${NC}"

# Connect to server and deploy
ssh -i "$DEPLOY_KEY" $DEPLOY_USER@$DEPLOY_HOST << 'SSHEOF'
    set -e
    cd $DEPLOY_PATH

    # Pull latest code
    git fetch origin
    git checkout master

    # Pull Docker images
    docker-compose -f docker-compose.$ENVIRONMENT.yml pull

    # Start services
    docker-compose -f docker-compose.$ENVIRONMENT.yml up -d

    # Wait for services to be ready
    sleep 10

    # Check status
    echo "Service Status:"
    docker-compose -f docker-compose.$ENVIRONMENT.yml ps

    # Show logs
    echo ""
    echo "Recent logs:"
    docker-compose -f docker-compose.$ENVIRONMENT.yml logs --tail=20
SSHEOF

echo ""
echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo ""
echo "Server: $DEPLOY_HOST"
echo "Path: $DEPLOY_PATH"
echo "Environment: $ENVIRONMENT"
echo ""
echo "Next steps:"
echo "  - Monitor logs: ssh $DEPLOY_USER@$DEPLOY_HOST 'cd $DEPLOY_PATH && docker-compose logs -f'"
echo "  - Scale crawler: docker-compose -f docker-compose.$ENVIRONMENT.yml up -d --scale crawler-en=3"
echo "  - Stop services: docker-compose -f docker-compose.$ENVIRONMENT.yml down"
