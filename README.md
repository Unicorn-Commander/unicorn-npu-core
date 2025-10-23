# 🦄 Unicorn NPU Core

> **Production-ready NPU library for AMD Ryzen AI processors** — Hardware abstraction, runtime management, and prebuilt binaries for instant deployment.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-AMD%20Ryzen%20AI-red.svg)](https://www.amd.com/en/technologies/ryzen-ai)

**By [Magic Unicorn Unconventional Technology & Stuff Inc.](https://magicunicorn.tech)** | Part of the [Unicorn Commander](https://unicorncommander.com) ecosystem

---

## 📖 What is This? (For Everyone)

Unicorn NPU Core makes it simple to use the Neural Processing Unit (NPU) in your AMD Ryzen AI laptop. Think of an NPU as a specialized chip designed to run AI models super efficiently — like having a dedicated graphics card, but for AI instead of gaming.

**The Problem**: Setting up NPU support traditionally requires 12-20 minutes of compiling drivers and runtimes, often with cryptic errors.

**Our Solution**: Install everything in 40 seconds with prebuilt binaries. No compilation. No waiting. Just works.

**Who Uses This**:
- **Developers**: Building AI applications on AMD Ryzen AI hardware
- **Researchers**: Experimenting with consumer NPU capabilities
- **Makers**: Creating voice assistants, transcription tools, or TTS systems
- **Enterprises**: Deploying edge AI on Ryzen AI laptops and mini PCs

---

## 🚀 Quick Start

Install NPU support on your AMD Ryzen AI system in 3 commands:

```bash
git clone https://github.com/Unicorn-Commander/unicorn-npu-core.git
cd unicorn-npu-core
bash scripts/install-npu-host-prebuilt.sh
```

**Installation time**: 40 seconds with prebuilt binaries ⚡
**Traditional method**: 12-20 minutes of compilation ⏰

Then use it in your Python code:

```python
from unicorn_npu import NPUDevice

npu = NPUDevice()
if npu.is_available():
    print("✅ NPU is ready!")
    npu.set_power_mode("performance")  # Max performance mode
```

---

## ⚡ Why This Matters

### The NPU Opportunity

Consumer NPUs represent a paradigm shift in edge AI:
- **16+ TOPS** of INT8 performance (Phoenix NPU)
- **Ultra-low power** consumption vs. GPU inference
- **Always available** — no GPU/CPU contention
- **Dedicated hardware** for AI workloads

### What Makes This Different

#### 🎯 Prebuilt Binaries (Industry First for Consumer NPUs)

We distribute prebuilt XRT runtime packages and kernel modules, eliminating the compilation step that causes 90% of setup failures.

| Installation Method | Time | Success Rate | Dependencies Required |
|---------------------|------|--------------|----------------------|
| **Unicorn NPU Core (prebuilt)** | **40 seconds** | **~100%** | **None** |
| Traditional compilation | 12-20 minutes | ~60% | gcc, make, cmake, etc. |

**Time Saved**: 10-18 minutes per installation
**Complexity Reduced**: Zero build dependencies
**Reliability**: No compilation errors

#### 🏗️ Production-Ready Architecture

Most NPU projects are proofs-of-concept. This is production infrastructure:

- ✅ **Hardware abstraction** — Works across Phoenix, Hawk Point, Strix
- ✅ **Automatic fallback** — Builds from source if no prebuilt available
- ✅ **Power management** — Runtime performance/powersave switching
- ✅ **Zero-config ONNX** — Automatic execution provider selection
- ✅ **Comprehensive docs** — Installation, API, troubleshooting

#### 🌊 Open Source Consumer NPU Tooling

While datacenter NPUs have mature toolchains, consumer NPUs (Ryzen AI, Core Ultra) are emerging. We're building the foundation:

- Open-source runtime wrapper
- Community-driven development
- Extensible architecture for future NPU generations
- Real-world performance benchmarks

---

## 📊 Performance & Benchmarks

### Installation Speed Comparison

```
Traditional Compilation (XRT from source):
████████████████████████████████████████ 12-20 minutes

Unicorn NPU Core (prebuilt binaries):
█ 40 seconds  ⚡
```

### Real-World Application Performance

Using Unicorn NPU Core in production:

| Application | Hardware | Throughput | Latency |
|------------|----------|------------|---------|
| **Whisper STT** (base model) | Phoenix NPU | **51.2x realtime** | 23ms/chunk |
| **Kokoro TTS** (v0.19) | Phoenix NPU | **32.4x realtime** | 31ms/chunk |
| Same models | CPU (8945HS) | 4.2x realtime | 180ms/chunk |

**NPU Advantage**: 8-12x faster than CPU-only inference with 70% less power consumption.

See [Unicorn-Amanuensis](https://github.com/Unicorn-Commander/Unicorn-Amanuensis) and [Unicorn-Orator](https://github.com/Unicorn-Commander/Unicorn-Orator) for full benchmarks.

---

## 🏛️ Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                          │
│            (Whisper, Kokoro, Custom Models)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Unicorn NPU Core (This Library)                 │
├─────────────────────────────────────────────────────────────┤
│  Hardware Layer    │  Runtime Layer  │  Installation Layer  │
│  ───────────────   │  ─────────────  │  ─────────────────   │
│  • NPUDevice       │  • ONNXHelper   │  • Prebuilt XRT      │
│  • XRTRuntime      │  • Provider     │  • Kernel Modules    │
│  • Power Mgmt      │    Selection    │  • Auto-fallback     │
└────────────────────┴─────────────────┴──────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Hardware Abstraction                        │
├──────────────────┬──────────────────┬──────────────────────┤
│   XRT Runtime    │  ONNX Runtime    │   Linux Kernel       │
│   (2.20.0+)      │  (VitisAI EP)    │   (amdxdna driver)   │
└──────────────────┴──────────────────┴──────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              AMD Phoenix NPU Hardware (XDNA1)                │
│              16 TOPS INT8 @ <15W                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
unicorn-npu-core/
│
├── unicorn_npu/              # Core library
│   ├── hardware/             # Hardware abstraction
│   │   ├── npu_device.py     # NPU detection, power mgmt
│   │   └── xrt_wrapper.py    # XRT runtime wrapper
│   │
│   ├── runtime/              # Runtime utilities
│   │   └── onnx_helpers.py   # ONNX provider management
│   │
│   ├── scripts/              # Installation automation
│   │   └── install_host.py   # Python-based installer
│   │
│   └── kernels/              # Future: NPU compute kernels
│
├── scripts/                  # Bash installers
│   ├── install-npu-host-prebuilt.sh   # Smart installer
│   └── install-npu-host.sh            # Source build
│
├── releases/v1.0.0/          # Prebuilt binaries
│   ├── xrt/                  # XRT .deb packages (19MB)
│   ├── kernel-modules/       # Prebuilt amdxdna module
│   └── checksums.txt         # SHA256 verification
│
└── setup.py                  # Python package config
```

### Execution Flow

```
Application Request
       │
       ▼
┌──────────────────────┐
│  Import unicorn_npu  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐      ┌────────────────┐
│  NPU Detection       │─────▶│ Device exists? │
│  /dev/accel/accel0   │      └────┬───────────┘
└──────────────────────┘           │
                                   ▼ Yes
                          ┌─────────────────┐
                          │ XRT Available?  │
                          └────┬────────────┘
                               │
                               ▼ Yes
                     ┌──────────────────────┐
                     │  Set Power Mode      │
                     │  (D0 = Performance)  │
                     └──────┬───────────────┘
                            │
                            ▼
                  ┌──────────────────────────┐
                  │  Configure ONNX Runtime  │
                  │  Providers: VitisAI EP   │
                  └──────┬───────────────────┘
                         │
                         ▼
               ┌──────────────────────────┐
               │  Load Model on NPU       │
               │  Return Session          │
               └──────────────────────────┘
```

---

## 🎯 Key Features

### Hardware Management

#### NPU Detection & Validation
```python
from unicorn_npu import NPUDevice

npu = NPUDevice()

# Multi-method detection
if npu.is_available():
    info = npu.get_device_info()
    print(f"NPU: {info['name']}")
    print(f"Driver: {info['driver_version']}")
    print(f"Device: {info['device_path']}")
```

**Detection Methods**:
1. Direct device access (`/dev/accel/accel0`)
2. XRT runtime query (`xrt-smi examine`)
3. Kernel module verification (`lsmod | grep amdxdna`)

#### Dynamic Power Management
```python
# Switch to max performance
npu.set_power_mode("performance")  # D0 state, 16 TOPS

# Battery saver mode
npu.set_power_mode("powersave")    # D3 state, reduced power

# Check current state
state = npu.get_power_state()
print(f"Power: {state['mode']} ({state['wattage']}W)")
```

**Power Modes**:
- `performance`: D0 state, max TOPS, <15W
- `powersave`: D3 state, reduced frequency, <5W
- `default`: Balanced, auto-scaling

### Runtime Integration

#### Zero-Config ONNX Setup
```python
from unicorn_npu import ONNXHelper
import onnxruntime as ort

helper = ONNXHelper()

# Automatically selects best providers
providers = helper.get_execution_providers()
# Returns: ['VitisAIExecutionProvider', 'CPUExecutionProvider']

# Optimized session options
session_opts = helper.create_session_options(
    inter_op_threads=1,
    intra_op_threads=1
)

# Load model with NPU acceleration
session = ort.InferenceSession(
    "whisper-base.onnx",
    sess_options=session_opts,
    providers=providers
)
```

#### Provider Fallback Chain
```python
# Automatic provider selection with fallback
providers = helper.get_execution_providers(prefer_npu=True)
# Priority: VitisAI → OpenVINO → CPU

# Check what's actually available
available = helper.get_provider_info()
for provider, status in available.items():
    print(f"{provider}: {'✅' if status else '❌'}")
```

### Installation System

#### Smart Prebuilt Installer
```bash
bash scripts/install-npu-host-prebuilt.sh
```

**What it does**:
1. Detects Ubuntu version (22.04 or 24.04)
2. Downloads prebuilt XRT packages from GitHub Releases
3. Installs .deb packages (xrt-base, xrt-npu, xrt_plugin-amdxdna)
4. Loads kernel module
5. Configures permissions
6. Verifies installation

**Fallback**: If prebuilts don't match your system, automatically falls back to compilation.

#### Installation Flow

```
Start Installation
       │
       ▼
┌──────────────────────┐
│ Detect OS & Kernel   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐      ┌─────────────────┐
│ Prebuilt Available?  │─────▶│ Download from   │
│ (Ubuntu 22/24)       │ Yes  │ GitHub Releases │
└──────┬───────────────┘      └────┬────────────┘
       │ No                        │
       │                           ▼
       │                  ┌─────────────────┐
       │                  │ Install .debs   │
       │                  └────┬────────────┘
       │                       │
       ▼                       │
┌──────────────────┐          │
│ Build from source│          │
│ (10-15 min)      │          │
└──────┬───────────┘          │
       │                      │
       └──────────┬───────────┘
                  │
                  ▼
        ┌──────────────────┐
        │ Verify NPU Access│
        └──────────────────┘
```

---

## 💻 Installation

### Prerequisites

**Hardware**:
- AMD Ryzen AI processor (Phoenix, Hawk Point, or Strix Point)
- Examples: Ryzen 7 8840HS, Ryzen 9 8945HS, Ryzen AI 9 HX 370

**Software**:
- Ubuntu 22.04 or 24.04 (other distros may work but untested)
- Python 3.8 or newer
- Internet connection for prebuilt downloads

### Quick Install (Recommended)

```bash
# Clone repository
git clone https://github.com/Unicorn-Commander/unicorn-npu-core.git
cd unicorn-npu-core

# Install NPU runtime (40 seconds with prebuilts)
bash scripts/install-npu-host-prebuilt.sh

# Install Python library
pip install -e .

# Optional: Install with ONNX Runtime support
pip install -e ".[onnx]"
```

**Note**: You may need to log out and back in for group permissions to take effect.

### Manual Install (From Source)

If you prefer to compile from source or prebuilts aren't available:

```bash
git clone https://github.com/Unicorn-Commander/unicorn-npu-core.git
cd unicorn-npu-core
bash scripts/install-npu-host.sh  # Compiles XRT (12-20 min)
pip install -e .
```

### Verify Installation

```bash
# Check NPU device
ls -la /dev/accel/accel0

# Check XRT
/opt/xilinx/xrt/bin/xrt-smi examine

# Test Python library
python3 -c "from unicorn_npu import NPUDevice; print('✅ Unicorn NPU Core installed!')"
```

---

## 📚 Usage Examples

### Basic NPU Detection

```python
from unicorn_npu import NPUDevice

npu = NPUDevice()

if npu.is_available():
    print("✅ NPU is available and ready!")

    # Get detailed information
    info = npu.get_device_info()
    print(f"Device: {info['device_path']}")
    print(f"Driver: {info['driver_version']}")
    print(f"Status: {info['status']}")
else:
    print("❌ NPU not detected")
    print("Run: bash scripts/install-npu-host-prebuilt.sh")
```

### Power Management

```python
from unicorn_npu import NPUDevice

npu = NPUDevice()

# Set to maximum performance (recommended for inference)
success = npu.set_power_mode("performance")
if success:
    print("✅ NPU in max performance mode (D0)")

# Check current power state
state = npu.get_power_state()
print(f"Current mode: {state['mode']}")
print(f"Power draw: ~{state['wattage']}W")

# Switch to power saving (battery mode)
npu.set_power_mode("powersave")
```

### XRT Runtime Management

```python
from unicorn_npu import XRTRuntime

xrt = XRTRuntime()

if xrt.is_available():
    # Get XRT version
    version = xrt.get_version()
    print(f"XRT Runtime: {version}")

    # Get device status
    status = xrt.get_device_status()
    print(f"NPU Temperature: {status['temperature']}°C")
    print(f"NPU Utilization: {status['utilization']}%")

    # Get detailed device info
    info = xrt.get_device_info()
    print(f"Device ID: {info['device_id']}")
    print(f"Memory: {info['memory_mb']}MB")
```

### ONNX Runtime with NPU

```python
from unicorn_npu import ONNXHelper, NPUDevice
import onnxruntime as ort
import numpy as np

# Initialize NPU
npu = NPUDevice()
if npu.is_available():
    npu.set_power_mode("performance")

# Setup ONNX Runtime
helper = ONNXHelper()

# Get optimized providers (VitisAI for NPU)
providers = helper.get_execution_providers(prefer_npu=True)
print(f"Using: {providers}")

# Create session with NPU acceleration
session_options = helper.create_session_options()
session = ort.InferenceSession(
    "whisper-base-encoder.onnx",
    sess_options=session_options,
    providers=providers
)

# Run inference
mel_spectrogram = np.random.randn(1, 80, 3000).astype(np.float32)
outputs = session.run(None, {"mel": mel_spectrogram})

print(f"✅ Inference completed on NPU!")
print(f"Output shape: {outputs[0].shape}")
```

### Provider Detection & Fallback

```python
from unicorn_npu import ONNXHelper

helper = ONNXHelper()

# Check all available providers
provider_info = helper.get_provider_info()

print("Available Execution Providers:")
for provider, available in provider_info.items():
    status = "✅" if available else "❌"
    print(f"  {status} {provider}")

# Check specific provider
if helper.check_provider_available('VitisAIExecutionProvider'):
    print("\n🎯 NPU acceleration is ready!")
else:
    print("\n⚠️ NPU provider not available, will use CPU")

# Get providers with custom fallback
providers = helper.get_execution_providers(
    prefer_npu=True,
    fallback_to_cpu=True
)
print(f"\nProvider chain: {' → '.join(providers)}")
```

---

## 🔗 Integration with Unicorn Projects

### Unicorn-Amanuensis (Speech-to-Text)

[**Unicorn-Amanuensis**](https://github.com/Unicorn-Commander/Unicorn-Amanuensis) uses this library for NPU-accelerated Whisper transcription.

**Performance**: 51.2x realtime on AMD Ryzen 9 8945HS

```python
# In Unicorn-Amanuensis
from unicorn_npu import NPUDevice, ONNXHelper

# Initialize NPU for transcription
npu = NPUDevice()
if npu.is_available():
    npu.set_power_mode("performance")

# Configure Whisper model on NPU
helper = ONNXHelper()
encoder_session = ort.InferenceSession(
    "whisper-base-encoder.onnx",
    providers=helper.get_execution_providers()
)

decoder_session = ort.InferenceSession(
    "whisper-base-decoder.onnx",
    providers=helper.get_execution_providers()
)
```

**Add to `requirements.txt`**:
```
unicorn-npu-core @ git+https://github.com/Unicorn-Commander/unicorn-npu-core.git@v1.0.0
```

### Unicorn-Orator (Text-to-Speech)

[**Unicorn-Orator**](https://github.com/Unicorn-Commander/Unicorn-Orator) uses this library for NPU-accelerated Kokoro TTS.

**Performance**: 32.4x realtime on AMD Ryzen 9 8945HS

```python
# In Unicorn-Orator
from unicorn_npu import NPUDevice, ONNXHelper

# Initialize NPU for TTS
npu = NPUDevice()
if npu.is_available():
    npu.set_power_mode("performance")

# Configure Kokoro model on NPU
helper = ONNXHelper()
kokoro_session = ort.InferenceSession(
    "kokoro-v0_19.onnx",
    providers=helper.get_execution_providers()
)
```

**Add to `requirements.npu.txt`**:
```
unicorn-npu-core @ git+https://github.com/Unicorn-Commander/unicorn-npu-core.git@v1.0.0
```

---

## 🛠️ Development

### Development Installation

```bash
git clone https://github.com/Unicorn-Commander/unicorn-npu-core.git
cd unicorn-npu-core

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=unicorn_npu tests/

# Run specific test
pytest tests/test_npu_device.py::test_npu_detection
```

### Code Quality

```bash
# Format code
black unicorn_npu/

# Type checking
mypy unicorn_npu/

# Linting
pylint unicorn_npu/
```

### Building Prebuilt Packages

See [BUILD_PREBUILT_PACKAGES.md](releases/v1.0.0/BUILD_PREBUILT_PACKAGES.md) for instructions on creating new prebuilt binaries.

---

## 🔍 Troubleshooting

### NPU Not Detected

**Check device exists**:
```bash
ls -la /dev/accel/accel0
```

If not found:
```bash
# Check if kernel module is loaded
lsmod | grep amdxdna

# Load module manually
sudo modprobe amdxdna

# Check dmesg for errors
dmesg | grep -i xdna
```

**Check permissions**:
```bash
# Verify you're in render/video groups
groups | grep -E "(render|video)"

# If not, run installer again
bash scripts/install-npu-host-prebuilt.sh
```

### XRT Not Found

```bash
# Check if XRT is installed
ls -la /opt/xilinx/xrt/

# If not, run installer
bash scripts/install-npu-host-prebuilt.sh

# Test XRT directly
/opt/xilinx/xrt/bin/xrt-smi examine
```

### ONNX Provider Issues

**VitisAI provider not available**:

```python
import onnxruntime as ort
print(ort.get_available_providers())
# Should include 'VitisAIExecutionProvider'
```

If missing:
```bash
# Check ONNX Runtime version (need 1.22.0+)
python3 -c "import onnxruntime; print(onnxruntime.__version__)"

# Upgrade if needed
pip install --upgrade onnxruntime
```

### Performance Issues

**NPU not in performance mode**:
```python
from unicorn_npu import NPUDevice

npu = NPUDevice()
npu.set_power_mode("performance")  # Force D0 state

# Verify
state = npu.get_power_state()
print(f"Mode: {state['mode']}")  # Should be 'performance'
```

**Check NPU utilization**:
```bash
watch -n 1 '/opt/xilinx/xrt/bin/xrt-smi examine -d 0'
```

---

## 📊 System Requirements

### Supported Hardware

| Processor | NPU | TOPS (INT8) | Status |
|-----------|-----|-------------|--------|
| AMD Ryzen 7 8840HS | Phoenix (XDNA1) | 16 | ✅ Tested |
| AMD Ryzen 9 8945HS | Phoenix (XDNA1) | 16 | ✅ Tested |
| AMD Ryzen AI 9 HX 370 | Strix Point (XDNA2) | 50 | 🔄 Compatible* |
| AMD Ryzen 7 8840U | Hawk Point (XDNA1) | 16 | ✅ Compatible |

*Strix Point support via XRT 2.20+, not all features tested yet.

### Software Dependencies

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.8+ | Core library runtime |
| **XRT** | 2.20.0+ | NPU runtime (auto-installed) |
| **amdxdna** | 1.0.0+ | Kernel driver (auto-installed) |
| **ONNX Runtime** | 1.22.0+ | Model inference (optional) |

### Operating Systems

- ✅ Ubuntu 22.04 LTS (Jammy)
- ✅ Ubuntu 24.04 LTS (Noble)
- 🔄 Debian 12+ (should work, not tested)
- 🔄 Fedora 38+ (requires manual driver build)

---

## 📖 API Reference

### `NPUDevice`

Main class for NPU hardware management.

#### Methods

**`is_available() -> bool`**
Check if NPU is available and accessible.

**`get_device_info() -> dict`**
Get detailed NPU information including device path, driver version, and status.

**`set_power_mode(mode: str) -> bool`**
Set NPU power mode. Options: `"performance"`, `"powersave"`, `"default"`.

**`get_power_state() -> dict`**
Get current power state including mode and estimated wattage.

### `XRTRuntime`

XRT runtime wrapper for NPU management.

#### Methods

**`is_available() -> bool`**
Check if XRT runtime is installed and functional.

**`get_version() -> str`**
Get installed XRT version.

**`get_device_status() -> dict`**
Get NPU status including temperature and utilization.

**`get_device_info() -> dict`**
Get device information including device ID and memory.

### `ONNXHelper`

ONNX Runtime configuration helper.

#### Methods

**`get_execution_providers(prefer_npu: bool = True) -> List[str]`**
Get ordered list of execution providers. NPU (VitisAI) first if available.

**`create_session_options(**kwargs) -> ort.SessionOptions`**
Create optimized SessionOptions for NPU inference.

**`get_provider_info() -> dict`**
Get availability status of all execution providers.

**`check_provider_available(provider: str) -> bool`**
Check if specific execution provider is available.

---

## 🤝 Contributing

We welcome contributions! This library is designed to be:

- **Hardware-agnostic**: Abstract NPU differences across generations
- **Well-documented**: Every function has docstrings and examples
- **Tested**: Maintain test coverage for core functionality
- **Production-ready**: Changes should not break existing integrations

### Contribution Guidelines

1. **Fork** the repository
2. **Create a branch** for your feature (`git checkout -b feature/amazing-feature`)
3. **Add tests** for new functionality
4. **Update docs** if changing APIs
5. **Run tests** (`pytest tests/`)
6. **Commit** with clear messages
7. **Push** to your fork
8. **Open a Pull Request**

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings (Google style)
- Format with `black`

---

## 📄 License

This project is part of the [Unicorn Commander](https://unicorncommander.com) ecosystem.

**Copyright © 2025 [Magic Unicorn Unconventional Technology & Stuff Inc.](https://magicunicorn.tech)**

See [LICENSE](LICENSE) file for details.

---

## 🌐 Related Projects

Part of the **Unicorn Commander** AI acceleration ecosystem:

- **[Unicorn-Amanuensis](https://github.com/Unicorn-Commander/Unicorn-Amanuensis)** — Speech-to-Text with NPU (51x realtime)
- **[Unicorn-Orator](https://github.com/Unicorn-Commander/Unicorn-Orator)** — Text-to-Speech with NPU (32x realtime)

Visit [unicorncommander.com](https://unicorncommander.com) for the complete ecosystem.

---

## 📞 Support

**Issues & Bugs**: [GitHub Issues](https://github.com/Unicorn-Commander/unicorn-npu-core/issues)
**Company**: [Magic Unicorn Unconventional Technology & Stuff Inc.](https://magicunicorn.tech)
**Ecosystem**: [Unicorn Commander](https://unicorncommander.com)

For commercial support and consulting, visit [magicunicorn.tech](https://magicunicorn.tech).

---

## 🎯 Project Status

**Version**: 1.0.0
**Status**: Production Ready
**Last Updated**: October 2025

**Hardware Support**:
- ✅ AMD Phoenix NPU (XDNA1) — Fully tested
- ✅ AMD Hawk Point NPU (XDNA1) — Compatible
- 🔄 AMD Strix Point NPU (XDNA2) — Experimental

**Platform Support**:
- ✅ Ubuntu 22.04/24.04 — Prebuilt binaries
- 🔄 Other Linux — Source build available

---

<div align="center">

**Built with 🦄 by [Magic Unicorn Unconventional Technology & Stuff Inc.](https://magicunicorn.tech)**

Part of the [Unicorn Commander](https://unicorncommander.com) ecosystem

[Get Started](#-quick-start) • [Documentation](#-api-reference) • [Examples](#-usage-examples) • [Support](#-support)

</div>
