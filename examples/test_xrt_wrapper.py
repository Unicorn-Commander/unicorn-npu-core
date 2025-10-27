#!/usr/bin/env python3
"""
Example usage of XRT wrapper for NPU access
Tests basic XRT functionality with unicorn-npu-core
"""
from unicorn_npu.runtime.xrt_wrapper import (
    check_xrt_available,
    get_xrt_version,
    NPUDevice,
    XCLBINLoader
)

def main():
    print("=" * 70)
    print("UNICORN-NPU-CORE: XRT Wrapper Test")
    print("=" * 70 + "\n")

    # Check if XRT is available
    print("1. Checking XRT availability...")
    if check_xrt_available():
        print("   ✅ XRT Python bindings available")
        version = get_xrt_version()
        print(f"   Version: {version}\n")
    else:
        print("   ❌ XRT Python bindings not available")
        print("   Install XRT 2.20.0+ for NPU support\n")
        return 1

    # Open NPU device
    print("2. Opening NPU device...")
    try:
        npu = NPUDevice(device_index=0)
        print("   ✅ NPU device opened successfully\n")
    except Exception as e:
        print(f"   ❌ Failed to open NPU: {e}\n")
        return 1

    # Try to load XCLBIN (example)
    print("3. XCLBIN loading test...")
    xclbin_path = "/path/to/your.xclbin"  # Update with actual path

    xclbin_info = XCLBINLoader.validate_xclbin(xclbin_path)
    if xclbin_info["valid"] and xclbin_info["exists"]:
        print(f"   ✅ XCLBIN found: {xclbin_path}")
        print(f"   Size: {xclbin_info['size']} bytes")

        try:
            uuid = npu.load_xclbin(xclbin_path)
            print(f"   ✅ XCLBIN loaded successfully!")
            print(f"   UUID: {uuid}\n")
        except Exception as e:
            print(f"   ⚠️  XCLBIN loading failed: {e}")
            print("   (This is expected if XCLBIN is missing metadata)\n")
    else:
        print(f"   ℹ️  No XCLBIN specified for testing")
        print("   Update xclbin_path in this script to test loading\n")

    # Close device
    npu.close()

    print("=" * 70)
    print("✅ XRT Wrapper Test Complete!")
    print("=" * 70)
    print("\nUnicorn-NPU-Core is ready for NPU acceleration!")
    print("See documentation for integrating with your models.\n")

    return 0


if __name__ == "__main__":
    exit(main())
