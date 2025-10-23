# Building Prebuilt Packages for Distribution

**Date**: October 23, 2025
**Purpose**: Instructions for creating prebuilt XRT packages

---

## 📦 Building XRT .deb Packages

### Prerequisites

```bash
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
```

### Build XRT from Source

```bash
# Clone the AMD XDNA driver repository
cd ~
git clone https://github.com/amd/xdna-driver
cd xdna-driver

# Build XRT (takes 15-30 minutes)
./build.sh -release

# Find the generated .deb packages
ls -lh build/Release/*.deb
```

**Expected Output**:
```
build/Release/
├── xrt-base_2.20.0_amd64.deb          (~30MB)
├── xrt-npu_2.20.0_amd64.deb           (~30MB)
└── xrt_plugin-amdxdna_2.20_amd64.deb  (~20MB)
```

### Copy to Release Directory

```bash
# Copy to unicorn-npu-core releases
cp build/Release/*.deb \
   /home/ucadmin/UC-1/unicorn-npu-core/releases/v1.0.0/xrt/

# Verify
ls -lh /home/ucadmin/UC-1/unicorn-npu-core/releases/v1.0.0/xrt/
```

---

## 🔧 Packaging Kernel Modules

### Current Kernel Module

```bash
# Get current kernel version
KERNEL_VERSION=$(uname -r)

# Find the kernel module
sudo find /lib/modules/${KERNEL_VERSION} -name "amdxdna.ko*"

# Copy to releases
sudo cp /lib/modules/${KERNEL_VERSION}/updates/dkms/amdxdna.ko.zst \
   /home/ucadmin/UC-1/unicorn-npu-core/releases/v1.0.0/kernel-modules/amdxdna-${KERNEL_VERSION}.ko.zst

# Fix ownership
sudo chown $USER:$USER \
   /home/ucadmin/UC-1/unicorn-npu-core/releases/v1.0.0/kernel-modules/*.ko.zst
```

### Multiple Kernel Versions (Optional)

If you have access to multiple systems or kernel versions:

```bash
# For each kernel version you want to support
for KERNEL in 6.14.0-34-generic 6.8.0-48-generic 6.5.0-35-generic; do
    # Build DKMS module for that kernel
    # (requires that kernel headers are installed)
    sudo dkms build -m amdxdna -v 2.20.0 -k ${KERNEL}

    # Copy module
    sudo cp /lib/modules/${KERNEL}/updates/dkms/amdxdna.ko.zst \
       /home/ucadmin/UC-1/unicorn-npu-core/releases/v1.0.0/kernel-modules/amdxdna-${KERNEL}.ko.zst
done
```

---

## 📋 Generate Checksums

```bash
cd /home/ucadmin/UC-1/unicorn-npu-core/releases/v1.0.0

# Generate SHA256 checksums for all files
find . -type f \( -name "*.deb" -o -name "*.ko.zst" \) -exec sha256sum {} \; > checksums.txt

cat checksums.txt
```

---

## 📤 Upload to GitHub Release

### 1. Create Release on GitHub

```bash
# Tag the release
cd /home/ucadmin/UC-1/unicorn-npu-core
git tag -a v1.0.0 -m "Release v1.0.0 - Prebuilt binaries included"
git push origin v1.0.0
```

### 2. Upload Release Assets

Via GitHub web interface:
1. Go to https://github.com/Unicorn-Commander/unicorn-npu-core/releases
2. Click "Draft a new release"
3. Choose tag: v1.0.0
4. Upload files:
   - `xrt/xrt-base_2.20.0_amd64.deb`
   - `xrt/xrt-npu_2.20.0_amd64.deb`
   - `xrt/xrt_plugin-amdxdna_2.20_amd64.deb`
   - `kernel-modules/amdxdna-6.14.0-34-generic.ko.zst`
   - `checksums.txt`
   - `install-xrt-prebuilt.sh`

Or via GitHub CLI:
```bash
# Install gh CLI if needed
# sudo apt install gh

# Upload release
gh release create v1.0.0 \
  --title "v1.0.0 - Prebuilt Binaries for AMD Phoenix NPU" \
  --notes "First release with prebuilt XRT packages" \
  xrt/*.deb \
  kernel-modules/*.ko.zst \
  checksums.txt \
  scripts/install-xrt-prebuilt.sh
```

---

## ✅ Verification

After uploading, test download:

```bash
# Test download XRT
wget https://github.com/Unicorn-Commander/unicorn-npu-core/releases/download/v1.0.0/xrt-base_2.20.0_amd64.deb

# Test download kernel module
wget https://github.com/Unicorn-Commander/unicorn-npu-core/releases/download/v1.0.0/amdxdna-6.14.0-34-generic.ko.zst

# Verify checksums
wget https://github.com/Unicorn-Commander/unicorn-npu-core/releases/download/v1.0.0/checksums.txt
sha256sum -c checksums.txt
```

---

## 📊 Expected File Sizes

| File | Size | Purpose |
|------|------|---------|
| xrt-base_2.20.0_amd64.deb | ~30MB | XRT base runtime |
| xrt-npu_2.20.0_amd64.deb | ~30MB | NPU support |
| xrt_plugin-amdxdna_2.20_amd64.deb | ~20MB | XDNA driver plugin |
| amdxdna-*.ko.zst | ~320KB | Kernel module |
| **Total** | **~80.3MB** | Complete prebuilt package |

---

## 🔄 Update Process

When XRT version changes:

1. Build new version: `./build.sh -release`
2. Copy new .debs to releases/vX.Y.Z/
3. Update version in installation scripts
4. Create new GitHub release tag
5. Upload new binaries

---

**Ready to build and package!**
