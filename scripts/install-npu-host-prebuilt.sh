#!/bin/bash
#
# Unicorn NPU Core - Host System Setup (with Prebuilt Binaries)
# Installs XRT runtime and NPU kernel module
#
# Automatically tries prebuilt binaries first, falls back to source compilation
#

set -e

RELEASE_VERSION="v1.0.0"
GITHUB_REPO="Unicorn-Commander/unicorn-npu-core"
RELEASE_URL="https://github.com/${GITHUB_REPO}/releases/download/${RELEASE_VERSION}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🦄 Unicorn NPU Core - Host System Setup"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo -e "${RED}❌ Please do NOT run this script as root${NC}"
   echo "   Run as regular user with sudo access"
   exit 1
fi

# Detect system
UBUNTU_VERSION=$(lsb_release -rs 2>/dev/null || echo "unknown")
KERNEL_VERSION=$(uname -r)
ARCH=$(dpkg --print-architecture 2>/dev/null || echo "amd64")

echo -e "${BLUE}System Information:${NC}"
echo "  OS: Ubuntu ${UBUNTU_VERSION}"
echo "  Kernel: ${KERNEL_VERSION}"
echo "  Arch: ${ARCH}"
echo ""

# Check for AMD NPU hardware
echo "🔍 Checking for AMD NPU hardware..."
if [ -e "/sys/bus/pci/devices/0000:c7:00.1" ] || [ -e "/dev/accel/accel0" ]; then
    echo -e "${GREEN}✅ AMD NPU hardware detected${NC}"
else
    echo -e "${YELLOW}⚠️  Warning: AMD NPU may not be present${NC}"
    echo "   This setup requires AMD Ryzen AI (Phoenix/Hawk Point/Strix)"
    read -p "   Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "================================================"
echo "Step 1: Installing XRT Runtime"
echo "================================================"
echo ""

# Check if XRT already installed
if [ -f "/opt/xilinx/xrt/bin/xrt-smi" ]; then
    echo -e "${GREEN}✅ XRT already installed${NC}"
    /opt/xilinx/xrt/bin/xrt-smi version 2>&1 | head -1 || true
    echo ""
    read -p "Reinstall XRT? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping XRT installation"
    else
        INSTALL_XRT="yes"
    fi
else
    INSTALL_XRT="yes"
fi

if [ "$INSTALL_XRT" = "yes" ]; then
    # Try prebuilt first for Ubuntu 22.04/24.04
    if [ "$UBUNTU_VERSION" = "22.04" ] || [ "$UBUNTU_VERSION" = "24.04" ]; then
        echo -e "${BLUE}Attempting to install prebuilt XRT...${NC}"
        echo "This will take ~30 seconds (vs 10-15 minutes to compile)"
        echo ""

        # Create temp directory
        TEMP_DIR=$(mktemp -d)
        cd "$TEMP_DIR"

        # Try to download prebuilt packages
        echo "📥 Downloading XRT packages..."
        if wget -q "${RELEASE_URL}/xrt-base_2.20.0_amd64.deb" && \
           wget -q "${RELEASE_URL}/xrt-npu_2.20.0_amd64.deb" && \
           wget -q "${RELEASE_URL}/xrt_plugin-amdxdna_2.20_amd64.deb"; then

            echo -e "${GREEN}✅ Prebuilt packages downloaded${NC}"
            echo ""
            echo "📦 Installing XRT packages..."

            # Install
            sudo dpkg -i xrt-*.deb 2>&1 | grep -v "dpkg: warning" || true
            sudo apt-get install -f -y > /dev/null 2>&1

            # Clean up
            cd /
            rm -rf "$TEMP_DIR"

            echo -e "${GREEN}✅ XRT installed (prebuilt)${NC}"
        else
            echo -e "${YELLOW}⚠️  Prebuilt packages not available${NC}"
            echo "   Falling back to source compilation..."
            cd /
            rm -rf "$TEMP_DIR"
            COMPILE_XRT="yes"
        fi
    else
        echo -e "${YELLOW}⚠️  No prebuilt for Ubuntu ${UBUNTU_VERSION}${NC}"
        echo "   Compiling from source..."
        COMPILE_XRT="yes"
    fi

    # Compile from source if needed
    if [ "$COMPILE_XRT" = "yes" ]; then
        echo ""
        echo "🔨 Compiling XRT from source..."
        echo "   This will take 10-15 minutes..."
        echo ""

        # Install build dependencies
        sudo apt-get update
        sudo apt-get install -y \
            build-essential \
            cmake \
            git \
            libboost-all-dev \
            libssl-dev \
            uuid-dev \
            libudev-dev \
            libdrm-dev \
            pkg-config

        # Clone and build
        cd ~
        if [ ! -d "xdna-driver" ]; then
            git clone https://github.com/amd/xdna-driver
        fi
        cd xdna-driver
        git pull

        ./build.sh -release

        # Install
        sudo dpkg -i build/Release/*.deb

        cd ~/UC-1 || cd ~

        echo -e "${GREEN}✅ XRT installed (compiled from source)${NC}"
    fi
fi

echo ""
echo "================================================"
echo "Step 2: Installing NPU Kernel Module"
echo "================================================"
echo ""

# Check if module already loaded
if lsmod | grep -q amdxdna; then
    echo -e "${GREEN}✅ amdxdna module already loaded${NC}"
    modinfo amdxdna | grep -E "version" || true
    echo ""
    read -p "Reinstall kernel module? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping kernel module installation"
        INSTALL_MODULE="no"
    else
        INSTALL_MODULE="yes"
    fi
else
    INSTALL_MODULE="yes"
fi

if [ "$INSTALL_MODULE" = "yes" ]; then
    # Try prebuilt module first
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    echo "📥 Attempting to download prebuilt kernel module..."
    echo "   Looking for: amdxdna-${KERNEL_VERSION}.ko.zst"

    if wget -q "${RELEASE_URL}/amdxdna-${KERNEL_VERSION}.ko.zst"; then
        echo -e "${GREEN}✅ Prebuilt module found!${NC}"
        echo ""
        echo "📦 Installing kernel module..."

        sudo mkdir -p /lib/modules/${KERNEL_VERSION}/updates/dkms
        sudo cp amdxdna-${KERNEL_VERSION}.ko.zst /lib/modules/${KERNEL_VERSION}/updates/dkms/amdxdna.ko.zst
        sudo depmod -a
        sudo modprobe amdxdna || true

        cd /
        rm -rf "$TEMP_DIR"

        echo -e "${GREEN}✅ Kernel module installed (prebuilt)${NC}"
    else
        echo -e "${YELLOW}⚠️  No prebuilt for kernel ${KERNEL_VERSION}${NC}"
        echo "   Building with DKMS (takes 2-5 minutes)..."
        cd /
        rm -rf "$TEMP_DIR"

        # Install DKMS build dependencies
        sudo apt-get update > /dev/null 2>&1
        sudo apt-get install -y dkms build-essential linux-headers-${KERNEL_VERSION} > /dev/null 2>&1

        # Clone driver if needed
        cd ~
        if [ ! -d "xdna-driver" ]; then
            git clone https://github.com/amd/xdna-driver
        fi
        cd xdna-driver
        git pull

        # Build and install
        ./amdxdna_drv.sh -install

        cd ~/UC-1 || cd ~

        echo -e "${GREEN}✅ Kernel module installed (DKMS)${NC}"
    fi
fi

echo ""
echo "================================================"
echo "Step 3: Configuring Permissions"
echo "================================================"
echo ""

# Add user to required groups
USER_NAME=${SUDO_USER:-$USER}
echo "Adding user ${USER_NAME} to render and video groups..."
sudo usermod -aG render ${USER_NAME}
sudo usermod -aG video ${USER_NAME}

# Setup udev rules
echo "Setting up udev rules..."
echo 'SUBSYSTEM=="accel", MODE="0666"' | sudo tee /etc/udev/rules.d/99-npu.rules > /dev/null
sudo udevadm control --reload-rules
sudo udevadm trigger

echo -e "${GREEN}✅ Permissions configured${NC}"

echo ""
echo "================================================"
echo "Step 4: Verification"
echo "================================================"
echo ""

# Verify XRT
if [ -f "/opt/xilinx/xrt/bin/xrt-smi" ]; then
    echo -e "${GREEN}✅ XRT Runtime:${NC}"
    /opt/xilinx/xrt/bin/xrt-smi version 2>&1 | head -3 || true
else
    echo -e "${RED}❌ XRT not found${NC}"
fi

echo ""

# Verify kernel module
if lsmod | grep -q amdxdna; then
    echo -e "${GREEN}✅ Kernel Module:${NC}"
    modinfo amdxdna | grep -E "version|filename" || true
else
    echo -e "${YELLOW}⚠️  Kernel module not loaded${NC}"
    echo "   Try: sudo modprobe amdxdna"
fi

echo ""

# Verify NPU device
if [ -e "/dev/accel/accel0" ]; then
    echo -e "${GREEN}✅ NPU Device:${NC}"
    ls -la /dev/accel/accel0
else
    echo -e "${YELLOW}⚠️  NPU device not yet available${NC}"
    echo "   May require reboot"
fi

echo ""
echo "================================================"
echo -e "${GREEN}🎉 NPU Host Setup Complete!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. ${YELLOW}Log out and log back in${NC} (for group changes to take effect)"
echo "2. Verify NPU: ls -la /dev/accel/accel0"
echo "3. Test XRT: /opt/xilinx/xrt/bin/xrt-smi examine"
echo "4. Install unicorn-npu-core Python library"
echo ""
echo "Time saved with prebuilts: ~10-15 minutes! ⚡"
echo ""
