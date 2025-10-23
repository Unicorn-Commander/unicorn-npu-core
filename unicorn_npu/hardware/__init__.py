"""NPU hardware access modules"""

from .npu_device import NPUDevice
from .xrt_wrapper import XRTRuntime

__all__ = ["NPUDevice", "XRTRuntime"]
