#!/bin/bash

# CloudPioneer Agent Package Installation Script
# This script handles package manager-based installation of the CloudPioneer agent

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Default values
CLOUD_PIONEER_API_KEY=""
CLOUD_PIONEER_REGION="us-east-1"
INSTALL_METHOD="package"  # package, container, or kubernetes

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
        -m|--method)
            INSTALL_METHOD="$2"
            shift 2
            ;;
        -h|--help)
            echo "CloudPioneer Agent Package Installer"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  -k, --api-key     API key for authentication (required)"
            echo "  -r, --region      Region for agent connection (default: us-east-1)"
            echo "  -m, --method      Installation method (package, container, kubernetes)"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Check for required API key
if [ -z "$CLOUD_PIONEER_API_KEY" ]; then
    log_error "API key is required. Use --api-key or -k to provide it."
    exit 1
fi

# Function to add package repositories
add_package_repo() {
    log_info "Adding CloudPioneer package repository..."
    
    case $1 in
        apt)
            # Add apt repository for Debian/Ubuntu
            curl -fsSL https://packages.cloudpioneer.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloudpioneer-archive-keyring.gpg
            echo "deb [signed-by=/usr/share/keyrings/cloudpioneer-archive-keyring.gpg] https://packages.cloudpioneer.com/apt stable main" | sudo tee /etc/apt/sources.list.d/cloudpioneer.list
            sudo apt-get update
            ;;
        yum)
            # Add yum repository for RHEL/CentOS
            sudo rpm --import https://packages.cloudpioneer.com/gpg
            sudo tee /etc/yum.repos.d/cloudpioneer.repo << EOF
[cloudpioneer]
name=CloudPioneer Repository
baseurl=https://packages.cloudpioneer.com/yum/\$basearch
enabled=1
gpgcheck=1
gpgkey=https://packages.cloudpioneer.com/gpg
EOF
            sudo yum makecache
            ;;
        brew)
            # Add Homebrew tap
            brew tap cloudpioneer/agent
            ;;
    esac
}

# Function to install via package manager
install_package() {
    local OS_TYPE=$(uname -s)
    
    log_info "Installing CloudPioneer agent via package manager..."
    
    case $OS_TYPE in
        Linux)
            if [ -f /etc/debian_version ]; then
                add_package_repo apt
                sudo apt-get install -y cloudpioneer-agent
            elif [ -f /etc/redhat-release ]; then
                add_package_repo yum
                sudo yum install -y cloudpioneer-agent
            else
                log_error "Unsupported Linux distribution"
                exit 1
            fi
            ;;
        Darwin)
            add_package_repo brew
            brew install cloudpioneer-agent
            ;;
        MINGW*|MSYS*|CYGWIN*)
            log_info "Installing on Windows..."
            # Download and run Windows installer
            curl -o cloudpioneer-agent-setup.exe https://packages.cloudpioneer.com/windows/cloudpioneer-agent-setup.exe
            ./cloudpioneer-agent-setup.exe /VERYSILENT /API_KEY="$CLOUD_PIONEER_API_KEY" /REGION="$CLOUD_PIONEER_REGION"
            ;;
        *)
            log_error "Unsupported operating system: $OS_TYPE"
            exit 1
            ;;
    esac
}

# Function to install via container
install_container() {
    log_info "Installing CloudPioneer agent as a container..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is required for container installation"
        exit 1
    }
    
    # Pull and run the container
    docker pull cloudpioneer/agent:latest
    docker run -d \
        --name cloudpioneer-agent \
        --restart always \
        -e CLOUD_PIONEER_API_KEY="$CLOUD_PIONEER_API_KEY" \
        -e CLOUD_PIONEER_REGION="$CLOUD_PIONEER_REGION" \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /proc:/host/proc:ro \
        -v /sys:/host/sys:ro \
        cloudpioneer/agent:latest
}

# Function to install via Kubernetes
install_kubernetes() {
    log_info "Installing CloudPioneer agent on Kubernetes..."
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is required for Kubernetes installation"
        exit 1
    }
    
    # Create namespace
    kubectl create namespace cloudpioneer --dry-run=client -o yaml | kubectl apply -f -
    
    # Create secret for API key
    kubectl create secret generic cloudpioneer-agent-config \
        --from-literal=api-key="$CLOUD_PIONEER_API_KEY" \
        --from-literal=region="$CLOUD_PIONEER_REGION" \
        -n cloudpioneer \
        --dry-run=client -o yaml | kubectl apply -f -
    
    # Apply DaemonSet
    curl -s https://packages.cloudpioneer.com/kubernetes/agent-daemonset.yaml | \
        kubectl apply -f - -n cloudpioneer
}

# Main installation process
main() {
    log_info "Starting CloudPioneer agent installation..."
    
    case $INSTALL_METHOD in
        package)
            install_package
            ;;
        container)
            install_container
            ;;
        kubernetes)
            install_kubernetes
            ;;
        *)
            log_error "Invalid installation method: $INSTALL_METHOD"
            exit 1
            ;;
    esac
    
    log_info "Installation complete! 🚀"
    log_info "Agent Status: Installing and configuring..."
    log_info "Region: $CLOUD_PIONEER_REGION"
    log_info "Dashboard: https://dashboard.cloudpioneer.com"
    echo ""
    log_info "For support, contact support@cloudpioneer.com"
}

# Run main installation
main