#!/usr/bin/env python3
"""
Crown Test Runner Fix

This script fixes issues with the Crown Nexus deployment test runner.
Run this script within the test runner container to fix deployment issues.
"""
from __future__ import annotations

import os
import sys
import time
import shutil
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any

def print_header(text: str) -> None:
    """Print a header with formatting."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

async def run_command(cmd: str, cwd: Optional[str] = None) -> Tuple[int, str, str]:
    """
    Run a command asynchronously.

    Args:
        cmd: Command to run
        cwd: Working directory

    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    print(f"Running command: {cmd}")
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )

        stdout, stderr = await process.communicate()

        stdout_str = stdout.decode() if stdout else ""
        stderr_str = stderr.decode() if stderr else ""

        if process.returncode != 0:
            print(f"Command failed with code {process.returncode}")
            print(f"Error output: {stderr_str}")
        else:
            print(f"Command completed successfully")

        return process.returncode, stdout_str, stderr_str
    except Exception as e:
        print(f"Error running command: {e}")
        return 1, "", str(e)

def fix_deployment_script(output_dir: Path) -> None:
    """
    Fix the deployment script to work in automated testing.

    Args:
        output_dir: Path to the deployment scripts directory
    """
    print_header("Fixing deployment script")

    deploy_script = output_dir / "deploy.sh"
    if not deploy_script.exists():
        print(f"Error: Deployment script not found at {deploy_script}")
        return

    print(f"Fixing deployment script at {deploy_script}")

    # Read the current content
    with open(deploy_script, "r") as f:
        content = f.read()

    # Backup the original
    with open(f"{deploy_script}.bak", "w") as f:
        f.write(content)

    # Make non-interactive
    content = content.replace(
        'read -p "Continue with deployment? [y/N] " -n 1 -r',
        'REPLY="y" # Auto yes for testing'
    )

    # Fix the script to avoid interactive prompting
    content = content.replace(
        'if [[ ! $REPLY =~ ^[Yy]$ ]]; then',
        'if false; then'
    )

    # Add a test mode check
    test_mode_check = """
# Test mode detection
if [ "$TEST_MODE" = "true" ]; then
    echo "Running in test mode - automated deployment"
fi
"""

    content = content.replace(
        "set -e  # Exit on any error",
        "set -e  # Exit on any error\n" + test_mode_check
    )

    # Write the updated content
    with open(deploy_script, "w") as f:
        f.write(content)

    # Make sure it's executable
    os.chmod(deploy_script, 0o755)

    print(f"Fixed deployment script at {deploy_script}")

def create_test_env_script(output_dir: Path) -> None:
    """
    Create a test environment script.

    Args:
        output_dir: Path to the deployment scripts directory
    """
    print_header("Creating test environment script")

    test_env_script = output_dir / "test-env.sh"
    content = """#!/bin/bash
# Test environment for Crown Nexus deployment

# Set test mode
export TEST_MODE=true

# Skip interactive prompts
export SKIP_INTERACTIVE=true

# SSH user
export SSH_USER="crown_test"

# SSH key
export SSH_KEY_PATH="/root/.ssh/id_rsa"

echo "Test environment loaded"
"""

    with open(test_env_script, "w") as f:
        f.write(content)

    os.chmod(test_env_script, 0o755)

    print(f"Created test environment script at {test_env_script}")

def create_run_script(output_dir: Path) -> None:
    """
    Create a run script that wraps the deployment script.

    Args:
        output_dir: Path to the deployment scripts directory
    """
    print_header("Creating deployment run script")

    run_script = output_dir / "run_test_deploy.sh"
    content = """#!/bin/bash
# Run script for Crown Nexus deployment tests

set -e

# Change to script directory
cd $(dirname $0)

# Load test environment
source ./test-env.sh

# Print environment info
echo "=== Environment Information ==="
echo "Working directory: $(pwd)"
echo "Test mode: $TEST_MODE"
echo "SSH user: $SSH_USER"
echo "SSH key: $SSH_KEY_PATH"
echo "==========================="

# Run deployment with debugging
bash -x ./deploy.sh
"""

    with open(run_script, "w") as f:
        f.write(content)

    os.chmod(run_script, 0o755)

    print(f"Created run script at {run_script}")

def fix_server_scripts(output_dir: Path) -> None:
    """
    Fix server setup scripts to work in automated testing.

    Args:
        output_dir: Path to the deployment scripts directory
    """
    print_header("Fixing server setup scripts")

    for server_dir in output_dir.glob("server*"):
        setup_script = server_dir / "setup.sh"
        if not setup_script.exists():
            print(f"Error: Setup script not found at {setup_script}")
            continue

        print(f"Fixing setup script at {setup_script}")

        # Read the current content
        with open(setup_script, "r") as f:
            content = f.read()

        # Backup the original
        with open(f"{setup_script}.bak", "w") as f:
            f.write(content)

        # Make non-interactive
        content = content.replace(
            "apt",
            "DEBIAN_FRONTEND=noninteractive apt"
        )

        # Skip certbot in test environment
        content = content.replace(
            "sudo certbot",
            "# Skipped in test mode: sudo certbot"
        )

        # Write the updated content
        with open(setup_script, "w") as f:
            f.write(content)

        # Make sure it's executable
        os.chmod(setup_script, 0o755)

        print(f"Fixed setup script at {setup_script}")

async def fix_ssh_config() -> None:
    """Fix SSH configuration for testing."""
    print_header("Fixing SSH configuration")

    # Create .ssh directory
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True)
    os.chmod(ssh_dir, 0o700)

    # Create SSH config
    ssh_config = os.path.join(ssh_dir, "config")
    config_content = """Host *
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
"""

    with open(ssh_config, "w") as f:
        f.write(config_content)

    os.chmod(ssh_config, 0o600)

    print(f"Created SSH config at {ssh_config}")

    # Generate SSH key if needed
    ssh_key = os.path.join(ssh_dir, "id_rsa")
    if not os.path.exists(ssh_key):
        print("Generating SSH key...")
        cmd = f"ssh-keygen -t rsa -b 2048 -f {ssh_key} -N \"\""
        await run_command(cmd)

    os.chmod(ssh_key, 0o600)
    print(f"SSH key ready at {ssh_key}")

    # Copy key to test servers
    if os.path.exists(f"{ssh_key}.pub"):
        with open(f"{ssh_key}.pub", "r") as f:
            public_key = f.read().strip()

        for i in range(1, 4):
            container = f"crown-test-server{i}"
            print(f"Copying SSH key to {container}...")

            cmd = f"docker exec {container} bash -c 'mkdir -p /home/crown_test/.ssh && chmod 700 /home/crown_test/.ssh && echo \"{public_key}\" > /home/crown_test/.ssh/authorized_keys && chmod 600 /home/crown_test/.ssh/authorized_keys && chown -R crown_test:crown_test /home/crown_test/.ssh'"
            await run_command(cmd)

            # Restart SSH service
            cmd = f"docker exec {container} service ssh restart"
            await run_command(cmd)

            # Test connection
            ip = f"172.28.1.{9+i}"
            cmd = f"ssh -o ConnectTimeout=5 crown_test@{ip} echo 'SSH test successful'"
            ret_code, stdout, stderr = await run_command(cmd)

            if ret_code == 0:
                print(f"✅ SSH connection to {container} successful")
            else:
                print(f"❌ SSH connection to {container} failed")
                print(f"Debug info for {container}:")

                # Run detailed diagnostics
                cmd = f"docker exec {container} ps aux | grep sshd"
                await run_command(cmd)

                cmd = f"docker exec {container} ls -la /home/crown_test/.ssh"
                await run_command(cmd)

                cmd = f"docker exec {container} cat /home/crown_test/.ssh/authorized_keys"
                await run_command(cmd)

    print("SSH configuration fixed")

async def main() -> int:
    """Main function to fix all issues."""
    print_header("Crown Test Runner Fix")

    # Find deployment directory
    output_dir = Path("/app/test-deployment")
    if not output_dir.exists():
        print(f"Error: Deployment directory not found at {output_dir}")
        print("Please run the deployment script generator first")
        return 1

    # Fix SSH configuration
    await fix_ssh_config()

    # Fix deployment script
    fix_deployment_script(output_dir)

    # Fix server scripts
    fix_server_scripts(output_dir)

    # Create test environment script
    create_test_env_script(output_dir)

    # Create run script
    create_run_script(output_dir)

    print_header("All fixes completed")
    print(f"You can now run the deployment test with: {output_dir}/run_test_deploy.sh")

    return 0

if __name__ == "__main__":
    asyncio.run(main())
