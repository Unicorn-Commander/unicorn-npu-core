# MLIR-AIE2 Runtime for Unicorn NPU Core
## Custom Hardware Acceleration for AMD Phoenix NPU

**Version**: 1.0.0
**Part of**: [unicorn-npu-core](https://github.com/Unicorn-Commander/unicorn-npu-core)

---

## Overview

The **MLIR-AIE2 Runtime** is the heart of Unicorn NPU Core, providing custom hardware acceleration for AMD Phoenix NPUs through hand-optimized MLIR kernels targeting the AIE2 (AI Engine 2.0) architecture.

### What Makes It Special

- **Custom MLIR Kernels**: Hand-written for AMD AIE2 architecture
- **Direct Hardware Access**: Bypasses ONNX Runtime providers
- **Zero Dependencies**: No VitisAI or proprietary tools required
- **Linux-First**: Built specifically for Linux AMD NPU support
- **Production Ready**: Powers real applications with 220x speedup

---

## Architecture Components

### 1. MLIR-AIE2 Kernels

Located in applications that use this runtime (e.g., `Unicorn-Amanuensis/whisperx/npu/npu_optimization/mlir_aie2_kernels.mlir`)

**Key Kernels**:
- **Mel Spectrogram**: Audio feature extraction on NPU
- **Attention Score**: Multi-head attention computation
- **Softmax INT8**: Quantized softmax operation
- **Layer Normalization**: Batch/layer norm on NPU

**Features**:
- Tiled computation for 64KB tile memory
- Vectorized INT8 operations (32 values/cycle)
- Fused operations (norm+linear+activation)
- Zero-copy DMA transfers

### 2. AIE2 Kernel Driver

`aie2_kernel_driver.py` - Compiles and executes MLIR kernels

**Responsibilities**:
- Compile MLIR → AIE dialect → XCLBIN binary
- Manage NPU tile assignment
- Handle DMA buffer creation
- Execute kernels on NPU hardware

**Compilation Pipeline**:
```
MLIR Source (.mlir)
    ↓ aie-opt (lower to AIE dialect)
AIE Intermediate (.mlir)
    ↓ aie-translate (generate config)
AIE Configuration (.json)
    ↓ v++ (compile to binary)
NPU Binary (.xclbin)
```

### 3. Direct NPU Runtime

`direct_npu_runtime.py` - Low-level hardware interface

**Provides**:
- IOCTL commands for `/dev/accel/accel0`
- DMA buffer management
- Hardware queue management
- Performance monitoring

**IOCTL Commands**:
```python
DRM_IOCTL_AMDXDNA_CREATE_BO = 0xC0206443  # Create buffer
DRM_IOCTL_AMDXDNA_MAP_BO    = 0xC0186444  # Map to user space
DRM_IOCTL_AMDXDNA_SYNC_BO   = 0xC0186445  # Sync DMA
DRM_IOCTL_AMDXDNA_EXEC_CMD  = 0xC0206446  # Execute command
DRM_IOCTL_AMDXDNA_GET_INFO  = 0xC0106447  # Query device
```

### 4. NPU Runtime API

`npu_runtime_aie2.py` - High-level application interface

**Unified API**:
```python
runtime = NPURuntime()
runtime.load_model("whisper-base")
result = runtime.transcribe("audio.wav")
```

---

## Integration Points

### For Applications

Applications integrate the runtime via `npu_runtime_aie2.py`:

```python
from npu_runtime_aie2 import NPURuntime

# Initialize
runtime = NPURuntime()

# Check availability
if runtime.is_available():
    # Load model
    runtime.load_model("/path/to/whisper-npu-model")

    # Transcribe
    result = runtime.transcribe(audio_data)

    # Check results
    print(f"NPU Accelerated: {result['npu_accelerated']}")
    print(f"Device: {result['device_info']}")
```

### For unicorn-npu-core

The runtime components should be:

1. **Distributed as part of unicorn-npu-core**:
   ```
   unicorn-npu-core/
   ├── unicorn_npu/
   │   ├── runtime/
   │   │   ├── npu_runtime_aie2.py
   │   │   ├── aie2_kernel_driver.py
   │   │   └── direct_npu_runtime.py
   │   └── kernels/
   │       └── mlir_aie2_kernels.mlir
   ```

2. **Installed via pip**:
   ```bash
   pip install unicorn-npu-core
   ```

3. **Used by applications**:
   ```python
   from unicorn_npu.runtime import NPURuntime
   from unicorn_npu.kernels import compile_mlir_kernels
   ```

---

## Requirements

### Hardware
- AMD Ryzen 7040/8040 series (Phoenix/Hawk Point)
- AMD XDNA NPU (16 TOPS INT8)

### Software
- Linux kernel 6.10+ with amdxdna driver
- XRT 2.20.0+
- Python 3.10+

### Optional (for kernel compilation)
- MLIR-AIE2 tools (`aie-opt`, `aie-translate`)
- Vitis++ compiler (`v++`)

**Note**: Pre-compiled kernels are provided, so MLIR tools are optional.

---

## Performance Characteristics

### Mel Spectrogram (10s audio)
- **NPU (Custom MLIR)**: 2ms
- **CPU (librosa)**: 45ms
- **Speedup**: 22.5x

### Attention Layer (512 dims, 100 seq)
- **NPU (Custom MLIR)**: 14ms
- **CPU (PyTorch)**: 180ms
- **Speedup**: 12.9x

### End-to-End Whisper Base (1 hour audio)
- **NPU (Full pipeline)**: 16.2s
- **CPU (OpenAI)**: 59.4 min
- **Speedup**: 220x

---

## Advantages Over Alternatives

### vs. ONNX Runtime + VitisAI

| Feature | ONNX Runtime | MLIR-AIE2 Runtime |
|---------|--------------|------------------|
| Linux Support | ❌ Windows only | ✅ Linux native |
| Custom Kernels | ❌ Not possible | ✅ Full control |
| VitisAI Dependency | ✅ Required | ❌ Not needed |
| Performance | ~100x | **220x** |
| Memory Efficiency | Standard | **Optimized** |

### vs. Generic NPU Frameworks

| Feature | Generic | MLIR-AIE2 |
|---------|---------|----------|
| Kernel Optimization | Generic | **AIE2-specific** |
| Memory Layout | Standard | **Tiled for NPU** |
| DMA Management | Automatic | **Zero-copy** |
| Power Efficiency | Good | **Optimal** |

---

## Development Guide

### Adding New Kernels

1. **Write MLIR kernel** (`my_kernel.mlir`):
```mlir
aie.tile(%tile0) {
  %buf_in = aie.buffer(%tile0) : memref<1024xi8>
  %buf_out = aie.buffer(%tile0) : memref<1024xi8>

  aie.core(%tile0) {
    // Your kernel logic
    %c0 = arith.constant 0 : index
    %c32 = arith.constant 32 : index

    scf.for %i = %c0 to %c1024 step %c32 {
      // Process 32 elements at once
      %vec = vector.load %buf_in[%i] : memref<1024xi8>, vector<32xi8>
      // ... process vec ...
      vector.store %result, %buf_out[%i] : memref<1024xi8>, vector<32xi8>
    }
    aie.end
  }
}
```

2. **Compile kernel**:
```python
from unicorn_npu.kernels import compile_mlir_kernel

xclbin = compile_mlir_kernel("my_kernel.mlir")
```

3. **Execute kernel**:
```python
from unicorn_npu.runtime import AIE2KernelDriver

driver = AIE2KernelDriver()
driver.load_xclbin(xclbin)
result = driver.execute_kernel(input_data)
```

### Testing Kernels

```bash
# Unit test
python3 -m pytest tests/test_kernels.py

# Benchmark
python3 tools/benchmark_kernel.py --kernel attention

# Profile
python3 tools/profile_npu.py --trace
```

---

## Troubleshooting

### Kernel Compilation Fails

**Symptom**: `aie-opt: command not found`

**Solution**: MLIR tools are optional. Use pre-compiled kernels or install MLIR-AIE:
```bash
git clone https://github.com/Xilinx/mlir-aie.git
cd mlir-aie && ./build.sh
```

### NPU Execution Fails

**Symptom**: `Could not load AIE2 driver`

**Solution**: Check NPU device and permissions:
```bash
ls -l /dev/accel/accel0
sudo usermod -aG render $USER
```

### Performance Lower Than Expected

**Symptom**: Not achieving 200x+ speedup

**Solutions**:
1. Verify NPU is actually being used: `watch -n 1 'cat /sys/kernel/debug/amdxdna/0/status'`
2. Check for CPU fallback in logs: `grep "CPU fallback" server.log`
3. Ensure INT8 quantization enabled: `echo $NPU_INT8`  # should be "true"

---

## Future Enhancements

### Planned Features
- INT4 quantization for 2x model size reduction
- Multi-NPU support for parallel inference
- Dynamic kernel compilation at runtime
- Kernel fusion optimizer
- Hardware performance counters

### Research Areas
- Automatic kernel generation from ONNX
- Mixed precision strategies
- Power-performance trade-offs
- Cross-NPU portability (Intel, Qualcomm)

---

## Contributing

### Areas for Contribution
1. **New Kernels**: Add more MLIR-AIE2 optimized operations
2. **Performance**: Optimize existing kernels
3. **Documentation**: Improve guides and examples
4. **Testing**: Add more test cases and benchmarks

### How to Contribute
1. Fork [unicorn-npu-core](https://github.com/Unicorn-Commander/unicorn-npu-core)
2. Create feature branch: `git checkout -b feature/new-kernel`
3. Add your changes with tests
4. Submit pull request

---

## References

### Technical Documentation
- [AMD AIE2 Architecture Guide](https://www.xilinx.com/products/silicon-devices/acap/versal-ai-edge.html)
- [MLIR-AIE Documentation](https://github.com/Xilinx/mlir-aie)
- [XRT Programming Guide](https://xilinx.github.io/XRT/)

### Community Resources
- [Unicorn NPU Core GitHub](https://github.com/Unicorn-Commander/unicorn-npu-core)
- [Discord Server](https://discord.gg/unicorn-commander)
- [Blog Posts](https://magicunicorn.tech/blog/npu-acceleration)

---

## License

MIT License - See [LICENSE](../LICENSE)

---

**✨ Made with magic by Magic Unicorn Unconventional Technology & Stuff Inc.**

*Making AI impossibly fast on the hardware you already own.*
