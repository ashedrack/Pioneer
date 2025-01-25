#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "🚀 Starting Cloud Pioneer End-to-End Tests"

# Check required environment variables
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo -e "${RED}Error: AWS credentials not set${NC}"
    echo "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install pytest pytest-html docker psutil

# Deploy infrastructure
echo "Deploying test infrastructure..."
cd terraform
terraform init
terraform apply -auto-approve

# Get infrastructure outputs
API_BASE_URL=$(terraform output -raw api_base_url)
export API_BASE_URL

cd ..

# Run tests
echo "Running end-to-end tests..."
python -m pytest tests/end_to_end_test.py \
    --html=test-report.html \
    --self-contained-html

# Check test results
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed successfully!${NC}"
else
    echo -e "${RED}✗ Some tests failed. Check test-report.html for details${NC}"
    exit 1
fi

# Cleanup
echo "Cleaning up infrastructure..."
cd terraform
terraform destroy -auto-approve

# Deactivate virtual environment
deactivate

echo -e "${GREEN}✓ Testing completed!${NC}"
echo "Test report available at: test-report.html"
