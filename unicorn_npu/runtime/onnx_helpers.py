#!/usr/bin/env python3
"""
ONNX Runtime Helpers
Common utilities for ONNX Runtime configuration and execution
"""

import os
import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)


class ONNXHelper:
    """Helper class for ONNX Runtime configuration"""

    def __init__(self):
        """Initialize ONNX helper"""
        self.cpu_only_mode = os.environ.get('CPU_ONLY_MODE', '').lower() in ('1', 'true', 'yes')

    def get_execution_providers(self, prefer_npu: bool = True) -> List[str]:
        """
        Get list of execution providers in priority order

        Args:
            prefer_npu: If True, prioritize NPU-related providers

        Returns:
            List of execution provider names
        """
        if self.cpu_only_mode:
            logger.info("🖥️ CPU-only mode enabled")
            return ['CPUExecutionProvider']

        try:
            import onnxruntime as ort
            available = ort.get_available_providers()
            logger.info(f"📋 Available ONNX providers: {available}")

            providers = []

            # Priority order for NPU/GPU providers
            priority_providers = [
                'VitisAIExecutionProvider',  # AMD Ryzen AI NPU
                'OpenVINOExecutionProvider',  # Intel iGPU/NPU
                'CUDAExecutionProvider',      # NVIDIA GPU
                'ROCmExecutionProvider',      # AMD GPU
                'DmlExecutionProvider',       # DirectML (Windows)
            ]

            # Add available providers in priority order
            for provider in priority_providers:
                if provider in available:
                    providers.append(provider)
                    logger.info(f"✅ Using {provider}")

            # Always add CPU as fallback
            providers.append('CPUExecutionProvider')

            return providers

        except ImportError:
            logger.error("❌ onnxruntime not installed")
            return ['CPUExecutionProvider']
        except Exception as e:
            logger.error(f"❌ Failed to get execution providers: {e}")
            return ['CPUExecutionProvider']

    def create_session_options(self,
                               inter_op_threads: int = 1,
                               intra_op_threads: int = 1,
                               enable_profiling: bool = False) -> Any:
        """
        Create ONNX Runtime session options

        Args:
            inter_op_threads: Number of threads for inter-op parallelism
            intra_op_threads: Number of threads for intra-op parallelism
            enable_profiling: Enable profiling

        Returns:
            SessionOptions object
        """
        try:
            import onnxruntime as ort

            options = ort.SessionOptions()
            options.inter_op_num_threads = inter_op_threads
            options.intra_op_num_threads = intra_op_threads

            if enable_profiling:
                options.enable_profiling = True

            # Optimize for inference
            options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

            return options

        except ImportError:
            logger.error("❌ onnxruntime not installed")
            return None
        except Exception as e:
            logger.error(f"❌ Failed to create session options: {e}")
            return None

    def check_provider_available(self, provider_name: str) -> bool:
        """
        Check if a specific execution provider is available

        Args:
            provider_name: Name of the execution provider

        Returns:
            True if available, False otherwise
        """
        try:
            import onnxruntime as ort
            return provider_name in ort.get_available_providers()
        except ImportError:
            return False
        except Exception as e:
            logger.error(f"❌ Failed to check provider: {e}")
            return False

    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about available execution providers

        Returns:
            Dictionary with provider information
        """
        info = {
            'cpu_only_mode': self.cpu_only_mode,
            'providers': []
        }

        try:
            import onnxruntime as ort

            available = ort.get_available_providers()

            for provider in available:
                provider_info = {
                    'name': provider,
                    'available': True
                }

                # Add specific info for known providers
                if provider == 'VitisAIExecutionProvider':
                    provider_info['description'] = 'AMD Ryzen AI NPU'
                elif provider == 'OpenVINOExecutionProvider':
                    provider_info['description'] = 'Intel OpenVINO (CPU/iGPU/NPU)'
                elif provider == 'CUDAExecutionProvider':
                    provider_info['description'] = 'NVIDIA CUDA GPU'
                elif provider == 'ROCmExecutionProvider':
                    provider_info['description'] = 'AMD ROCm GPU'
                elif provider == 'CPUExecutionProvider':
                    provider_info['description'] = 'CPU execution'

                info['providers'].append(provider_info)

            return info

        except ImportError:
            info['error'] = 'onnxruntime not installed'
            return info
        except Exception as e:
            info['error'] = str(e)
            return info
