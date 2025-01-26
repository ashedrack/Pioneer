#!/bin/bash

OS_TYPE=$(uname -s)

if [ "$OS_TYPE" == "Linux" ]; then
    if [ -f /etc/apt/sources.list ]; then
        sudo apt update
        sudo apt install cloudpioneer-agent
    elif [ -f /etc/yum.conf ]; then
        sudo yum install cloudpioneer-agent
    fi
elif [ "$OS_TYPE" == "Darwin" ]; then
    brew install cloudpioneer-agent
elif [[ "$OS_TYPE" == *"NT"* ]]; then
    echo "Installing on Windows using Homebrew..."
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed. Please install Homebrew first."
        exit 1
    fi
    brew install cloudpioneer-agent
else
    echo "Unsupported OS."
fi