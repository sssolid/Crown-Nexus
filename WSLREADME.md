# ========================
# 🔥 FIX WSL PERMISSIONS
# ========================

# 1️⃣ Check ownership of a file
ls -l ./crown_deploy/test-output/server3/rollback.sh
# Output format: "-rwxr-xr-x 1 root root 491 Mar 10 16:23 rollback.sh"
# If the owner is "root", you might need to change ownership.

# 2️⃣ Change ownership of the entire project to your user (inside WSL)
sudo chown -R $(whoami):$(whoami) /mnt/d/crown-nexus
# ⚠️ This only works if the project is in the WSL filesystem.
# If your project is inside /mnt/d/, see the metadata mounting fix below.

# 3️⃣ Change file permissions to allow writing
chmod -R u+rw /mnt/d/crown-nexus
# This ensures you can edit files.

# ========================
# 🔄 CONVERT LINE ENDINGS
# ========================

# 4️⃣ Convert all .sh scripts to Unix line endings
find . -type f -name "*.sh" -exec dos2unix {} +
# Fixes issues where Windows-style CRLF line endings cause script failures.

# 5️⃣ Find files with Windows-style line endings (^M characters)
grep -rl $'\r' .
# Identifies problem files before running dos2unix.

# ========================
# 🔧 WSL-SPECIFIC FIXES
# ========================

# 6️⃣ Remount Windows drive with metadata support (fixes chown & chmod issues)
sudo umount /mnt/d
sudo mount -t drvfs D: /mnt/d -o metadata
# This enables Linux-style permissions on Windows-mounted drives.

# 7️⃣ Make the metadata mount option permanent
echo -e "[automount]\noptions = \"metadata\"" | sudo tee -a /etc/wsl.conf
# Restart WSL to apply changes
wsl --shutdown

# ========================
# 🚀 MAKE SCRIPTS EXECUTABLE
# ========================

# 8️⃣ Give execute (+x) permissions to all .sh scripts
find . -type f -name "*.sh" -exec chmod +x {} \;

# 9️⃣ Verify that .sh files are executable
ls -l **/*.sh
# Look for "-rwxr-xr-x" (instead of "-rw-r--r--").

# 🔟 Only apply +x to scripts that don't already have execute permissions
find . -type f -name "*.sh" ! -perm /u+x -exec chmod u+x {} \;

# ========================
# 🛠️ WINDOWS-BASED FIXES (If WSL is still acting up)
# ========================

# 1️⃣1️⃣ Remove Windows Read-Only attributes from all files in PowerShell (Run as Admin)
powershell -Command "Get-ChildItem -Path 'D:\crown-nexus' -Recurse | ForEach-Object { $_.Attributes -= 'ReadOnly' }"

# 1️⃣2️⃣ Convert line endings from PowerShell (Run in Windows Terminal)
powershell -Command "(Get-Content D:\crown-nexus\crown_deploy\test-output\server3\rollback.sh) | Set-Content -NoNewline D:\crown-nexus\crown_deploy\test-output\server3\rollback.sh"

# ==============================
# SYSTEM INFORMATION & CHECKS
# ==============================

# Check Ubuntu version
lsb_release -a    # Displays detailed Ubuntu version information
cat /etc/os-release   # Shows OS details from the system file
hostnamectl    # Displays system hostname and OS details
uname -r   # Shows the kernel version

# ==============================
# USER MANAGEMENT
# ==============================

# Create a new user named 'solid'
sudo adduser solid

# Add 'solid' user to sudo group for administrative privileges
sudo usermod -aG sudo solid

# Add 'solid' user to docker group to allow Docker commands without sudo
sudo usermod -aG docker solid

# Check which groups a user belongs to
groups solid

# ==============================
# SSH CONFIGURATION
# ==============================

# Create SSH directory for 'solid' user
mkdir -p /home/solid/.ssh

# Copy SSH key from root to 'solid' user for key-based authentication
cp /root/.ssh/authorized_keys /home/solid/.ssh/

# Set correct ownership and permissions for SSH directory and keys
chown -R solid:solid /home/solid/.ssh
chmod 700 /home/solid/.ssh
chmod 600 /home/solid/.ssh/authorized_keys

# Disable root login and password authentication in SSH (script version)
sudo sed -i 's/^#\?\(PermitRootLogin\) .*/\1 no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?\(PasswordAuthentication\) .*/\1 no/' /etc/ssh/sshd_config

# Restart SSH service to apply changes
sudo systemctl restart ssh

# ==============================
# DOCKER & DOCKER COMPOSE INSTALLATION
# ==============================

# Update system package lists
sudo apt update && sudo apt upgrade -y

# Install prerequisite packages for Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker's official repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package lists to include Docker packages
sudo apt update

# Install Docker and its components
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Verify Docker installation
docker --version

# ==============================
# DOCKER COMPOSE INSTALLATION & FIXES
# ==============================

# Check if Docker Compose (V2) is available
docker compose version

# If necessary, manually install Docker Compose
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose

# If 'docker-compose' command is missing, create a symlink
sudo ln -s /usr/bin/docker /usr/local/bin/docker-compose

# Verify the installation of Docker Compose
docker-compose version

# ==============================
# OTHER SYSTEM UTILITIES
# ==============================

# Install Git
sudo apt install -y git

# Verify Git installation
git --version

# Install system monitoring tool (htop)
sudo apt install -y htop

# Enable and configure Uncomplicated Firewall (UFW) for SSH access
sudo apt install -y ufw
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status

# Enable automatic security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades

# 🚀 STEP 1: INSTALL WSL & UBUNTU
# --------------------------------
# If WSL and Ubuntu are not installed yet, install them:

wsl --install -d Ubuntu-22.04
# Restart your computer if required.

# Check that Ubuntu-22.04 is installed:
wsl -l -v

# If Ubuntu-22.04 is installed but not default, set it as default:
wsl --set-default Ubuntu-22.04

# Restart WSL to apply changes:
wsl --shutdown

# Open WSL to verify it works:
wsl -d Ubuntu-22.04

# 🚀 STEP 2: INSTALL PYTHON & CREATE A VIRTUAL ENVIRONMENT
# -------------------------------------------------------
# Inside WSL (Ubuntu-22.04), install Python 3.12 and required dependencies:

sudo apt update && sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Navigate to your project directory (adjust path if necessary):
cd /mnt/d/crown-nexus

# Create a virtual environment inside the project:
python3 -m venv venv

# Activate the virtual environment:
source venv/bin/activate

# Verify that the virtual environment is working:
which python   # Should return: /mnt/d/crown-nexus/venv/bin/python
python --version  # Should return: Python 3.12.x

# 🚀 STEP 3: CONFIGURE INTELLIJ IDEA TO USE WSL
# ---------------------------------------------
# Open IntelliJ IDEA and follow these steps:

# 1. Open IntelliJ and go to: File > Settings > Tools > Terminal
# 2. Set the Shell Path to:
#    wsl.exe -d Ubuntu-22.04 --cd /mnt/d/crown-nexus -e bash --login
# 3. Click OK and restart IntelliJ.

# 🚀 STEP 4: AUTO-ACTIVATE VIRTUAL ENV IN WSL
# -------------------------------------------
# Modify .bashrc to automatically activate the venv when opening WSL:

nano ~/.bashrc

# Add the following lines at the bottom:
if [[ "$PWD" == "/mnt/d/crown-nexus" ]]; then
source venv/bin/activate
fi

# Save and exit (CTRL + X, then Y, then Enter).
# Apply changes:
source ~/.bashrc

# 🚀 STEP 5: ADD WSL PYTHON INTERPRETER TO INTELLIJ IDEA
# ------------------------------------------------------
# 1. Open IntelliJ IDEA and go to: File > Settings > Languages & Frameworks > Python Interpreter
# 2. Click the ⚙️ (gear icon) > "Add Interpreter" > "Add via WSL"
# 3. Select Ubuntu-22.04
# 4. Set the Interpreter Path to:
#    /mnt/d/crown-nexus/venv/bin/python
# 5. Click OK and wait for indexing to complete.

# 🚀 STEP 6: VERIFY EVERYTHING WORKS
# ----------------------------------
# Open IntelliJ IDEA Terminal (View > Tool Windows > Terminal)
# Run:

which python  # Should return: /mnt/d/crown-nexus/venv/bin/python
python --version  # Should return Python 3.12.x

# Try running a Python script to confirm:
python -c "import sys; print(sys.version)"

# If everything works, IntelliJ is now fully configured with WSL and venv!

