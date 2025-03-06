#!/usr/bin/env python3
"""
Example script demonstrating how to use the Python-based server analyzer directly.
"""
import asyncio
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the crown_deploy package
sys.path.insert(0, str(Path(__file__).parent.parent))

from crown_deploy.models.server import ServerConnection
from crown_deploy.services.python_analyzer import PythonServerAnalyzer


async def main():
    """Example usage of the PythonServerAnalyzer."""
    # Define your servers
    servers = [
        ServerConnection(
            hostname="server1",
            ip="192.168.1.101",
            username="ubuntu",
            key_path="~/.ssh/id_rsa",
            description="Primary server"
        ),
        ServerConnection(
            hostname="server2",
            ip="192.168.1.102",
            username="ubuntu",
            key_path="~/.ssh/id_rsa",
            description="Secondary server"
        ),
        # Add more servers as needed
    ]
    
    # Create the analyzer
    analyzer = PythonServerAnalyzer()
    
    # Analyze all servers and create a cluster configuration
    cluster = await analyzer.analyze_and_create_cluster(servers)
    
    # Print the results
    print("\n=== Server Analysis Results ===")
    for i, server in enumerate(cluster.servers, 1):
        roles_str = ", ".join(str(role) for role in server.assigned_roles)
        print(f"Server {i}: {server.hostname} ({server.ip})")
        if server.specs:
            print(f"  - CPU: {server.specs.cpu_cores} cores, {server.specs.cpu_model}")
            print(f"  - Memory: {server.specs.memory_gb} GB")
            print(f"  - Disk: {server.specs.disk_gb} GB, {server.specs.disk_type}")
            print(f"  - OS: {server.specs.os_info}")
        print(f"  - Recommended roles: {roles_str}")
        print()
    
    # Check for any role assignment issues
    errors = cluster.validate_roles()
    if errors:
        print("\n=== Configuration Warnings ===")
        for error in errors:
            print(f"- {error}")


if __name__ == "__main__":
    asyncio.run(main())
