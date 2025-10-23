#!/usr/bin/env python3
"""
NPU Device Detection and Management
Provides common NPU hardware access for all Unicorn projects
"""

import os
import subprocess
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class NPUDevice:
    """NPU device detection and management"""

    def __init__(self):
        """Initialize NPU device"""
        self.device_path = "/dev/accel/accel0"
        self.device_info = None
        self.available = self._detect_npu()

    def _detect_npu(self) -> bool:
        """Detect and validate NPU availability"""
        # Try direct device file access first (doesn't require XRT tools)
        if os.path.exists(self.device_path):
            try:
                # Try to open the device to verify it's accessible
                fd = os.open(self.device_path, os.O_RDWR)
                os.close(fd)
                self.device_info = {
                    'device': self.device_path,
                    'type': 'AMD Phoenix NPU',
                    'method': 'direct_device_access'
                }
                logger.info(f"✅ NPU Phoenix detected via direct device access")
                logger.info(f"Device: {self.device_path}")
                return True
            except Exception as e:
                logger.warning(f"⚠️ NPU device exists but not accessible: {e}")
                return False

        # Fallback to XRT if available
        try:
            result = subprocess.run(
                ['/opt/xilinx/xrt/bin/xrt-smi', 'examine'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and ('NPU Phoenix' in result.stdout or 'RyzenAI' in result.stdout):
                self.device_info = self._parse_xrt_info(result.stdout)
                self.device_info['method'] = 'xrt_tools'
                logger.info(f"✅ NPU Phoenix detected via XRT tools")
                logger.info(f"Device info: {self.device_info}")
                return True
            else:
                logger.error("❌ NPU Phoenix not detected")
                return False

        except subprocess.TimeoutExpired:
            logger.error("❌ XRT device detection timeout")
            return False
        except FileNotFoundError:
            logger.warning("⚠️ XRT tools not found")
            return False
        except Exception as e:
            logger.error(f"❌ NPU detection failed: {e}")
            return False

    def _parse_xrt_info(self, xrt_output: str) -> Dict[str, Any]:
        """Parse XRT device information"""
        info = {'device': self.device_path}

        for line in xrt_output.split('\n'):
            line = line.strip()
            if 'Device' in line and '[' in line:
                # Extract PCI address
                start = line.find('[')
                end = line.find(']')
                if start != -1 and end != -1:
                    info['pci_address'] = line[start+1:end]
            elif 'Firmware' in line and ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    info['firmware'] = parts[1].strip()
            elif 'Type' in line and ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    info['type'] = parts[1].strip()

        return info

    def is_available(self) -> bool:
        """Check if NPU is available"""
        return self.available

    def get_device_info(self) -> Dict[str, Any]:
        """Get NPU device information"""
        if not self.available:
            return {"status": "not available"}
        return self.device_info

    def set_power_mode(self, mode: str = "performance") -> bool:
        """Set NPU power mode (performance/powersave/default)"""
        if not self.available:
            logger.error("❌ NPU not available")
            return False

        try:
            # Find xrt-smi (may be in different locations)
            xrt_smi_paths = [
                '/opt/xilinx/xrt/bin/xrt-smi',
                '/opt/xilinx/xrt/bin/unwrapped/xrt-smi'
            ]

            xrt_smi = None
            for path in xrt_smi_paths:
                if os.path.exists(path):
                    xrt_smi = path
                    break

            if not xrt_smi:
                logger.error("❌ xrt-smi not found")
                return False

            # Get PCI address if we have it
            pci_address = self.device_info.get('pci_address', '0000:c7:00.1')

            # Set power mode
            result = subprocess.run(
                ['sudo', xrt_smi, 'configure', '--device', pci_address, '--pmode', mode],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logger.info(f"✅ NPU power mode set to: {mode}")
                return True
            else:
                logger.error(f"❌ Failed to set power mode: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to set NPU power mode: {e}")
            return False

    def get_power_state(self) -> Optional[str]:
        """Get current NPU power state"""
        if not self.available:
            return None

        try:
            xrt_smi = '/opt/xilinx/xrt/bin/xrt-smi'
            if not os.path.exists(xrt_smi):
                xrt_smi = '/opt/xilinx/xrt/bin/unwrapped/xrt-smi'

            if not os.path.exists(xrt_smi):
                return None

            result = subprocess.run(
                [xrt_smi, 'examine'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                # Parse power state from output
                for line in result.stdout.split('\n'):
                    if 'Power' in line or 'D0' in line or 'D3' in line:
                        if 'D0' in line:
                            return 'D0 (full performance)'
                        elif 'D3' in line:
                            return 'D3hot (low power)'

            return "Unknown"

        except Exception as e:
            logger.error(f"❌ Failed to get power state: {e}")
            return None
