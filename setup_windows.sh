# Update and upgrade the package lists
sudo apt update && sudo apt upgrade -y

# Add 'solid' to the 'sudo' group to grant administrative privileges
sudo usermod -aG sudo solid

# Install prerequisite packages for Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker's repository to APT sources
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package lists to include Docker's packages
sudo apt update

# Install Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Add 'solid' to the 'docker' group to allow Docker command usage without sudo
sudo usermod -aG docker solid

# Install Git
sudo apt install -y git

# Install Docker Compose for all users
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Verify Docker installation
docker --version

# Verify Docker Compose installation
docker compose version

# Verify Git installation
git --version
