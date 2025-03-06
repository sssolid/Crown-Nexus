"""Server analyzer service for the Crown Nexus deployment system."""
from __future__ import annotations

import asyncio
import re
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import structlog

from crown_deploy.models.server import Server, ServerConnection, ServerRole, ServerSpecs
from crown_deploy.models.config import ClusterConfig
from crown_deploy.utils.errors import AnalyzerError, ServerConnectionError

# Initialize logger
logger = structlog.get_logger()


class ServerAnalyzer:
    """Class to analyze servers and determine their optimal roles."""

    def __init__(self, analyzer_script_path: str):
        """Initialize with the path to the server analyzer script."""
        self.analyzer_script = Path(analyzer_script_path)
        if not self.analyzer_script.exists():
            raise FileNotFoundError(f"Analyzer script not found: {analyzer_script_path}")
        if not self.analyzer_script.is_file():
            raise ValueError(f"Analyzer script path is not a file: {analyzer_script_path}")

    async def analyze_server(self, connection: ServerConnection) -> Tuple[ServerSpecs, Set[ServerRole]]:
        """Analyze a server and determine its optimal roles."""
        # Call the server-analyzer.sh script to analyze the server
        logger.info("Analyzing server", hostname=connection.hostname, ip=connection.ip)

        # Create a temporary file to store the server in the inventory
        with tempfile.NamedTemporaryFile('w+', suffix='.csv') as tmp:
            # Create a minimal inventory file with just this server
            tmp.write("hostname,ip,username,key_path,description\n")
            tmp.write(f"{connection.hostname},{connection.ip},{connection.username},{connection.key_path},{connection.description}\n")
            tmp.flush()

            # Run the analyzer script
            cmd = [str(self.analyzer_script), "analyze", connection.hostname]
            logger.debug("Running analyzer command", cmd=cmd)

            try:
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env={"SERVER_INVENTORY_FILE": tmp.name}
                )
                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    error_msg = stderr.decode('utf-8')
                    logger.error("Analyzer script failed",
                                 error=error_msg,
                                 return_code=process.returncode)
                    raise ServerConnectionError(f"Failed to analyze server {connection.hostname}: {error_msg}")

                # Parse the output to extract server specs and recommended roles
                output = stdout.decode('utf-8')
                logger.debug("Analyzer output", output=output)

                # Extract specs
                specs = self._parse_specs(output, connection.hostname, connection.ip)

                # Extract recommended roles
                roles = self._parse_recommended_roles(output)

                return specs, roles

            except Exception as e:
                logger.exception("Error analyzing server",
                                 hostname=connection.hostname,
                                 error=str(e))
                raise ServerConnectionError(f"Error analyzing server {connection.hostname}: {str(e)}")

    def _parse_specs(self, output: str, hostname: str, ip: str) -> ServerSpecs:
        """Parse server specifications from analyzer output."""
        # Extract CPU information
        cpu_model = ""
        cpu_cores = 0
        for line in output.splitlines():
            if "CPU:" in line:
                match = re.search(r"CPU:\s+(.*)\s+\((\d+)\s+cores\)", line)
                if match:
                    cpu_model = match.group(1).strip()
                    cpu_cores = int(match.group(2))
                    break

        # Extract memory information
        memory_gb = 0
        for line in output.splitlines():
            if "Memory:" in line:
                match = re.search(r"Memory:\s+(\d+)GB", line)
                if match:
                    memory_gb = int(match.group(1))
                    break
                # Alternative pattern for memory in format like "16GB total"
                match = re.search(r"Memory:\s+([\d.]+)(?:GB|G|GiB) total", line)
                if match:
                    memory_gb = int(float(match.group(1)))
                    break

        # Extract disk information
        disk_gb = 0
        disk_type = "Unknown"
        for line in output.splitlines():
            if "Disk:" in line:
                # Pattern for disk like "500GB total, SSD"
                match = re.search(r"Disk:\s+([\d.]+)(?:GB|G|GiB) total,\s+(\w+)", line)
                if match:
                    disk_gb = int(float(match.group(1)))
                    disk_type_str = match.group(2).upper()
                    if disk_type_str in ["SSD", "HDD", "NVME"]:
                        disk_type = disk_type_str
                    break

        # Extract OS information
        os_info = ""
        for line in output.splitlines():
            if "OS:" in line:
                match = re.search(r"OS:\s+(.*)", line)
                if match:
                    os_info = match.group(1).strip()
                    break

        # Create and return the ServerSpecs object
        return ServerSpecs(
            hostname=hostname,
            ip=ip,
            cpu_cores=cpu_cores,
            cpu_model=cpu_model,
            memory_gb=memory_gb,
            disk_gb=disk_gb,
            disk_type=disk_type,
            os_info=os_info
        )

    def _parse_recommended_roles(self, output: str) -> Set[ServerRole]:
        """Parse recommended roles from analyzer output."""
        roles: Set[ServerRole] = set()
        in_recommendations_section = False

        for line in output.splitlines():
            if "Recommended Roles:" in line:
                in_recommendations_section = True
                continue

            if in_recommendations_section:
                if not line.strip() or "===" in line:
                    # End of recommendations section
                    in_recommendations_section = False
                    continue

                # Check for specific role recommendations
                if "database" in line.lower() or "postgresql" in line.lower() or "mysql" in line.lower():
                    roles.add(ServerRole.DATABASE)

                if "application server" in line.lower() or "web server" in line.lower() or "api" in line.lower():
                    roles.add(ServerRole.BACKEND)
                    roles.add(ServerRole.FRONTEND)

                if "load balancer" in line.lower() or "reverse proxy" in line.lower() or "nginx" in line.lower():
                    roles.add(ServerRole.LOAD_BALANCER)

                if "monitoring" in line.lower() or "prometheus" in line.lower() or "grafana" in line.lower():
                    roles.add(ServerRole.MONITORING)

                if "ci/cd" in line.lower() or "jenkins" in line.lower() or "gitlab" in line.lower():
                    roles.add(ServerRole.CI_CD)

                if "elasticsearch" in line.lower() or "elk" in line.lower():
                    roles.add(ServerRole.ELASTICSEARCH)

                if "redis" in line.lower() or "cache" in line.lower() or "in-memory" in line.lower():
                    roles.add(ServerRole.REDIS)

                if "storage" in line.lower() or "nfs" in line.lower() or "backup" in line.lower():
                    roles.add(ServerRole.STORAGE)

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
        """Optimize role assignments based on server specifications."""
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

    def _find_best_server_for_role(self, role: ServerRole, servers: List[Server]) -> Optional[Server]:
        """Find the best server for a specific role based on hardware specs."""
        if not servers or not any(s.specs for s in servers):
            return None

        # Define scoring function based on role
        def score_for_role(server: Server) -> float:
            if not server.specs:
                return 0.0

            specs = server.specs
            score = 0.0

            # Base score components
            cpu_score = specs.cpu_cores * 1.0
            mem_score = specs.memory_gb * 0.5
            disk_score = specs.disk_gb * 0.1
            ssd_bonus = 20.0 if specs.disk_type in ["SSD", "NVME"] else 0.0

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

            return score

        # Score each server
        scored_servers = [(server, score_for_role(server)) for server in servers]

        # Sort by score (highest first)
        scored_servers.sort(key=lambda x: x[1], reverse=True)

        # Return the highest-scoring server
        return scored_servers[0][0] if scored_servers else None
