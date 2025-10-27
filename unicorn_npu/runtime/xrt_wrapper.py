"""
XRT Python Wrapper for NPU Access
Provides simplified interface to AMD XRT for NPU acceleration
"""
import sys
import os
from pathlib import Path
from typing import Optional, Union

# Add XRT Python bindings to path
XRT_PYTHON_PATH = "/opt/xilinx/xrt/python"
if XRT_PYTHON_PATH not in sys.path:
    sys.path.insert(0, XRT_PYTHON_PATH)

try:
    import pyxrt as xrt
    XRT_AVAILABLE = True
except ImportError:
    xrt = None
    XRT_AVAILABLE = False


class NPUDevice:
    """Wrapper for AMD Phoenix NPU access via XRT"""

    def __init__(self, device_index: int = 0):
        """
        Initialize NPU device

        Args:
            device_index: NPU device index (default: 0 for /dev/accel/accel0)
        """
        if not XRT_AVAILABLE:
            raise RuntimeError(
                "XRT Python bindings not available. "
                f"Expected at: {XRT_PYTHON_PATH}"
            )

        self.device_index = device_index
        self.device = None
        self.xclbin_uuid = None
        self._open_device()

    def _open_device(self):
        """Open NPU device"""
        try:
            self.device = xrt.device(self.device_index)
            print(f"✅ NPU device {self.device_index} opened successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to open NPU device {self.device_index}: {e}")

    def load_xclbin(self, xclbin_path: Union[str, Path]) -> str:
        """
        Load XCLBIN file onto NPU

        Args:
            xclbin_path: Path to XCLBIN file

        Returns:
            UUID of loaded XCLBIN
        """
        xclbin_path = str(xclbin_path)

        if not os.path.exists(xclbin_path):
            raise FileNotFoundError(f"XCLBIN not found: {xclbin_path}")

        try:
            self.xclbin_uuid = self.device.load_xclbin(xclbin_path)
            print(f"✅ XCLBIN loaded successfully")
            print(f"   UUID: {self.xclbin_uuid}")
            return str(self.xclbin_uuid)
        except Exception as e:
            raise RuntimeError(f"Failed to load XCLBIN: {e}")

    def allocate_bo(self, size: int):
        """
        Allocate buffer object on NPU

        Args:
            size: Buffer size in bytes

        Returns:
            Buffer object
        """
        if self.device is None:
            raise RuntimeError("Device not opened")

        return xrt.bo(self.device, size, xrt.bo.normal, 0)

    def close(self):
        """Close NPU device"""
        if self.device:
            self.device = None
            print("✅ NPU device closed")


class XCLBINLoader:
    """Helper for loading and managing XCLBIN files"""

    @staticmethod
    def validate_xclbin(xclbin_path: Union[str, Path]) -> dict:
        """
        Validate and inspect XCLBIN file

        Args:
            xclbin_path: Path to XCLBIN file

        Returns:
            Dictionary with XCLBIN metadata
        """
        xclbin_path = Path(xclbin_path)

        if not xclbin_path.exists():
            return {
                "valid": False,
                "error": f"File not found: {xclbin_path}"
            }

        info = {
            "valid": True,
            "path": str(xclbin_path),
            "size": xclbin_path.stat().st_size,
            "exists": True
        }

        # TODO: Add xclbinutil inspection if available
        # This would require calling xclbinutil --info

        return info

    @staticmethod
    def find_xclbin(search_dir: Union[str, Path], pattern: str = "*.xclbin") -> list:
        """
        Find XCLBIN files in directory

        Args:
            search_dir: Directory to search
            pattern: Glob pattern for XCLBIN files

        Returns:
            List of paths to XCLBIN files
        """
        search_dir = Path(search_dir)
        return list(search_dir.glob(pattern))


def check_xrt_available() -> bool:
    """Check if XRT Python bindings are available"""
    return XRT_AVAILABLE


def get_xrt_version() -> Optional[str]:
    """Get XRT version if available"""
    if not XRT_AVAILABLE:
        return None

    try:
        # XRT doesn't always expose version via Python
        # Try to get it from xrt-smi
        import subprocess
        result = subprocess.run(
            ["/opt/xilinx/xrt/bin/xrt-smi", "version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'Version' in line:
                    return line.split(':')[-1].strip()
        return "Unknown (available)"
    except Exception:
        return "Unknown (available)"


# Module-level convenience functions
def open_npu(device_index: int = 0) -> NPUDevice:
    """
    Convenience function to open NPU device

    Args:
        device_index: NPU device index

    Returns:
        NPUDevice instance
    """
    return NPUDevice(device_index)


__all__ = [
    'NPUDevice',
    'XCLBINLoader',
    'check_xrt_available',
    'get_xrt_version',
    'open_npu',
    'XRT_AVAILABLE'
]
