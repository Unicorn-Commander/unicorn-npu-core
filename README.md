# Unicorn NPU Core

Core NPU library for Unicorn projects providing hardware access, runtime helpers, and utilities for AMD Phoenix NPU (XDNA1) acceleration.

## Overview

This library provides common NPU functionality shared across all Unicorn projects:

- **Hardware Access**: NPU device detection, XRT runtime wrapper
- **Runtime Helpers**: ONNX Runtime configuration with execution provider selection
- **Installation Scripts**: Automated host system setup for NPU support
- **Utilities**: Profiling, diagnostics, and monitoring (coming soon)

## Features

- 🔍 **Automatic NPU Detection**: Detects AMD Phoenix NPU via direct device access or XRT tools
- ⚡ **Power Management**: Set NPU power modes (performance/powersave/default)
- 🔧 **XRT Integration**: Simplified XRT runtime wrapper
- 🧠 **ONNX Runtime Support**: Automatic execution provider selection (VitisAI, OpenVINO, CPU)
- 📦 **Easy Installation**: Automated host system setup script
- 🦄 **Unicorn Ready**: Designed for Unicorn-Amanuensis, Unicorn-Orator, and other projects

## Installation

### From Local Directory (Development)

```bash
cd /home/ucadmin/UC-1/unicorn-npu-core
pip install -e .
```

### With ONNX Runtime Support

```bash
pip install -e ".[onnx]"
```

### With OpenVINO Support

```bash
pip install -e ".[openvino]"
```

## Host System Setup

To install NPU drivers and XRT runtime on the host system:

```bash
# Using Python
python3 -m unicorn_npu.scripts.install_host

# Or directly
cd /home/ucadmin/UC-1/unicorn-npu-core
bash scripts/install-npu-host.sh
```

**Note**: After installation, log out and log back in for group changes to take effect.

## Usage

### Basic NPU Detection

```python
from unicorn_npu import NPUDevice

# Create NPU device instance
npu = NPUDevice()

# Check if NPU is available
if npu.is_available():
    print("✅ NPU detected!")
    print(f"Device info: {npu.get_device_info()}")
else:
    print("❌ NPU not available")
```

### Set NPU Power Mode

```python
from unicorn_npu import NPUDevice

npu = NPUDevice()

if npu.is_available():
    # Set to performance mode (D0)
    npu.set_power_mode("performance")

    # Check current power state
    state = npu.get_power_state()
    print(f"NPU power state: {state}")
```

### XRT Runtime

```python
from unicorn_npu import XRTRuntime

# Create XRT runtime instance
xrt = XRTRuntime()

if xrt.is_available():
    print(f"XRT version: {xrt.get_version()}")

    # Get device status
    status = xrt.get_device_status()
    print(f"Device status: {status}")
```

### ONNX Runtime Helpers

```python
from unicorn_npu import ONNXHelper
import onnxruntime as ort

# Create ONNX helper
helper = ONNXHelper()

# Get execution providers (prioritizes NPU)
providers = helper.get_execution_providers()
print(f"Using providers: {providers}")

# Create session with optimized settings
session_options = helper.create_session_options(
    inter_op_threads=1,
    intra_op_threads=1
)

# Load model with NPU support
session = ort.InferenceSession(
    "model.onnx",
    sess_options=session_options,
    providers=providers
)
```

### Check Provider Information

```python
from unicorn_npu import ONNXHelper

helper = ONNXHelper()

# Get all provider info
info = helper.get_provider_info()
print(f"Available providers: {info}")

# Check specific provider
if helper.check_provider_available('VitisAIExecutionProvider'):
    print("✅ AMD Ryzen AI NPU provider available")
```

## Integration with Unicorn Projects

### Unicorn-Amanuensis (STT)

Add to `requirements.txt`:
```
unicorn-npu-core @ file:///home/ucadmin/UC-1/unicorn-npu-core
```

Or for GitHub:
```
unicorn-npu-core @ git+https://github.com/Unicorn-Commander/unicorn-npu-core.git
```

Use in code:
```python
from unicorn_npu import NPUDevice, ONNXHelper

# Initialize NPU
npu = NPUDevice()
if npu.is_available():
    npu.set_power_mode("performance")

# Configure ONNX Runtime for Whisper
helper = ONNXHelper()
providers = helper.get_execution_providers()

# Create Whisper session with NPU
session = ort.InferenceSession(
    "whisper_model.onnx",
    providers=providers
)
```

### Unicorn-Orator (TTS)

Similar integration pattern for Kokoro TTS models.

## Architecture

```
unicorn-npu-core/
├── unicorn_npu/
│   ├── __init__.py           # Main package exports
│   ├── hardware/             # Hardware access layer
│   │   ├── npu_device.py     # NPU detection & management
│   │   └── xrt_wrapper.py    # XRT runtime wrapper
│   ├── runtime/              # Runtime helpers
│   │   └── onnx_helpers.py   # ONNX Runtime utilities
│   ├── kernels/              # NPU compute kernels (future)
│   ├── utils/                # Utilities (future)
│   └── scripts/              # Installation scripts
│       └── install_host.py   # Host setup automation
├── scripts/
│   └── install-npu-host.sh   # NPU host installation
├── tests/                    # Unit tests
├── setup.py                  # Package configuration
└── README.md                 # This file
```

## Requirements

### Hardware
- AMD Ryzen AI processor with Phoenix NPU (XDNA1)
- Device: `/dev/accel/accel0`

### Software
- Python >= 3.8
- XRT Runtime 2.20.0+ (installed via `install-npu-host.sh`)
- Optional: onnxruntime >= 1.22.0

### Operating System
- Linux (Ubuntu 22.04+ recommended)
- Kernel with amdxdna driver support

## Development

### Install in Development Mode

```bash
cd /home/ucadmin/UC-1/unicorn-npu-core
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black unicorn_npu/
```

## Performance

- NPU Detection: < 100ms
- Power Mode Switch: < 2 seconds
- XRT Runtime Initialization: < 500ms
- ONNX Session Creation: Varies by model size

## Troubleshooting

### NPU Not Detected

1. Check device exists:
   ```bash
   ls -la /dev/accel/accel0
   ```

2. Verify permissions:
   ```bash
   groups | grep -E "(render|video)"
   ```

3. Check XRT installation:
   ```bash
   /opt/xilinx/xrt/bin/xrt-smi examine
   ```

### XRT Not Found

Run host installation:
```bash
bash scripts/install-npu-host.sh
```

### ONNX Provider Issues

Check available providers:
```python
import onnxruntime as ort
print(ort.get_available_providers())
```

Install specific provider:
```bash
pip install onnxruntime-openvino  # For OpenVINO
```

## Contributing

This library is part of the Unicorn Commander ecosystem. When adding new features:

1. Keep code hardware-agnostic where possible
2. Add type hints and docstrings
3. Update tests
4. Follow existing code style

## License

Part of the Unicorn Commander project.

## Related Projects

- **Unicorn-Amanuensis**: Speech-to-Text with NPU acceleration
- **Unicorn-Orator**: Text-to-Speech with NPU acceleration
- **Unicorn-Execution-Engine**: LLM inference with NPU
- **whisper_npu_project**: Unicorn Commander GUI (51x realtime!)
- **amd-npu-utils**: NPU development toolkit

## Support

For issues related to:
- NPU hardware: Check AMD Ryzen AI documentation
- XRT runtime: Check Xilinx XRT documentation
- This library: Create an issue in the repository

---

**Status**: Production Ready v1.0.0
**Hardware**: AMD Phoenix NPU (XDNA1)
**Performance**: Optimized for real-time AI inference
