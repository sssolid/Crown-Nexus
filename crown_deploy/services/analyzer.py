"""Python-based server analyzer for Crown Nexus deployment.

This module replaces the dependency on the external server-analyzer.sh script
with a pure Python implementation using asyncssh for remote command execution.
"""
from __future__ import annotations

import asyncio
import re
from typing import Dict, List, Optional, Set, Tuple, Any, cast

import asyncssh
import structlog
from pydantic import BaseModel

from crown_deploy.models.server import Server, ServerConnection, ServerRole, ServerSpecs
from crown_deploy.models.config import ClusterConfig
from crown_deploy.utils.errors import AnalyzerError, ServerConnectionError

# Initialize logger
logger = structlog.get_logger()


class ServerCommand(BaseModel):
    """Command to run on a server with parsing instructions."""
    command: str
    description: str
    parser: str = "text"  # Options: text, json, etc.
    required: bool = False
    timeout: int = 30  # Timeout in seconds


class PythonServerAnalyzer:
    """Python implementation of server hardware analysis and role recommendations."""
    
    # Standard commands to gather hardware information
    HARDWARE_COMMANDS = {
        "cpu_info": ServerCommand(
            command="lscpu",
            description="CPU information",
            required=True
        ),
        "memory_info": ServerCommand(
            command="free -h",
            description="Memory information",
            required=True
        ),
        "disk_info": ServerCommand(
            command="lsblk -o NAME,SIZE,TYPE,ROTA",
            description="Disk information",
            required=True
        ),
        "os_info": ServerCommand(
            command="cat /etc/os-release",
            description="OS information"
        ),
        "load_avg": ServerCommand(
            command="cat /proc/loadavg",
            description="Current load average"
        ),
        "installed_packages": ServerCommand(
            command="dpkg-query -f '${binary:Package}\n' -W",
            description="Installed packages",
            timeout=60
        )
    }
    
    def __init__(self):
        """Initialize the Python server analyzer."""
        pass
    
    async def analyze_server(self, connection: ServerConnection) -> Tuple[ServerSpecs, Set[ServerRole]]:
        """Analyze a server and determine its optimal roles."""
        logger.info("Analyzing server", hostname=connection.hostname, ip=connection.ip)
        
        try:
            # Gather hardware information
            hw_info = await self._gather_hardware_info(connection)
            
            # Parse the hardware info into structured data
            specs = self._parse_hardware_info(hw_info, connection.hostname, connection.ip)
            
            # Determine recommended roles based on specs
            roles = self._recommend_roles(specs)
            
            return specs, roles
            
        except Exception as e:
            logger.exception("Error analyzing server", 
                           hostname=connection.hostname,
                           error=str(e))
            raise ServerConnectionError(f"Error analyzing server {connection.hostname}: {str(e)}")
    
    async def _gather_hardware_info(self, connection: ServerConnection) -> Dict[str, str]:
        """Gather hardware information from the server via SSH."""
        hw_info: Dict[str, str] = {}
        
        try:
            # Set up SSH connection
            async with asyncssh.connect(
                connection.ip,
                username=connection.username,
                client_keys=[connection.key_path],
                known_hosts=None  # In production, you'd want to use known_hosts
            ) as ssh:
                logger.debug("SSH connection established", hostname=connection.hostname)
                
                # Execute hardware information commands
                for cmd_name, cmd_info in self.HARDWARE_COMMANDS.items():
                    try:
                        result = await ssh.run(cmd_info.command, timeout=cmd_info.timeout)
                        if result.exit_status == 0:
                            hw_info[cmd_name] = result.stdout
                        else:
                            logger.warning(f"Command failed: {cmd_info.command}",
                                         hostname=connection.hostname,
                                         exit_status=result.exit_status,
                                         stderr=result.stderr)
                            if cmd_info.required:
                                raise AnalyzerError(
                                    f"Required command failed on {connection.hostname}: {cmd_info.command} - {result.stderr}"
                                )
                    except asyncio.TimeoutError:
                        logger.warning(f"Command timed out: {cmd_info.command}",
                                     hostname=connection.hostname,
                                     timeout=cmd_info.timeout)
                        if cmd_info.required:
                            raise AnalyzerError(
                                f"Required command timed out on {connection.hostname}: {cmd_info.command}"
                            )
            
            return hw_info
            
        except asyncssh.Error as e:
            logger.error("SSH connection error",
                       hostname=connection.hostname,
                       error=str(e))
            raise ServerConnectionError(f"SSH connection error for {connection.hostname}: {str(e)}")
    
    def _parse_hardware_info(self, hw_info: Dict[str, str], hostname: str, ip: str) -> ServerSpecs:
        """Parse hardware information into a ServerSpecs object."""
        # Initialize defaults
        cpu_model = ""
        cpu_cores = 0
        memory_gb = 0
        disk_gb = 0
        disk_type = "Unknown"
        os_info = ""
        
        # Parse CPU information
        if "cpu_info" in hw_info:
            cpu_info = hw_info["cpu_info"]
            
            # Get CPU model
            model_match = re.search(r"Model name:\s+(.*)", cpu_info)
            if model_match:
                cpu_model = model_match.group(1).strip()
            
            # Get CPU core count
            cores_match = re.search(r"CPU\(s\):\s+(\d+)", cpu_info)
            if cores_match:
                cpu_cores = int(cores_match.group(1))
        
        # Parse memory information
        if "memory_info" in hw_info:
            mem_info = hw_info["memory_info"]
            mem_match = re.search(r"Mem:\s+(\S+)\s+(\S+)", mem_info)
            if mem_match:
                # Convert memory to GB
                mem_total = mem_match.group(1)
                if 'G' in mem_total:
                    memory_gb = int(float(mem_total.replace('G', '').replace('i', '')))
                elif 'M' in mem_total:
                    memory_gb = int(float(mem_total.replace('M', '').replace('i', '')) / 1024)
                elif 'K' in mem_total:
                    memory_gb = int(float(mem_total.replace('K', '').replace('i', '')) / (1024 * 1024))
                else:
                    # Assume bytes
                    memory_gb = int(float(mem_total) / (1024 * 1024 * 1024))
        
        # Parse disk information
        if "disk_info" in hw_info:
            disk_info = hw_info["disk_info"]
            
            # Find the first disk (typically sda or nvme0n1)
            disk_match = re.search(r"(sd[a-z]|nvme\d+n\d+)\s+(\S+)\s+disk\s+(\d+)", disk_info)
            if disk_match:
                disk_name = disk_match.group(1)
                disk_size = disk_match.group(2)
                is_rotational = disk_match.group(3) == "1"
                
                # Convert disk size to GB
                if 'T' in disk_size:
                    disk_gb = int(float(disk_size.replace('T', '')) * 1024)
                elif 'G' in disk_size:
                    disk_gb = int(float(disk_size.replace('G', '')))
                elif 'M' in disk_size:
                    disk_gb = int(float(disk_size.replace('M', '')) / 1024)
                else:
                    # Fallback: look for size in bytes from other commands
                    size_match = re.search(r"SIZE=\"(\d+)\"", hw_info.get("disk_size", ""))
                    if size_match:
                        disk_gb = int(int(size_match.group(1)) / (1024 * 1024 * 1024))
                
                # Determine disk type
                if 'nvme' in disk_name:
                    disk_type = "NVMe"
                elif not is_rotational:
                    disk_type = "SSD"
                else:
                    disk_type = "HDD"
        
        # Parse OS information
        if "os_info" in hw_info:
            os_match = re.search(r'PRETTY_NAME="([^"]+)"', hw_info["os_info"])
            if os_match:
                os_info = os_match.group(1)
        
        # Create and return the ServerSpecs object
        return ServerSpecs(
            hostname=hostname,
            ip=ip,
            cpu_cores=max(cpu_cores, 1),  # Ensure at least 1 core
            cpu_model=cpu_model,
            memory_gb=max(memory_gb, 1),  # Ensure at least 1 GB
            disk_gb=max(disk_gb, 1),      # Ensure at least 1 GB
            disk_type=disk_type,
            os_info=os_info
        )
    
    def _recommend_roles(self, specs: ServerSpecs) -> Set[ServerRole]:
        """Recommend server roles based on hardware specs."""
        roles: Set[ServerRole] = set()
        
        # Base scores for role suitability
        role_scores: Dict[ServerRole, float] = {role: 0.0 for role in ServerRole}
        
        # Calculate scores for each role based on hardware
        # Database role benefits from SSD/NVMe and lots of memory
        role_scores[ServerRole.DATABASE] = (
            (5.0 if specs.disk_type in ["SSD", "NVMe"] else 0.0) +  # SSD major boost
            (specs.memory_gb * 0.3) +                               # Memory is important
            (specs.cpu_cores * 0.2)                                 # Some CPU importance
        )
        
        # Backend role needs balanced resources, CPU and memory important
        role_scores[ServerRole.BACKEND] = (
            (specs.cpu_cores * 0.4) +                               # CPU is important
            (specs.memory_gb * 0.3) +                               # Memory is important
            (2.0 if specs.disk_type in ["SSD", "NVMe"] else 0.0)    # SSD minor boost
        )
        
        # Frontend role needs less resources
        role_scores[ServerRole.FRONTEND] = (
            (specs.cpu_cores * 0.3) +                               # CPU is somewhat important
            (specs.memory_gb * 0.2) +                               # Memory is somewhat important
            (1.0 if specs.disk_type in ["SSD", "NVMe"] else 0.0)    # SSD slight boost
        )
        
        # Load balancer needs CPU for connection handling
        role_scores[ServerRole.LOAD_BALANCER] = (
            (specs.cpu_cores * 0.5) +                               # CPU is very important
            (specs.memory_gb * 0.1)                                 # Memory is less important
        )
        
        # Elasticsearch needs lots of memory and benefits from SSD
        role_scores[ServerRole.ELASTICSEARCH] = (
            (specs.memory_gb * 0.5) +                               # Memory is very important
            (specs.cpu_cores * 0.2) +                               # Some CPU importance
            (4.0 if specs.disk_type in ["SSD", "NVMe"] else 0.0)    # SSD major boost
        )
        
        # Redis is very memory intensive
        role_scores[ServerRole.REDIS] = (
            (specs.memory_gb * 0.6) +                               # Memory is critical
            (specs.cpu_cores * 0.1) +                               # CPU less important
            (2.0 if specs.disk_type in ["SSD", "NVMe"] else 0.0)    # SSD minor boost
        )
        
        # Monitoring can run on less powerful hardware
        role_scores[ServerRole.MONITORING] = (
            (specs.cpu_cores * 0.2) +                               # Some CPU needed
            (specs.memory_gb * 0.2) +                               # Some memory needed
            (specs.disk_gb * 0.01)                                  # Disk space for logs
        )
        
        # CI/CD needs good CPU and memory
        role_scores[ServerRole.CI_CD] = (
            (specs.cpu_cores * 0.4) +                               # CPU is important
            (specs.memory_gb * 0.3) +                               # Memory is important
            (specs.disk_gb * 0.01)                                  # Disk space for builds
        )
        
        # Storage role primarily needs disk space
        role_scores[ServerRole.STORAGE] = (
            (specs.disk_gb * 0.03) +                                # Disk space is critical
            (1.0 if specs.disk_type in ["SSD", "NVMe"] else 3.0)    # HDD is actually better for bulk storage
        )
        
        # Assign roles based on threshold scores and server capabilities
        
        # High-spec server (8+ cores, 16+ GB RAM)
        if specs.cpu_cores >= 8 and specs.memory_gb >= 16:
            # Can handle multiple roles
            top_roles = sorted(
                role_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]  # Take top 3 roles
            
            for role, score in top_roles:
                if score > 5.0:  # Minimum threshold
                    roles.add(role)
        
        # Medium-spec server (4+ cores, 8+ GB RAM)
        elif specs.cpu_cores >= 4 and specs.memory_gb >= 8:
            # Can handle a couple of roles
            top_roles = sorted(
                role_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:2]  # Take top 2 roles
            
            for role, score in top_roles:
                if score > 4.0:  # Minimum threshold
                    roles.add(role)
        
        # Low-spec server
        else:
            # Should just handle one role
            top_role = max(role_scores.items(), key=lambda x: x[1])
            if top_role[1] > 3.0:  # Minimum threshold
                roles.add(top_role[0])
        
        # Special cases: ensure we have essential roles even for low-spec servers
        if specs.cpu_cores >= 2 and specs.memory_gb >= 4 and not roles:
            # Assign at least FRONTEND role for minimally capable servers
            roles.add(ServerRole.FRONTEND)
        
        # If we have a good SSD/NVMe but no roles assigned yet
        if specs.disk_type in ["SSD", "NVMe"] and specs.memory_gb >= 8 and not roles:
            # Database is a good fit for SSD systems with reasonable memory
            roles.add(ServerRole.DATABASE)
        
        # If no roles assigned yet, assign MONITORING as a fallback
        if not roles and specs.cpu_cores >= 1 and specs.memory_gb >= 2:
            roles.add(ServerRole.MONITORING)
        
        return roles
    
    async def analyze_all_servers(self, connections: List[ServerConnection]) -> List[Tuple[ServerConnection, ServerSpecs, Set[ServerRole]]]:
        """Analyze all servers and determine their optimal roles."""
        results = []
        for conn in connections:
            try:
                specs, roles = await self.analyze_server(conn)
                results.append((conn, specs, roles))
            except Exception as e:
                logger.error("Failed to analyze server", 
                           hostname=conn.hostname,
                           error=str(e))
                # Continue with the next server
        
        return results
    
    async def analyze_and_create_cluster(self, connections: List[ServerConnection]) -> ClusterConfig:
        """Analyze servers and create a cluster configuration."""
        analysis_results = await self.analyze_all_servers(connections)
        
        servers = []
        for conn, specs, roles in analysis_results:
            server = Server(
                connection=conn,
                specs=specs,
                assigned_roles=roles
            )
            servers.append(server)
        
        # Create the cluster configuration
        cluster = ClusterConfig(servers=servers)
        
        # Validate and optimize role assignments
        self._optimize_role_assignments(cluster)
        
        return cluster
    
    def _optimize_role_assignments(self, cluster: ClusterConfig) -> None:
        """Optimize role assignments based on server specifications and cluster requirements."""
        # Ensure critical roles are assigned
        essential_roles = {ServerRole.DATABASE, ServerRole.BACKEND, ServerRole.FRONTEND}
        
        # Check if essential roles are assigned
        for role in essential_roles:
            if not cluster.get_servers_by_role(role):
                # Find the best server for this role
                best_server = self._find_best_server_for_role(role, cluster.servers)
                if best_server:
                    logger.info("Assigning missing essential role", 
                              role=role,
                              server=best_server.hostname)
                    best_server.assigned_roles.add(role)
        
        # Check for overloaded servers (too many roles)
        for server in cluster.servers:
            if len(server.assigned_roles) > 3:
                logger.warning("Server has too many roles", 
                             server=server.hostname,
                             roles=server.assigned_roles)
        
        # Ensure compatibility between roles
        for server in cluster.servers:
            roles = list(server.assigned_roles)
            
            # Check incompatible pairs and remove less suitable role
            if ServerRole.DATABASE in roles and ServerRole.CI_CD in roles:
                # These roles tend to conflict with resource usage
                # Determine which to keep based on server specs
                if server.specs:
                    if server.specs.disk_type in ["SSD", "NVMe"] and server.specs.memory_gb >= 16:
                        # Better for database
                        logger.warning("Removing CI_CD role from server with DATABASE role",
                                     server=server.hostname)
                        server.assigned_roles.remove(ServerRole.CI_CD)
                    else:
                        # Better for CI/CD
                        logger.warning("Removing DATABASE role from server with CI_CD role",
                                     server=server.hostname)
                        server.assigned_roles.remove(ServerRole.DATABASE)
    
    def _find_best_server_for_role(self, role: ServerRole, servers: List[Server]) -> Optional[Server]:
        """Find the best server for a specific role based on hardware specs."""
        if not servers or not any(s.specs for s in servers):
            return None
        
        # Score each server for the given role
        scored_servers = []
        for server in servers:
            if not server.specs:
                continue
            
            specs = server.specs
            score = 0.0
            
            # Base score components
            cpu_score = specs.cpu_cores * 1.0
            mem_score = specs.memory_gb * 0.5
            disk_score = specs.disk_gb * 0.1
            ssd_bonus = 20.0 if specs.disk_type in ["SSD", "NVMe"] else 0.0
            
            if role == ServerRole.DATABASE:
                # Databases benefit from SSD, memory, and moderate CPU
                score = ssd_bonus * 2.0 + mem_score * 1.5 + cpu_score
                
            elif role == ServerRole.BACKEND:
                # Backend servers benefit from CPU and memory
                score = cpu_score * 1.5 + mem_score + ssd_bonus * 0.5
                
            elif role == ServerRole.FRONTEND:
                # Frontend servers benefit from CPU and bandwidth (approximated by cpu)
                score = cpu_score + mem_score * 0.5
                
            elif role == ServerRole.LOAD_BALANCER:
                # Load balancers benefit from CPU and network (approximated by cpu)
                score = cpu_score * 1.5
                
            elif role == ServerRole.MONITORING:
                # Monitoring needs disk space and moderate CPU/memory
                score = disk_score + cpu_score * 0.5 + mem_score * 0.5
                
            elif role == ServerRole.CI_CD:
                # CI/CD benefits from CPU and memory
                score = cpu_score * 1.5 + mem_score
                
            elif role == ServerRole.ELASTICSEARCH:
                # Elasticsearch benefits from memory and SSD
                score = mem_score * 2.0 + ssd_bonus + cpu_score * 0.5
                
            elif role == ServerRole.REDIS:
                # Redis benefits from memory and SSD
                score = mem_score * 2.0 + ssd_bonus + cpu_score * 0.5
                
            elif role == ServerRole.STORAGE:
                # Storage benefits from disk size
                score = disk_score * 3.0
                
            # Penalize servers that already have many roles
            score -= len(server.assigned_roles) * 5.0
            
            scored_servers.append((server, score))
        
        # Sort by score (highest first)
        scored_servers.sort(key=lambda x: x[1], reverse=True)
        
        # Return the highest-scoring server
        return scored_servers[0][0] if scored_servers else None
