#!/bin/bash

set -e

# CloudPioneer Agent Installer
# This script installs and configures the CloudPioneer agent on supported platforms

# Default values
CLOUD_PIONEER_API_KEY=""
CLOUD_PIONEER_REGION="us-east-1"
CLOUD_PIONEER_VERSION="latest"
INSTALL_DIR="/opt/cloudpioneer-agent"
CONFIG_DIR="/etc/cloudpioneer"
LOG_DIR="/var/log/cloudpioneer"
SERVICE_NAME="cloudpioneer-agent"
TELEMETRY_ENDPOINT="https://telemetry.cloudpioneer.com/install"
DOWNLOAD_BASE_URL="https://download.cloudpioneer.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Parse command line arguments
while [ $# -gt 0 ]; do
    case $1 in
        -k|--api-key)
            CLOUD_PIONEER_API_KEY="$2"
            shift 2
            ;;
        -r|--region)
            CLOUD_PIONEER_REGION="$2"
            shift 2
            ;;
        -v|--version)
            CLOUD_PIONEER_VERSION="$2"
            shift 2
            ;;
        --no-telemetry)
            DISABLE_TELEMETRY=true
            shift
            ;;
        -h|--help)
            echo "CloudPioneer Agent Installer"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  -k, --api-key     API key for authentication (required)"
            echo "  -r, --region      Region for agent connection (default: us-east-1)"
            echo "  -v, --version     Agent version to install (default: latest)"
            echo "  --no-telemetry    Disable installation telemetry"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Verify root/admin privileges
check_privileges() {
    if [ "$(id -u)" != "0" ]; then
        log_error "This script must be run as root or with sudo privileges"
        exit 1
    fi
}

# Function to detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VERSION=$VERSION_ID
    elif [ -f /etc/redhat-release ]; then
        OS="rhel"
    elif [ "$(uname)" == "Darwin" ]; then
        OS="darwin"
        VERSION=$(sw_vers -productVersion)
    elif [ "$(uname -s)" == "Windows_NT" ]; then
        OS="windows"
        VERSION=$(cmd /c ver | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
    else
        OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    fi
    echo $OS
}

# Function to detect architecture
detect_arch() {
    ARCH=$(uname -m)
    case $ARCH in
        x86_64)
            echo "amd64"
            ;;
        aarch64)
            echo "arm64"
            ;;
        armv7l)
            echo "armv7"
            ;;
        *)
            log_error "Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac
}

# Send telemetry data
send_telemetry() {
    if [ "$DISABLE_TELEMETRY" != "true" ]; then
        local data=$(cat << EOF
{
    "os": "$OS",
    "version": "$VERSION",
    "arch": "$ARCH",
    "agent_version": "$CLOUD_PIONEER_VERSION",
    "region": "$CLOUD_PIONEER_REGION",
    "status": "$1"
}
EOF
)
        curl -s -X POST -H "Content-Type: application/json" -d "$data" "$TELEMETRY_ENDPOINT" || true
    fi
}

# Create necessary directories
create_directories() {
    log_info "Creating installation directories..."
    mkdir -p "$INSTALL_DIR" "$CONFIG_DIR" "$LOG_DIR"
    chmod 755 "$INSTALL_DIR" "$CONFIG_DIR"
    chmod 744 "$LOG_DIR"
}

# Download and install the agent
install_agent() {
    local OS=$(detect_os)
    local ARCH=$(detect_arch)
    local DOWNLOAD_URL="$DOWNLOAD_BASE_URL/$CLOUD_PIONEER_VERSION/$OS/$ARCH/cloudpioneer-agent"
    
    log_info "Downloading CloudPioneer agent..."
    if ! curl -f -L -o "$INSTALL_DIR/cloudpioneer-agent" "$DOWNLOAD_URL"; then
        log_error "Failed to download agent"
        send_telemetry "download_failed"
        exit 1
    fi
    
    chmod +x "$INSTALL_DIR/cloudpioneer-agent"
}

# Configure the agent
configure_agent() {
    log_info "Configuring agent..."
    cat > "$CONFIG_DIR/config.yaml" << EOF
api_key: ${CLOUD_PIONEER_API_KEY}
region: ${CLOUD_PIONEER_REGION}
log_dir: ${LOG_DIR}
telemetry:
  enabled: true
  endpoint: https://telemetry.cloudpioneer.com
metrics:
  collection_interval: 60
  batch_size: 100
security:
  tls_enabled: true
  verify_ssl: true
EOF
    chmod 600 "$CONFIG_DIR/config.yaml"
}

# Create service configuration
create_service() {
    log_info "Setting up system service..."
    if [ "$OS" = "darwin" ]; then
        # Create LaunchDaemon for macOS
        cat > "/Library/LaunchDaemons/com.cloudpioneer.agent.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cloudpioneer.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>${INSTALL_DIR}/cloudpioneer-agent</string>
        <string>--config</string>
        <string>${CONFIG_DIR}/config.yaml</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/agent-error.log</string>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/agent.log</string>
</dict>
</plist>
EOF
        launchctl load -w "/Library/LaunchDaemons/com.cloudpioneer.agent.plist"
    elif [ "$OS" = "windows" ]; then
        # Create Windows Service
        "$INSTALL_DIR/cloudpioneer-agent" --service install
        net start cloudpioneer-agent
    else
        # Create systemd service for Linux
        cat > "/etc/systemd/system/$SERVICE_NAME.service" << EOF
[Unit]
Description=CloudPioneer Agent
After=network.target

[Service]
Type=simple
ExecStart=${INSTALL_DIR}/cloudpioneer-agent --config ${CONFIG_DIR}/config.yaml
Restart=always
RestartSec=10
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF
        systemctl daemon-reload
        systemctl enable "$SERVICE_NAME"
        systemctl start "$SERVICE_NAME"
    fi
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    local MAX_RETRIES=5
    local RETRY_COUNT=0
    
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if "$INSTALL_DIR/cloudpioneer-agent" --version >/dev/null 2>&1; then
            log_info "✅ CloudPioneer agent installed successfully!"
            send_telemetry "success"
            return 0
        fi
        RETRY_COUNT=$((RETRY_COUNT + 1))
        sleep 2
    done
    
    log_error "Failed to verify agent installation"
    send_telemetry "verification_failed"
    exit 1
}

# Main installation process
main() {
    # Check for required API key
    if [ -z "$CLOUD_PIONEER_API_KEY" ]; then
        log_error "API key is required. Use --api-key or -k to provide it."
        exit 1
    }

    log_info "Starting CloudPioneer Agent installation..."
    send_telemetry "started"

    check_privileges
    create_directories
    install_agent
    configure_agent
    create_service
    verify_installation

    echo ""
    log_info "Installation Complete! 🚀"
    log_info "Agent Status: Running"
    log_info "Region: $CLOUD_PIONEER_REGION"
    log_info "Dashboard: https://dashboard.cloudpioneer.com"
    log_info "Documentation: https://docs.cloudpioneer.com"
    echo ""
    log_info "For support, contact support@cloudpioneer.com"
}

# Run main installation
main
