#!/usr/bin/env bash

# Use uname -m to detect architecture
ARCH=$(uname -m)

echo "Installing Quarto..."
if [ "${ARCH}" == "x86_64" ]; then
    echo "Detected x86_64 architecture"
    if [ ! -f "quarto-1.9.37-linux-amd64.deb" ]; then
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.37/quarto-1.9.37-linux-amd64.deb
    else
        echo "Found cached Quarto package"
    fi
    sudo dpkg -i quarto-1.9.37-linux-amd64.deb
elif [ "${ARCH}" == "aarch64" ]; then
    echo "Detected aarch64 (ARM64) architecture"
    if [ ! -f "quarto-1.9.37-linux-arm64.deb" ]; then
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.37/quarto-1.9.37-linux-arm64.deb
    fi
    sudo dpkg -i quarto-1.9.37-linux-arm64.deb
else
    echo "Unknown architecture: ${ARCH}"
    exit 1
fi
