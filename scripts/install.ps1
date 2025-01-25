param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey,
    
    [Parameter(Mandatory=$false)]
    [string]$Site = "us",
    
    [Parameter(Mandatory=$false)]
    [string]$Version = "1"
)

$ErrorActionPreference = "Stop"

# Installation directories
$InstallDir = "C:\Program Files\CloudPioneer\Agent"
$ConfigDir = "C:\ProgramData\CloudPioneer\Agent"
$LogDir = "C:\ProgramData\CloudPioneer\Agent\logs"

# Create necessary directories
function Create-Directories {
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
}

# Download and install the agent
function Install-Agent {
    $arch = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { "386" }
    $downloadUrl = "https://storage.googleapis.com/cloud-pioneer-agent/releases/$Version/windows/$arch/cloud-pioneer-agent.exe"
    
    Write-Host "Downloading Cloud Pioneer Agent..."
    Invoke-WebRequest -Uri $downloadUrl -OutFile "$InstallDir\cloud-pioneer-agent.exe"
}

# Configure the agent
function Configure-Agent {
    $config = @"
api_key: $ApiKey
site: $Site
log_level: info
log_file: $LogDir\agent.log

collectors:
  system:
    enabled: true
  docker:
    enabled: true
  mysql:
    enabled: false

backends:
  influxdb:
    enabled: true
    url: https://$Site.cloudpioneer.io
"@

    Set-Content -Path "$ConfigDir\agent.yaml" -Value $config
}

# Create Windows service
function Create-Service {
    $serviceName = "CloudPioneerAgent"
    $serviceDisplayName = "Cloud Pioneer Monitoring Agent"
    $servicePath = "$InstallDir\cloud-pioneer-agent.exe"
    
    if (Get-Service $serviceName -ErrorAction SilentlyContinue) {
        Write-Host "Stopping existing service..."
        Stop-Service $serviceName
        Write-Host "Removing existing service..."
        sc.exe delete $serviceName
        Start-Sleep -Seconds 2
    }
    
    Write-Host "Creating service..."
    New-Service -Name $serviceName `
                -DisplayName $serviceDisplayName `
                -BinaryPathName $servicePath `
                -StartupType Automatic `
                -Description "Cloud Pioneer monitoring and optimization agent"
    
    Write-Host "Starting service..."
    Start-Service $serviceName
}

# Main installation process
try {
    Write-Host "Installing Cloud Pioneer Agent..."
    Create-Directories
    Install-Agent
    Configure-Agent
    Create-Service
    
    Write-Host "Installation completed successfully!"
    Write-Host "Agent status: $(Get-Service CloudPioneerAgent | Select-Object Status)"
}
catch {
    Write-Host "Error during installation: $_"
    exit 1
}
