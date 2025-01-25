# Deploy AWS Infrastructure Script
Write-Host "Deploying Cloud Pioneer Infrastructure..."

# Check AWS credentials
$AWSCredentialsFile = "$env:USERPROFILE\.aws\credentials"
if (-not (Test-Path $AWSCredentialsFile)) {
    Write-Host "AWS credentials not found. Please run configure.ps1 first."
    exit 1
}

# Initialize Terraform
Write-Host "Initializing Terraform..."
Set-Location -Path terraform
terraform init

# Apply Terraform configuration
Write-Host "Applying Terraform configuration..."
terraform apply -auto-approve

# Get outputs
$API_BASE_URL = terraform output -raw api_base_url
$env:API_BASE_URL = $API_BASE_URL

Write-Host "Infrastructure deployed successfully!"
Write-Host "API Base URL: $API_BASE_URL"

# Return to original directory
Set-Location -Path ..
