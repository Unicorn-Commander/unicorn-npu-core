#!/usr/bin/env python3
"""
Host System NPU Setup
Callable from any Unicorn project for automated NPU installation
"""

import os
import subprocess
import sys
from pathlib import Path


def get_script_path() -> Path:
    """Get path to install-npu-host.sh"""
    # Get the directory containing this Python file
    this_dir = Path(__file__).parent.parent.parent
    script_path = this_dir / "scripts" / "install-npu-host.sh"

    if not script_path.exists():
        # Try alternative location (installed package)
        import unicorn_npu
        package_dir = Path(unicorn_npu.__file__).parent.parent
        script_path = package_dir / "scripts" / "install-npu-host.sh"

    return script_path


def main():
    """Run NPU host installation"""
    print("🦄 Unicorn NPU Core - Host System Setup")
    print("=" * 50)

    script_path = get_script_path()

    if not script_path.exists():
        print(f"❌ Installation script not found: {script_path}")
        sys.exit(1)

    print(f"📦 Running installation script: {script_path}")

    try:
        # Run the installation script
        result = subprocess.run(
            ["bash", str(script_path)],
            check=False
        )

        if result.returncode == 0:
            print("\n✅ NPU host setup complete!")
            print("⚠️ Please log out and back in for group changes to take effect")
        else:
            print(f"\n❌ Installation failed with code {result.returncode}")
            sys.exit(result.returncode)

    except Exception as e:
        print(f"\n❌ Installation error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
