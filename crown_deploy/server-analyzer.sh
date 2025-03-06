#!/bin/bash

# Server Cluster Analyzer
# This script connects to servers via SSH, analyzes their hardware,
# and provides recommendations for their role in a cluster.

set -e

# Default SSH options
SSH_OPTS="-o StrictHostKeyChecking=accept-new -o ConnectTimeout=10"

# Color codes for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Server inventory file (CSV format: hostname,ip,username,key_path,description)
INVENTORY_FILE="$HOME/server_inventory.csv"

# Create inventory file if it doesn't exist
if [ ! -f "$INVENTORY_FILE" ]; then
    echo -e "Creating new inventory file at $INVENTORY_FILE"
    mkdir -p "$(dirname "$INVENTORY_FILE")"
    echo "hostname,ip,username,key_path,description" > "$INVENTORY_FILE"
    echo "server1,192.168.1.101,user,~/.ssh/id_rsa,Primary server" >> "$INVENTORY_FILE"
    echo "server2,192.168.1.102,user,~/.ssh/id_rsa,Secondary server" >> "$INVENTORY_FILE"
    echo -e "${YELLOW}Initialized with default servers. Edit $INVENTORY_FILE to customize.${NC}"
fi

# Function to display usage information
show_usage() {
    echo -e "${BLUE}Server Cluster Analyzer${NC}"
    echo "Usage: $0 [options] [command]"
    echo
    echo "Commands:"
    echo "  list              List all servers in inventory"
    echo "  connect <n>    Connect to a specific server"
    echo "  analyze <n>    Analyze hardware and provide recommendations for a server"
    echo "  analyze-all       Analyze all servers and provide cluster recommendations"
    echo "  add               Add a new server to inventory"
    echo "  remove <n>     Remove a server from inventory"
    echo
    echo "Options:"
    echo "  -h, --help        Show this help message"
    echo "  -v, --verbose     Enable verbose output"
}

# Function to list all servers
list_servers() {
    echo -e "${BLUE}Server Inventory:${NC}"
    # Skip header line, then print formatted output
    awk -F, 'NR>1 {printf "%-15s %-15s %-10s %s\n", $1, $2, $3, $5}' "$INVENTORY_FILE"
}

# Function to add a new server
add_server() {
    echo -e "${BLUE}Add a new server to inventory:${NC}"
    read -p "Hostname: " hostname
    read -p "IP Address: " ip
    read -p "Username: " username
    read -p "SSH Key Path (default: ~/.ssh/id_rsa): " key_path
    key_path=${key_path:-~/.ssh/id_rsa}
    read -p "Description: " description

    # Append to inventory file
    echo "$hostname,$ip,$username,$key_path,$description" >> "$INVENTORY_FILE"
    echo -e "${GREEN}Server $hostname added to inventory.${NC}"
}

# Function to remove a server
remove_server() {
    local server_name=$1
    if [ -z "$server_name" ]; then
        echo -e "${RED}Error: Missing server name.${NC}"
        return 1
    fi

    # Create a temporary file
    local temp_file=$(mktemp)
    # Filter out the server to remove, keeping all other lines
    awk -F, -v name="$server_name" 'NR==1 || $1 != name' "$INVENTORY_FILE" > "$temp_file"

    # Check if any server was removed
    if [ "$(wc -l < "$INVENTORY_FILE")" -eq "$(wc -l < "$temp_file")" ]; then
        echo -e "${RED}Error: Server '$server_name' not found in inventory.${NC}"
        rm "$temp_file"
        return 1
    fi

    # Replace the original file
    mv "$temp_file" "$INVENTORY_FILE"
    echo -e "${GREEN}Server '$server_name' removed from inventory.${NC}"
}

# Function to get server details by name
get_server_details() {
    local server_name=$1
    awk -F, -v name="$server_name" '$1 == name {print $0}' "$INVENTORY_FILE"
}

# Function to recommend roles based on hardware specs
recommend_role() {
    local cpu_cores=$1
    local ram_gb=$2
    local disk_gb=$3
    local disk_type=$4

    echo -e "${PURPLE}Recommended Roles:${NC}"

    # High CPU recommendations
    if [ "$cpu_cores" -ge 16 ]; then
        echo -e "✅ Compute-intensive workloads (CI/CD runners, batch processing)"
    fi

    # High RAM recommendations
    if [ "$ram_gb" -ge 64 ]; then
        echo -e "✅ In-memory databases (Redis, Memcached)"
        echo -e "✅ Big data processing (Spark, Hadoop)"
    fi

    # Fast disk recommendations
    if [[ "$disk_type" == *"SSD"* || "$disk_type" == *"NVMe"* ]]; then
        echo -e "✅ Database server (PostgreSQL, MySQL)"
        echo -e "✅ Caching layer"
    fi

    # Large disk recommendations
    if [ "$disk_gb" -ge 1000 ]; then
        echo -e "✅ Storage server (NFS, object storage)"
        echo -e "✅ Log aggregation (ELK stack)"
        echo -e "✅ Backup server"
    fi

    # For balanced systems
    if [ "$cpu_cores" -ge 8 ] && [ "$ram_gb" -ge 16 ] && [ "$disk_gb" -ge 100 ]; then
        echo -e "✅ General-purpose application server"
        echo -e "✅ Kubernetes node"
    fi

    # For smaller systems
    if [ "$cpu_cores" -lt 8 ] || [ "$ram_gb" -lt 16 ]; then
        echo -e "✅ Monitoring server (Prometheus, Grafana)"
        echo -e "✅ Load balancer / reverse proxy (Nginx, HAProxy)"
        echo -e "✅ CI/CD coordinator (not runners)"
    fi
}

# Function to analyze server hardware
analyze_server() {
    local server_name=$1
    local server_details=$(get_server_details "$server_name")

    if [ -z "$server_details" ]; then
        echo -e "${RED}Error: Server '$server_name' not found in inventory.${NC}"
        return 1
    fi

    # Parse server details
    local ip=$(echo "$server_details" | cut -d',' -f2)
    local username=$(echo "$server_details" | cut -d',' -f3)
    local key_path=$(echo "$server_details" | cut -d',' -f4)
    local description=$(echo "$server_details" | cut -d',' -f5)

    echo -e "${BLUE}Analyzing server:${NC} $server_name ($ip) - $description"

    # Run hardware analysis commands via SSH
    echo -e "${YELLOW}Connecting to $server_name...${NC}"

    # Check if we can connect
    if ! ssh $SSH_OPTS -i "$key_path" "$username@$ip" "exit" 2>/dev/null; then
        echo -e "${RED}Error: Could not connect to $server_name ($ip).${NC}"
        return 1
    fi

    # Get CPU info
    local cpu_info=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" "lscpu | grep -E 'Model name|CPU\(s\):' | head -2")
    local cpu_model=$(echo "$cpu_info" | grep "Model name" | cut -d':' -f2- | xargs)
    local cpu_cores=$(echo "$cpu_info" | grep "CPU(s):" | head -1 | cut -d':' -f2- | xargs)

    # Get memory info
    local mem_info=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" "free -h | grep Mem:")
    local mem_total=$(echo "$mem_info" | awk '{print $2}')
    local mem_gb=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" "free -g | grep Mem:" | awk '{print $2}')

    # Get disk info - NEW METHOD THAT WORKS
    local disk_gb=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" 'grep " sd[a-z]$" /proc/partitions | awk "{print int(\$3/1024/1024)}"')

    # Try to determine disk type (SSD or HDD)
    local disk_type=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" "lsblk -d -o name,rota | grep -v 'loop' | head -2 | tail -1" | awk '{print $2=="0" ? "SSD" : "HDD"}')

    # Get OS info
    local os_info=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" "cat /etc/os-release | grep PRETTY_NAME" | cut -d'"' -f2)

    # Get load average
    local load_avg=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" "cat /proc/loadavg" | awk '{print $1, $2, $3}')

    # Display hardware info
    echo -e "\n${GREEN}Server Specifications:${NC}"
    echo -e "🖥️  CPU:       $cpu_model ($cpu_cores cores)"
    echo -e "🧠 Memory:    $mem_total total"
    echo -e "💾 Disk:      ${disk_gb}GB total, $disk_type"
    echo -e "🐧 OS:        $os_info"
    echo -e "⚡ Load Avg:  $load_avg (1, 5, 15 min)"

    # Provide recommendations
    echo -e "\n${GREEN}Recommendations:${NC}"
    recommend_role "$cpu_cores" "$mem_gb" "$disk_gb" "$disk_type"

    return 0
}

# Function to analyze all servers and provide cluster recommendations
analyze_all_servers() {
    echo -e "${BLUE}Analyzing all servers in inventory...${NC}"

    # Get all server names
    local server_names=$(awk -F, 'NR>1 {print $1}' "$INVENTORY_FILE")

    # Initialize arrays to store server data
    declare -a all_servers=()
    declare -a server_cpu_cores=()
    declare -a server_mem_gb=()
    declare -a server_disk_gb=()
    declare -a server_disk_type=()
    declare -a server_ips=()

    # Initialize counters
    local high_cpu=0
    local high_mem=0
    local high_storage=0
    local ssd_servers=0
    local total_servers=0

    # Track successful analyses
    local success_count=0

    # Analyze each server
    for server in $server_names; do
        echo -e "\n${PURPLE}======================================${NC}"
        if analyze_server "$server"; then
            success_count=$((success_count + 1))

            # Get server details for classification
            local server_details=$(get_server_details "$server")
            local ip=$(echo "$server_details" | cut -d',' -f2)
            local username=$(echo "$server_details" | cut -d',' -f3)
            local key_path=$(echo "$server_details" | cut -d',' -f4)

            # Get server specs for classification
            local cpu_cores=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" "lscpu | grep 'CPU(s):' | head -1" | cut -d':' -f2- | xargs)
            local mem_gb=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" "free -g | grep Mem:" | awk '{print $2}')

            # NEW METHOD FOR DISK SIZE THAT WORKS
            local disk_gb=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" 'grep " sd[a-z]$" /proc/partitions | awk "{print int(\$3/1024/1024)}"')

            local disk_type=$(ssh $SSH_OPTS -i "$key_path" "$username@$ip" "lsblk -d -o name,rota | grep -v 'loop' | head -2 | tail -1" | awk '{print $2=="0" ? "SSD" : "HDD"}')

            # Store server data in arrays
            all_servers+=("$server")
            server_cpu_cores+=("$cpu_cores")
            server_mem_gb+=("$mem_gb")
            server_disk_gb+=("$disk_gb")
            server_disk_type+=("$disk_type")
            server_ips+=("$ip")

            # Classify servers
            if [ "$cpu_cores" -ge 16 ]; then
                high_cpu=$((high_cpu + 1))
            fi

            if [ "$mem_gb" -ge 64 ]; then
                high_mem=$((high_mem + 1))
            fi

            if [ "$disk_gb" -ge 1000 ]; then
                high_storage=$((high_storage + 1))
            fi

            if [[ "$disk_type" == "SSD" ]]; then
                ssd_servers=$((ssd_servers + 1))
            fi

            total_servers=$((total_servers + 1))
        fi
    done

    # Display cluster-wide recommendations
    echo -e "\n${PURPLE}======================================${NC}"
    echo -e "${BLUE}Cluster Analysis Summary:${NC}"
    echo -e "Total servers: $total_servers (Successfully analyzed: $success_count)"
    echo -e "High CPU servers (16+ cores): $high_cpu"
    echo -e "High Memory servers (64+ GB): $high_mem"
    echo -e "High Storage servers (1+ TB): $high_storage"
    echo -e "SSD-equipped servers: $ssd_servers"

    echo -e "\n${GREEN}General Cluster Recommendations:${NC}"

    # General recommendations based on cluster composition
    if [ "$total_servers" -lt 3 ]; then
        echo -e "• Your cluster is small. Consider a general-purpose setup with:"
        echo -e "  - Combined app + database server"
        echo -e "  - Combined monitoring + CI/CD server"
    else
        echo -e "• Consider separating roles into dedicated servers:"
        echo -e "  - Application servers"
        echo -e "  - Database servers"
        echo -e "  - Monitoring and logging"
        echo -e "  - CI/CD infrastructure"
    fi

    # Specific recommendations based on hardware distribution
    if [ "$high_cpu" -eq 0 ]; then
        echo -e "• No high-CPU servers detected. Consider adding servers with 16+ cores for compute-intensive workloads."
    fi

    if [ "$high_mem" -eq 0 ]; then
        echo -e "• No high-memory servers detected. Consider adding servers with 64+ GB RAM for memory-intensive applications."
    fi

    if [ "$high_storage" -eq 0 ]; then
        echo -e "• No high-storage servers detected. Consider adding servers with 1+ TB storage for data-intensive applications."
    fi

    if [ "$ssd_servers" -eq 0 ]; then
        echo -e "• No SSD-equipped servers detected. Consider adding servers with SSDs for database and I/O-intensive workloads."
    fi

    # Create an array to track if a server has been assigned a role
    declare -a server_assigned=()
    for ((i=0; i<$total_servers; i++)); do
        server_assigned[$i]=0
    done

    # Function to find the best server for a role based on specific criteria
    find_best_server() {
        local role="$1"
        local best_idx=-1
        local best_score=0

        for ((i=0; i<$total_servers; i++)); do
            # Skip already assigned servers if we have enough servers
            if [ ${server_assigned[$i]} -eq 1 ] && [ $total_servers -gt 2 ]; then
                continue
            fi

            local score=0
            local cpu=${server_cpu_cores[$i]}
            local mem=${server_mem_gb[$i]}
            local disk=${server_disk_gb[$i]}
            local disk_type=${server_disk_type[$i]}
            local ssd_bonus=0

            # SSD bonus
            if [[ "$disk_type" == "SSD" ]]; then
                ssd_bonus=20
            fi

            case "$role" in
                "database")
                    # Database servers benefit from SSD, memory, and moderate CPU
                    score=$((ssd_bonus + mem / 2 + cpu / 4))
                    ;;
                "application")
                    # App servers benefit from balanced CPU and memory
                    score=$((cpu / 2 + mem / 4 + ssd_bonus / 4))
                    ;;
                "monitoring")
                    # Monitoring needs less resources
                    score=$((cpu / 4 + mem / 8))
                    ;;
                "storage")
                    # Storage servers benefit from disk size
                    score=$((disk / 10 + ssd_bonus / 10))
                    ;;
                "cicd")
                    # CI/CD benefits from CPU and memory
                    score=$((cpu / 2 + mem / 4))
                    ;;
            esac

            if [ $score -gt $best_score ]; then
                best_score=$score
                best_idx=$i
            fi
        done

        echo $best_idx
    }

    # Apply specific server role recommendations based on the number of servers
    echo -e "\n${BLUE}Specific Server Role Recommendations:${NC}"

    if [ "$total_servers" -eq 1 ]; then
        echo -e "• With only one server, ${YELLOW}${all_servers[0]}${NC} (${server_ips[0]}) should be configured as an all-in-one server:"
        echo -e "  - Combined application, database, monitoring, and CI/CD"
        echo -e "  - Consider adding more servers for better separation of concerns and redundancy"

    elif [ "$total_servers" -eq 2 ]; then
        # For 2 servers, find the best database server
        local db_idx=$(find_best_server "database")
        server_assigned[$db_idx]=1
        local db_server=${all_servers[$db_idx]}
        local db_ip=${server_ips[$db_idx]}

        # The other server becomes the application server
        local app_idx=-1
        for ((i=0; i<$total_servers; i++)); do
            if [ $i -ne $db_idx ]; then
                app_idx=$i
                break
            fi
        done
        server_assigned[$app_idx]=1
        local app_server=${all_servers[$app_idx]}
        local app_ip=${server_ips[$app_idx]}

        echo -e "• ${YELLOW}$db_server${NC} ($db_ip) should be your Database + Monitoring server:"
        echo -e "  - Database role: PostgreSQL/MySQL ($(if [[ "${server_disk_type[$db_idx]}" == "SSD" ]]; then echo "SSD detected - excellent for database"; else echo "Consider adding an SSD for better performance"; fi))"
        echo -e "  - Monitoring: Prometheus + Grafana"
        echo -e "  - Hardware: ${server_cpu_cores[$db_idx]} CPU cores, ${server_mem_gb[$db_idx]}GB RAM, ${server_disk_gb[$db_idx]}GB ${server_disk_type[$db_idx]}"

        echo -e "\n• ${YELLOW}$app_server${NC} ($app_ip) should be your Application + CI/CD server:"
        echo -e "  - Application server: Web servers, API services, application logic"
        echo -e "  - CI/CD: Jenkins, GitLab CI, or similar"
        echo -e "  - Hardware: ${server_cpu_cores[$app_idx]} CPU cores, ${server_mem_gb[$app_idx]}GB RAM, ${server_disk_gb[$app_idx]}GB ${server_disk_type[$app_idx]}"

    elif [ "$total_servers" -eq 3 ]; then
        # For 3 servers, find the best for each primary role
        local db_idx=$(find_best_server "database")
        server_assigned[$db_idx]=1
        local db_server=${all_servers[$db_idx]}
        local db_ip=${server_ips[$db_idx]}

        local app_idx=$(find_best_server "application")
        server_assigned[$app_idx]=1
        local app_server=${all_servers[$app_idx]}
        local app_ip=${server_ips[$app_idx]}

        # Find the remaining server for monitoring/CI/CD
        local monitor_idx=-1
        for ((i=0; i<$total_servers; i++)); do
            if [ $i -ne $db_idx ] && [ $i -ne $app_idx ]; then
                monitor_idx=$i
                break
            fi
        done
        server_assigned[$monitor_idx]=1
        local monitor_server=${all_servers[$monitor_idx]}
        local monitor_ip=${server_ips[$monitor_idx]}

        echo -e "• ${YELLOW}$db_server${NC} ($db_ip) should be your dedicated Database server:"
        echo -e "  - Primary role: PostgreSQL/MySQL/Redis"
        echo -e "  - Hardware: ${server_cpu_cores[$db_idx]} CPU cores, ${server_mem_gb[$db_idx]}GB RAM, ${server_disk_gb[$db_idx]}GB ${server_disk_type[$db_idx]}"
        echo -e "  - $(if [[ "${server_disk_type[$db_idx]}" == "SSD" ]]; then echo "SSD detected - excellent for database workloads"; else echo "Consider adding an SSD for better database performance"; fi)"

        echo -e "\n• ${YELLOW}$app_server${NC} ($app_ip) should be your dedicated Application server:"
        echo -e "  - Primary role: Web servers, API services, application logic"
        echo -e "  - Hardware: ${server_cpu_cores[$app_idx]} CPU cores, ${server_mem_gb[$app_idx]}GB RAM, ${server_disk_gb[$app_idx]}GB ${server_disk_type[$app_idx]}"
        echo -e "  - $(if [ ${server_cpu_cores[$app_idx]} -ge 8 ]; then echo "Good CPU core count for application workloads"; else echo "Consider adding more CPU resources for better application performance"; fi)"

        echo -e "\n• ${YELLOW}$monitor_server${NC} ($monitor_ip) should be your Monitoring + CI/CD server:"
        echo -e "  - Monitoring: Prometheus, Grafana, ELK stack"
        echo -e "  - CI/CD: Jenkins, GitLab CI, GitHub Actions runners"
        echo -e "  - Hardware: ${server_cpu_cores[$monitor_idx]} CPU cores, ${server_mem_gb[$monitor_idx]}GB RAM, ${server_disk_gb[$monitor_idx]}GB ${server_disk_type[$monitor_idx]}"

    else
        # For 4+ servers, find the best for each role
        local db_idx=$(find_best_server "database")
        server_assigned[$db_idx]=1
        local db_server=${all_servers[$db_idx]}
        local db_ip=${server_ips[$db_idx]}

        local app_idx=$(find_best_server "application")
        server_assigned[$app_idx]=1
        local app_server=${all_servers[$app_idx]}
        local app_ip=${server_ips[$app_idx]}

        local monitor_idx=$(find_best_server "monitoring")
        server_assigned[$monitor_idx]=1
        local monitor_server=${all_servers[$monitor_idx]}
        local monitor_ip=${server_ips[$monitor_idx]}

        local cicd_idx=$(find_best_server "cicd")
        server_assigned[$cicd_idx]=1
        local cicd_server=${all_servers[$cicd_idx]}
        local cicd_ip=${server_ips[$cicd_idx]}

        # Find any remaining unassigned servers
        local remaining_servers=""
        for ((i=0; i<$total_servers; i++)); do
            if [ ${server_assigned[$i]} -eq 0 ]; then
                remaining_servers="${remaining_servers}• ${YELLOW}${all_servers[$i]}${NC} (${server_ips[$i]}): Secondary application server or specialized role\n"
            fi
        done

        echo -e "• ${YELLOW}$db_server${NC} ($db_ip) should be your dedicated Database server:"
        echo -e "  - Primary role: PostgreSQL/MySQL/Redis"
        echo -e "  - Hardware: ${server_cpu_cores[$db_idx]} CPU cores, ${server_mem_gb[$db_idx]}GB RAM, ${server_disk_gb[$db_idx]}GB ${server_disk_type[$db_idx]}"
        echo -e "  - $(if [[ "${server_disk_type[$db_idx]}" == "SSD" ]]; then echo "SSD detected - excellent for database workloads"; else echo "Consider adding an SSD for better database performance"; fi)"

        echo -e "\n• ${YELLOW}$app_server${NC} ($app_ip) should be your primary Application server:"
        echo -e "  - Primary role: Web servers, API services, application logic"
        echo -e "  - Hardware: ${server_cpu_cores[$app_idx]} CPU cores, ${server_mem_gb[$app_idx]}GB RAM, ${server_disk_gb[$app_idx]}GB ${server_disk_type[$app_idx]}"

        echo -e "\n• ${YELLOW}$monitor_server${NC} ($monitor_ip) should be your Monitoring server:"
        echo -e "  - Primary role: Prometheus, Grafana, ELK stack"
        echo -e "  - Hardware: ${server_cpu_cores[$monitor_idx]} CPU cores, ${server_mem_gb[$monitor_idx]}GB RAM, ${server_disk_gb[$monitor_idx]}GB ${server_disk_type[$monitor_idx]}"

        echo -e "\n• ${YELLOW}$cicd_server${NC} ($cicd_ip) should be your CI/CD server:"
        echo -e "  - Primary role: Jenkins, GitLab CI, GitHub Actions runners"
        echo -e "  - Hardware: ${server_cpu_cores[$cicd_idx]} CPU cores, ${server_mem_gb[$cicd_idx]}GB RAM, ${server_disk_gb[$cicd_idx]}GB ${server_disk_type[$cicd_idx]}"

        if [ -n "$remaining_servers" ]; then
            echo -e "\nAdditional servers that can be utilized:"
            echo -e "$remaining_servers"
        fi
    fi

    # Provide hardware upgrade recommendations if needed
    echo -e "\n${BLUE}Hardware Upgrade Recommendations:${NC}"
    for ((i=0; i<$total_servers; i++)); do
        local upgrade_needed=false
        local upgrade_message=""

        # Check if the server has less than 4 CPU cores
        if [ ${server_cpu_cores[$i]} -lt 4 ]; then
            upgrade_needed=true
            upgrade_message="${upgrade_message}  - Add more CPU cores (currently ${server_cpu_cores[$i]})\n"
        fi

        # Check if the server has less than 8GB of RAM
        if [ ${server_mem_gb[$i]} -lt 8 ]; then
            upgrade_needed=true
            upgrade_message="${upgrade_message}  - Increase RAM (currently ${server_mem_gb[$i]}GB)\n"
        fi

        # Check for HDD on database servers
        if [[ "${server_disk_type[$i]}" != "SSD" ]] && [ $i -eq $db_idx ]; then
            upgrade_needed=true
            upgrade_message="${upgrade_message}  - Add an SSD for database performance\n"
        fi

        if [ "$upgrade_needed" = true ]; then
            echo -e "• ${YELLOW}${all_servers[$i]}${NC} (${server_ips[$i]}) recommended upgrades:"
            echo -e "$upgrade_message"
        fi
    done
}

# Function to connect to a server
connect_to_server() {
    local server_name=$1
    local server_details=$(get_server_details "$server_name")

    if [ -z "$server_details" ]; then
        echo -e "${RED}Error: Server '$server_name' not found in inventory.${NC}"
        return 1
    fi

    local ip=$(echo "$server_details" | cut -d',' -f2)
    local username=$(echo "$server_details" | cut -d',' -f3)
    local key_path=$(echo "$server_details" | cut -d',' -f4)
    local description=$(echo "$server_details" | cut -d',' -f5)

    echo -e "${BLUE}Connecting to server:${NC} $server_name ($ip) - $description"

    # Connect to the server using SSH
    ssh $SSH_OPTS -i "$key_path" "$username@$ip"
}

# Main logic
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    show_usage
    exit 0
fi

case "$1" in
    list)
        list_servers
        ;;
    connect)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Missing server name.${NC}"
            show_usage
            exit 1
        fi
        connect_to_server "$2"
        ;;
    analyze)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Missing server name.${NC}"
            show_usage
            exit 1
        fi
        analyze_server "$2"
        ;;
    analyze-all)
        analyze_all_servers
        ;;
    add)
        add_server
        ;;
    remove)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Missing server name.${NC}"
            show_usage
            exit 1
        fi
        remove_server "$2"
        ;;
    *)
        show_usage
        ;;
esac
