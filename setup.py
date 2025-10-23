#!/usr/bin/env python3
"""
Unicorn NPU Core - Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README if it exists
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text()

setup(
    name="unicorn-npu-core",
    version="1.0.0",
    author="Unicorn Commander Team",
    author_email="noreply@unicorn.local",
    description="Core NPU library for Unicorn projects - hardware access, runtime helpers, and utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Unicorn-Commander/unicorn-npu-core",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
    ],
    extras_require={
        "onnx": [
            "onnxruntime>=1.22.0",
        ],
        "openvino": [
            "onnxruntime-openvino>=1.23.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "npu-detect=unicorn_npu.utils.detect:main",
        ],
    },
    include_package_data=True,
    package_data={
        "unicorn_npu": [
            "scripts/*.sh",
            "scripts/*.py",
        ],
    },
)
