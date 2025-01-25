# Configure AWS Credentials
param(
    [Parameter(Mandatory=$true)]
    [string]$AccessKeyId,
    
    [Parameter(Mandatory=$true)]
    [string]$SecretAccessKey,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-west-2"
)

Write-Host "Configuring AWS Credentials..."

# Set AWS credentials as environment variables
$env:AWS_ACCESS_KEY_ID = $AccessKeyId
$env:AWS_SECRET_ACCESS_KEY = $SecretAccessKey
$env:AWS_DEFAULT_REGION = $Region

# Create AWS credentials file
$AWSFolder = "$env:USERPROFILE\.aws"
if (-not (Test-Path $AWSFolder)) {
    New-Item -ItemType Directory -Path $AWSFolder
}

$CredentialsContent = @"
[default]
aws_access_key_id = $AccessKeyId
aws_secret_access_key = $SecretAccessKey
region = $Region
"@

Set-Content -Path "$AWSFolder\credentials" -Value $CredentialsContent

# Verify AWS credentials
Write-Host "Verifying AWS credentials..."
aws sts get-caller-identity

if ($LASTEXITCODE -eq 0) {
    Write-Host "AWS credentials configured successfully!"
} else {
    Write-Host "Failed to configure AWS credentials. Please check your access key and secret."
    exit 1
}
