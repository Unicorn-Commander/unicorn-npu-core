#!/usr/bin/env python3
"""
XRT Runtime Wrapper
Provides simplified interface to XRT for NPU operations
"""

import os
import subprocess
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class XRTRuntime:
    """XRT Runtime wrapper for NPU operations"""

    def __init__(self):
        """Initialize XRT runtime"""
        self.xrt_available = False
        self._setup_environment()
        self._check_xrt()

    def _setup_environment(self):
        """Set up XRT environment variables"""
        xrt_setup = "/opt/xilinx/xrt/setup.sh"

        if os.path.exists(xrt_setup):
            try:
                # Source XRT environment
                env_vars = subprocess.run(
                    f"source {xrt_setup} && env",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if env_vars.returncode == 0:
                    for line in env_vars.stdout.split('\n'):
                        if '=' in line and any(x in line for x in ['XRT', 'XILINX']):
                            key, value = line.split('=', 1)
                            os.environ[key] = value
                    logger.info("✅ XRT environment configured")
                else:
                    logger.warning("⚠️ XRT environment setup failed")
            except Exception as e:
                logger.warning(f"⚠️ Failed to setup XRT environment: {e}")

    def _check_xrt(self):
        """Check if XRT is available"""
        try:
            result = subprocess.run(
                ['/opt/xilinx/xrt/bin/xrt-smi', 'version'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                self.xrt_available = True
                logger.info("✅ XRT runtime available")
            else:
                logger.warning("⚠️ XRT not available")

        except (FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("⚠️ XRT tools not found")
        except Exception as e:
            logger.warning(f"⚠️ XRT check failed: {e}")

    def is_available(self) -> bool:
        """Check if XRT is available"""
        return self.xrt_available

    def get_version(self) -> Optional[str]:
        """Get XRT version"""
        if not self.xrt_available:
            return None

        try:
            result = subprocess.run(
                ['/opt/xilinx/xrt/bin/xrt-smi', 'version'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                # Parse version from output
                for line in result.stdout.split('\n'):
                    if 'Version' in line or 'xrt' in line.lower():
                        return line.strip()

            return "Unknown"

        except Exception as e:
            logger.error(f"❌ Failed to get XRT version: {e}")
            return None

    def get_device_status(self) -> Optional[Dict[str, Any]]:
        """Get NPU device status via XRT"""
        if not self.xrt_available:
            return None

        try:
            result = subprocess.run(
                ['/opt/xilinx/xrt/bin/xrt-smi', 'examine'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                status = {
                    'online': True,
                    'raw_output': result.stdout
                }

                # Parse key information
                for line in result.stdout.split('\n'):
                    if 'Temperature' in line:
                        status['temperature'] = line.strip()
                    elif 'Power' in line:
                        status['power'] = line.strip()
                    elif 'Firmware' in line:
                        status['firmware'] = line.strip()

                return status
            else:
                return {'online': False, 'error': result.stderr}

        except Exception as e:
            logger.error(f"❌ Failed to get device status: {e}")
            return None
