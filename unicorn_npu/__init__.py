"""
Unicorn NPU Core Library

Common NPU hardware access, runtime helpers, and utilities
shared across all Unicorn projects.
"""

__version__ = "1.0.0"

from .hardware.npu_device import NPUDevice
from .hardware.xrt_wrapper import XRTRuntime
from .runtime.onnx_helpers import ONNXHelper

__all__ = [
    "NPUDevice",
    "XRTRuntime",
    "ONNXHelper",
]
