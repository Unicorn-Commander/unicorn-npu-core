#!/bin/bash
#
# Package Kernel Module for Distribution
# Run this to copy the kernel module to the release directory
#

set -e

KERNEL_VERSION=$(uname -r)
RELEASE_DIR="/home/ucadmin/UC-1/unicorn-npu-core/releases/v1.0.0"

echo "📦 Packaging Kernel Module for GitHub Release"
echo "=============================================="
echo ""
echo "Kernel version: ${KERNEL_VERSION}"
echo "Release directory: ${RELEASE_DIR}"
echo ""

# Create kernel-modules directory
mkdir -p "${RELEASE_DIR}/kernel-modules"

# Copy kernel module (requires sudo)
echo "📋 Copying kernel module (requires sudo password)..."
sudo cp /lib/modules/${KERNEL_VERSION}/updates/dkms/amdxdna.ko.zst \
   "${RELEASE_DIR}/kernel-modules/amdxdna-${KERNEL_VERSION}.ko.zst"

# Fix ownership
echo "🔧 Fixing ownership..."
sudo chown $USER:$USER "${RELEASE_DIR}/kernel-modules/"*.ko.zst

# Verify
echo ""
echo "✅ Kernel module packaged:"
ls -lh "${RELEASE_DIR}/kernel-modules/"

echo ""
echo "📝 Regenerating checksums..."
cd "${RELEASE_DIR}"
find . -type f \( -name "*.deb" -o -name "*.ko.zst" -o -name "*.sh" \) -exec sha256sum {} \; > checksums.txt

echo ""
echo "✅ Checksums updated:"
cat checksums.txt

echo ""
echo "🎉 Kernel module packaged and ready for release!"
echo ""
echo "Next step: Upload to GitHub Release v1.0.0"
