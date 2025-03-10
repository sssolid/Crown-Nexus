#!/usr/bin/env python3
"""
Deployment Debugger Script for Crown Nexus.

This script helps diagnose issues with the Crown Nexus deployment in Docker test environments.
It checks SSH connectivity, verifies file permissions, and ensures the environment is properly set up.
"""
from __future__ import annotations

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import asyncssh


async def check_ssh_connection(
    host: str, port: int = 22, username: str = "crown_test", key_path: str = "~/.ssh/id_rsa"
) -> Tuple[bool, str]:
    """
    Check if SSH connection to a server is working.

    Args:
        host: Hostname or IP address
        port: SSH port
        username: SSH username
        key_path: Path to SSH private key

    Returns:
        Tuple of (success, message)
    """
    try:
        expanded_key_path = os.path.expanduser(key_path)
        print(f"Trying to connect to {host}:{port} as {username} using key {expanded_key_path}")

        async with asyncssh.connect(
            host,
            port=port,
            username=username,
            client_keys=[expanded_key_path],
            known_hosts=None
        ) as conn:
            result = await conn.run("echo 'SSH connection successful'")
            if result.exit_status == 0:
                return True, "SSH connection successful"
            else:
                return False, f"SSH command failed with exit code {result.exit_status}"
    except Exception as e:
        return False, f"SSH connection failed: {str(e)}"


def check_file_permissions(file_path: str) -> Tuple[bool, str]:
    """
    Check if a file exists and has the correct permissions.

    Args:
        file_path: Path to the file

    Returns:
        Tuple of (success, message)
    """
    try:
        expanded_path = os.path.expanduser(file_path)
        if not os.path.exists(expanded_path):
            return False, f"File {expanded_path} does not exist"

        permissions = oct(os.stat(expanded_path).st_mode)[-3:]
        if file_path.endswith(".sh") and permissions != '755':
            return False, f"Script {expanded_path} has incorrect permissions: {permissions}, should be 755"
        elif "id_rsa" in file_path and permissions not in ('600', '400'):
            return False, f"SSH key {expanded_path} has incorrect permissions: {permissions}, should be 600 or 400"

        return True, f"File {expanded_path} exists with permissions {permissions}"
    except Exception as e:
        return False, f"Error checking file {file_path}: {str(e)}"


def check_environment_variables() -> Tuple[bool, Dict[str, str]]:
    """
    Check if all required environment variables are set.

    Returns:
        Tuple of (success, variables_dict)
    """
    required_vars = [
        "SERVER1_IP", "SERVER2_IP", "SERVER3_IP",
        "SSH_USER", "TEST_MODE"
    ]

    env_vars = {}
    missing_vars = []

    for var in required_vars:
        value = os.environ.get(var)
        env_vars[var] = value
        if value is None:
            missing_vars.append(var)

    return len(missing_vars) == 0, env_vars


def run_shell_command(command: str) -> Tuple[bool, str, str]:
    """
    Run a shell command and return the result.

    Args:
        command: Command to run

    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


async def check_docker_containers() -> List[Dict[str, str]]:
    """
    Check the status of Docker containers in the test environment.

    Returns:
        List of container info dictionaries
    """
    success, stdout, stderr = run_shell_command("docker ps -a --format '{{.Names}},{{.Status}},{{.Ports}}'")

    containers = []
    if success:
        for line in stdout.strip().split('\n'):
            if line:
                parts = line.split(',')
                if len(parts) >= 2:
                    name = parts[0]
                    status = parts[1]
                    ports = parts[2] if len(parts) > 2 else ""

                    containers.append({
                        "name": name,
                        "status": status,
                        "ports": ports
                    })

    return containers


async def check_ssh_keys_in_containers() -> Dict[str, Tuple[bool, str]]:
    """
    Check if SSH keys are properly installed in the containers.

    Returns:
        Dictionary of container_name -> (success, message)
    """
    results = {}

    for i in range(1, 4):
        container_name = f"crown-test-server{i}"
        try:
            success, stdout, stderr = run_shell_command(
                f"docker exec {container_name} ls -la /home/crown_test/.ssh/authorized_keys"
            )

            if success:
                # Check file permissions
                if "-rw------- 1 crown_test crown_test" in stdout or "-r--r--r-- 1 crown_test crown_test" in stdout:
                    file_ok = True
                else:
                    file_ok = False

                # Check file content
                content_cmd = f"docker exec {container_name} cat /home/crown_test/.ssh/authorized_keys"
                content_success, content, _ = run_shell_command(content_cmd)

                if content_success and content.strip():
                    results[container_name] = (
                        file_ok,
                        f"Key file exists with content {'and correct permissions' if file_ok else 'but incorrect permissions'}"
                    )
                else:
                    results[container_name] = (False, "Key file exists but is empty or unreadable")
            else:
                results[container_name] = (False, f"Key file doesn't exist: {stderr}")
        except Exception as e:
            results[container_name] = (False, f"Error checking keys: {str(e)}")

    return results


async def diagnose_deployment_script(script_path: str) -> List[str]:
    """
    Check the deployment script for potential issues.

    Args:
        script_path: Path to the deployment script

    Returns:
        List of issues found
    """
    issues = []

    # Check if script exists
    exists, msg = check_file_permissions(script_path)
    if not exists:
        issues.append(msg)
        return issues

    # Check shell syntax
    success, stdout, stderr = run_shell_command(f"bash -n {script_path}")
    if not success:
        issues.append(f"Shell syntax error in {script_path}: {stderr}")

    # Read script content
    try:
        with open(script_path, 'r') as f:
            content = f.read()

        # Check for common issues
        if "#!/bin/bash" not in content:
            issues.append(f"Missing shebang (#!/bin/bash) in {script_path}")

        if "set -e" not in content:
            issues.append(f"Missing 'set -e' in {script_path} (script won't exit on errors)")

        # Check for environment imports
        if "source" not in content and ". " not in content:
            issues.append(f"Script might not be importing environment variables in {script_path}")

    except Exception as e:
        issues.append(f"Error analyzing script {script_path}: {str(e)}")

    return issues


async def main() -> int:
    """
    Main function to run all checks.

    Returns:
        Exit code, 0 for success, non-zero for failure
    """
    print("=== Crown Nexus Deployment Debugger ===")
    print(f"Running checks at: {os.getcwd()}")

    all_ok = True

    # Check environment variables
    print("\n--- Checking Environment Variables ---")
    env_ok, env_vars = check_environment_variables()
    for var, value in env_vars.items():
        print(f"{var}: {value if value is not None else 'NOT SET'}")
    if not env_ok:
        print("❌ Some required environment variables are missing!")
        all_ok = False
    else:
        print("✅ All required environment variables are set")

    # Check Docker containers
    print("\n--- Checking Docker Containers ---")
    containers = await check_docker_containers()
    for container in containers:
        print(f"{container['name']}: {container['status']}")
        print(f"  Ports: {container['ports']}")

    # Check SSH keys in containers
    print("\n--- Checking SSH Keys in Containers ---")
    key_results = await check_ssh_keys_in_containers()
    for container, (success, message) in key_results.items():
        if success:
            print(f"✅ {container}: {message}")
        else:
            print(f"❌ {container}: {message}")
            all_ok = False

    # Check SSH connectivity
    print("\n--- Checking SSH Connectivity ---")
    for i in range(1, 4):
        ip = env_vars.get(f"SERVER{i}_IP", f"172.28.1.{9+i}")
        username = env_vars.get("SSH_USER", "crown_test")

        success, message = await check_ssh_connection(
            host=ip,
            username=username,
            key_path="/root/.ssh/id_rsa"
        )

        if success:
            print(f"✅ Server {i} ({ip}): {message}")
        else:
            print(f"❌ Server {i} ({ip}): {message}")
            all_ok = False

    # Check deployment script
    print("\n--- Checking Deployment Scripts ---")
    deployment_dir = Path("/app/test-deployment")
    deploy_script = deployment_dir / "deploy.sh"

    # Check if deploy script exists and is executable
    if not deploy_script.exists():
        print(f"❌ Deployment script not found: {deploy_script}")
        all_ok = False
    else:
        success, message = check_file_permissions(str(deploy_script))
        if success:
            print(f"✅ {deploy_script}: {message}")
        else:
            print(f"❌ {deploy_script}: {message}")
            all_ok = False

        # Analyze deploy script content
        issues = await diagnose_deployment_script(str(deploy_script))
        if issues:
            print(f"⚠️ Issues found in deployment script:")
            for issue in issues:
                print(f"  - {issue}")
            all_ok = False

    # Check if output directory exists and contains expected files
    try:
        if deployment_dir.exists():
            files = list(deployment_dir.glob("**/*.sh"))
            print(f"Found {len(files)} shell scripts in {deployment_dir}")
            for file in files[:5]:  # Show only first 5 for brevity
                success, message = check_file_permissions(str(file))
                if success:
                    print(f"✅ {file.relative_to(deployment_dir)}: {message}")
                else:
                    print(f"❌ {file.relative_to(deployment_dir)}: {message}")
                    all_ok = False

            if len(files) > 5:
                print(f"... and {len(files) - 5} more scripts")
        else:
            print(f"❌ Deployment directory not found: {deployment_dir}")
            all_ok = False
    except Exception as e:
        print(f"❌ Error checking deployment directory: {str(e)}")
        all_ok = False

    # Summary
    print("\n--- Summary ---")
    if all_ok:
        print("✅ All checks passed successfully")
        return 0
    else:
        print("❌ Some checks failed. See details above")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
