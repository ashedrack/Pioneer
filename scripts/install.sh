#!/bin/bash

# Default values
CLOUD_PIONEER_API_KEY=""
CLOUD_PIONEER_SITE="us"
CLOUD_PIONEER_AGENT_MAJOR_VERSION="1"
INSTALL_DIR="/opt/cloudpioneer-agent"
CONFIG_DIR="/etc/cloudpioneer"
LOG_DIR="/var/log/cloudpioneer"
SERVICE_NAME="cloudpioneer-agent"

# Parse command line arguments
while [ $# -gt 0 ]; do
    case $1 in
        -k|--api-key)
            CLOUD_PIONEER_API_KEY="$2"
            shift 2
            ;;
        -s|--site)
            CLOUD_PIONEER_SITE="$2"
            shift 2
            ;;
        -v|--version)
            CLOUD_PIONEER_AGENT_MAJOR_VERSION="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Check if API key is provided
if [ -z "$CLOUD_PIONEER_API_KEY" ]; then
    echo "Error: API key is required"
    exit 1
fi

# Function to detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VERSION=$VERSION_ID
    elif [ -f /etc/redhat-release ]; then
        OS="rhel"
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
        *)
            echo "Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac
}

# Create necessary directories
create_directories() {
    mkdir -p $INSTALL_DIR
    mkdir -p $CONFIG_DIR
    mkdir -p $LOG_DIR
}

# Download and install the agent
install_agent() {
    OS=$(detect_os)
    ARCH=$(detect_arch)
    VERSION=$CLOUD_PIONEER_AGENT_MAJOR_VERSION
    DOWNLOAD_URL="https://storage.googleapis.com/cloud-pioneer-agent/releases/${VERSION}/${OS}/${ARCH}/cloud-pioneer-agent"
    
    echo "Downloading Cloud Pioneer Agent..."
    curl -L -o $INSTALL_DIR/cloud-pioneer-agent $DOWNLOAD_URL
    chmod +x $INSTALL_DIR/cloud-pioneer-agent
}

# Configure the agent
configure_agent() {
    cat > $CONFIG_DIR/agent.yaml << EOF
api_key: ${CLOUD_PIONEER_API_KEY}
site: ${CLOUD_PIONEER_SITE}
log_level: info
log_file: ${LOG_DIR}/agent.log

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
    url: https://${CLOUD_PIONEER_SITE}.cloudpioneer.io
EOF
}

# Create systemd service
create_service() {
    cat > /etc/systemd/system/${SERVICE_NAME}.service << EOF
[Unit]
Description=Cloud Pioneer Monitoring Agent
After=network.target

[Service]
Type=simple
User=root
ExecStart=$INSTALL_DIR/cloud-pioneer-agent
Restart=always
RestartSec=10
StartLimitInterval=0

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable ${SERVICE_NAME}
    systemctl start ${SERVICE_NAME}
}

# Main installation process
echo "Installing Cloud Pioneer Agent..."
create_directories
install_agent
configure_agent
create_service

echo "Installation completed successfully!"
echo "Agent status: $(systemctl status ${SERVICE_NAME} --no-pager)"
