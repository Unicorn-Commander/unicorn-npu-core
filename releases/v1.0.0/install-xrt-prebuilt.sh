#!/bin/bash
#
# Install Prebuilt XRT Runtime for AMD Phoenix NPU
# Downloads and installs prebuilt XRT packages from GitHub Releases
#
# Usage: bash install-xrt-prebuilt.sh
#

set -e

VERSION="2.20.0"
RELEASE_VERSION="v1.0.0"
GITHUB_REPO="Unicorn-Commander/unicorn-npu-core"
RELEASE_URL="https://github.com/${GITHUB_REPO}/releases/download/${RELEASE_VERSION}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "📦 Installing Prebuilt XRT Runtime for AMD NPU"
echo "==============================================="
echo ""

# Check Ubuntu version
UBUNTU_VERSION=$(lsb_release -rs 2>/dev/null || echo "unknown")
if [ "$UBUNTU_VERSION" != "22.04" ] && [ "$UBUNTU_VERSION" != "24.04" ]; then
    echo -e "${YELLOW}⚠️  Warning: Prebuilt XRT is for Ubuntu 22.04/24.04${NC}"
    echo "   Your version: Ubuntu $UBUNTU_VERSION"
    read -p "   Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if XRT already installed
if [ -f "/opt/xilinx/xrt/bin/xrt-smi" ]; then
    echo -e "${GREEN}✅ XRT already installed${NC}"
    /opt/xilinx/xrt/bin/xrt-smi version 2>&1 | head -1
    read -p "Reinstall? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "📥 Downloading XRT packages from GitHub Releases..."
echo "   Source: ${RELEASE_URL}"
echo ""

# Download XRT base
echo -n "   xrt-base... "
if wget -q --show-progress "${RELEASE_URL}/xrt-base_${VERSION}_amd64.deb" 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ Failed${NC}"
    echo ""
    echo -e "${RED}❌ Download failed. Please check:${NC}"
    echo "   1. GitHub Release exists: https://github.com/${GITHUB_REPO}/releases/tag/${RELEASE_VERSION}"
    echo "   2. Internet connection working"
    echo "   3. Release assets uploaded"
    exit 1
fi

# Download XRT NPU
echo -n "   xrt-npu... "
wget -q --show-progress "${RELEASE_URL}/xrt-npu_${VERSION}_amd64.deb" 2>&1 && echo -e "${GREEN}✓${NC}" || { echo -e "${RED}✗ Failed${NC}"; exit 1; }

# Download XRT plugin
echo -n "   xrt_plugin-amdxdna... "
wget -q --show-progress "${RELEASE_URL}/xrt_plugin-amdxdna_2.20_amd64.deb" 2>&1 && echo -e "${GREEN}✓${NC}" || { echo -e "${RED}✗ Failed${NC}"; exit 1; }

echo ""
echo "📦 Installing XRT packages..."

# Install packages
sudo dpkg -i xrt-base_*.deb xrt-npu_*.deb xrt_plugin-amdxdna_*.deb 2>&1 | grep -v "dpkg: warning" || true

# Fix dependencies if needed
echo "🔧 Fixing dependencies..."
sudo apt-get install -f -y > /dev/null 2>&1

# Clean up
cd /
rm -rf "$TEMP_DIR"

echo ""
echo -e "${GREEN}✅ XRT Runtime installed successfully!${NC}"
echo ""

# Verify installation
if [ -f "/opt/xilinx/xrt/bin/xrt-smi" ]; then
    echo "📊 Verification:"
    /opt/xilinx/xrt/bin/xrt-smi version 2>&1 | head -3
    echo ""
    echo -e "${GREEN}Installation complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Install kernel module: bash install-amdxdna-prebuilt.sh"
    echo "2. Reboot system (or: sudo modprobe amdxdna)"
    echo "3. Verify NPU: ls -la /dev/accel/accel0"
else
    echo -e "${RED}❌ Installation verification failed${NC}"
    exit 1
fi
