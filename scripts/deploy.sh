#!/bin/bash

# Exit on error
set -e

# Configuration
AWS_REGION="us-east-1"
ECR_REPO_NAME="cloud-pioneer-app"
APP_NAME="cloud-pioneer"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "🚀 Starting deployment process for ${APP_NAME}..."

# Run tests
echo "Running tests..."
python -m pytest tests/
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Tests passed successfully${NC}"
else
    echo -e "${RED}✗ Tests failed${NC}"
    exit 1
fi

# Build Docker image
echo "Building Docker image..."
docker build -t ${APP_NAME} .

# Get ECR login token
echo "Logging into ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Tag and push image
echo "Tagging and pushing image to ECR..."
docker tag ${APP_NAME}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:latest

# Apply Terraform changes
echo "Applying infrastructure changes..."
cd terraform
terraform init
terraform apply -auto-approve

# Wait for deployment to complete
echo "Waiting for ECS service to stabilize..."
aws ecs wait services-stable \
    --cluster cloud-pioneer-cluster \
    --services cloud-pioneer-service \
    --region ${AWS_REGION}

echo -e "${GREEN}✓ Deployment completed successfully!${NC}"

# Get the ALB DNS name
ALB_DNS=$(terraform output -raw alb_dns_name)
echo -e "Application is accessible at: http://${ALB_DNS}"
