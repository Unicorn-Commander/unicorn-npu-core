#!/bin/bash
#
# Install Prebuilt AMD NPU Kernel Module
# Downloads and installs prebuilt amdxdna kernel module from GitHub Releases
#
# Usage: bash install-amdxdna-prebuilt.sh
#

set -e

RELEASE_VERSION="v1.0.0"
GITHUB_REPO="Unicorn-Commander/unicorn-npu-core"
RELEASE_URL="https://github.com/${GITHUB_REPO}/releases/download/${RELEASE_VERSION}"
KERNEL_VERSION=$(uname -r)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "📦 Installing Prebuilt AMD NPU Kernel Module"
echo "============================================="
echo ""
echo "Kernel version: ${KERNEL_VERSION}"
echo ""

# Check if module already loaded
if lsmod | grep -q amdxdna; then
    echo -e "${GREEN}✅ amdxdna module already loaded${NC}"
    modinfo amdxdna | grep -E "filename|version"
    echo ""
    read -p "Reinstall? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "📥 Attempting to download prebuilt kernel module..."
echo "   Looking for: amdxdna-${KERNEL_VERSION}.ko.zst"
echo ""

# Try to download prebuilt module
if wget -q "${RELEASE_URL}/amdxdna-${KERNEL_VERSION}.ko.zst"; then
    echo -e "${GREEN}✅ Prebuilt module found for your kernel!${NC}"
    echo ""
    echo "📦 Installing kernel module..."

    # Install module
    sudo mkdir -p /lib/modules/${KERNEL_VERSION}/updates/dkms
    sudo cp amdxdna-${KERNEL_VERSION}.ko.zst /lib/modules/${KERNEL_VERSION}/updates/dkms/amdxdna.ko.zst
    sudo depmod -a
    sudo modprobe amdxdna

    # Clean up
    cd /
    rm -rf "$TEMP_DIR"

    echo ""
    echo -e "${GREEN}✅ Kernel module installed successfully!${NC}"
    echo ""
    echo "📊 Verification:"
    lsmod | grep amdxdna
    modinfo amdxdna | grep -E "version|filename"

else
    echo -e "${YELLOW}⚠️  No prebuilt module for kernel ${KERNEL_VERSION}${NC}"
    echo ""
    echo "Available options:"
    echo "1. Build with DKMS (recommended) - takes 2-5 minutes"
    echo "2. Use a different kernel with prebuilt module"
    echo ""
    read -p "Build with DKMS? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo ""
        echo "📦 Installing DKMS build dependencies..."
        sudo apt-get update > /dev/null 2>&1
        sudo apt-get install -y dkms build-essential linux-headers-${KERNEL_VERSION} > /dev/null 2>&1

        echo "📥 Downloading amdxdna driver source..."
        cd ~
        if [ ! -d "xdna-driver" ]; then
            git clone https://github.com/amd/xdna-driver
        fi
        cd xdna-driver
        git pull

        echo "🔨 Building kernel module with DKMS..."
        ./amdxdna_drv.sh -install

        echo ""
        echo -e "${GREEN}✅ Kernel module built and installed!${NC}"
    else
        echo "Installation cancelled"
        cd /
        rm -rf "$TEMP_DIR"
        exit 1
    fi

    cd /
    rm -rf "$TEMP_DIR"
fi

echo ""
echo "🔍 Checking NPU device..."
if [ -e "/dev/accel/accel0" ]; then
    echo -e "${GREEN}✅ NPU device found: /dev/accel/accel0${NC}"
    ls -la /dev/accel/accel0
else
    echo -e "${YELLOW}⚠️  NPU device not yet available${NC}"
    echo "   Try: sudo modprobe amdxdna"
    echo "   Or reboot the system"
fi
