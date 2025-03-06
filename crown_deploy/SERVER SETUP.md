### 1. Create a Bootable Ubuntu USB Drive from Windows 11

- **Download the ISO:**
    - Get the Ubuntu ISO (Desktop or Server) from the [Ubuntu website](https://ubuntu.com/download).

- **Create the Bootable USB:**
    - Use a tool like [Rufus](https://rufus.ie) (or [balenaEtcher](https://www.balena.io/etcher/)) to write the ISO to your USB flash drive.
    - Verify that settings such as the partition scheme (MBR or GPT) and file system (FAT) are correct.

---

### 2. Configure a Static IP Address on Ubuntu Server

- **Verify the Current IP Settings:**
    - Run `ip a` to check the current interface configuration.

- **Edit the Netplan Configuration:**
    - Backup the current file:
      ```bash
      sudo cp /etc/netplan/50-cloud-init.yaml /etc/netplan/50-cloud-init.yaml.bak
      ```
    - Open the file with your editor:
      ```bash
      sudo nano /etc/netplan/50-cloud-init.yaml
      ```
    - Change the settings from DHCP to static. For example:
      ```yaml
      network:
        version: 2
        ethernets:
          eno1:
            dhcp4: false
            addresses:
              - 192.168.10.234/24
            nameservers:
              addresses:
                - 8.8.8.8
                - 8.8.4.4
            routes:
              - to: default
                via: 192.168.10.1
      ```
- **Apply and Verify:**
    - Run `sudo netplan apply`.
    - Confirm the new IP using `ip a`.

- **Determine the Gateway:**
    - Run `ip route` to check that the default gateway is correctly set (e.g., `default via 192.168.10.1`).

---

### 3. Set Up SSH Key-Based Authentication

- **Generate an SSH Key Pair on Your Client:**
    - Use a command like:
      ```bash
      ssh-keygen -t ed25519 -C "your_email@example.com"
      ```
    - (Or use RSA if needed: `ssh-keygen -t rsa -b 4096`)

- **Copy Your Public Key to the Server:**
    - Use `ssh-copy-id`:
      ```bash
      ssh-copy-id ryan@nexus-01
      ```
    - Or manually copy the contents of your `~/.ssh/id_ed25519.pub` (or `id_rsa.pub`) to the server’s `~/.ssh/authorized_keys` file.

- **Test Key-Based Login:**
    - Open a new terminal session and connect:
      ```bash
      ssh ryan@nexus-01
      ```
    - Confirm that you can log in without entering your password.

- **Disable Password Authentication (After Confirming Key Login):**
    - Edit the SSH configuration:
      ```bash
      sudo nano /etc/ssh/sshd_config
      ```
    - Set the following parameters:
      ```plaintext
      PasswordAuthentication no
      ChallengeResponseAuthentication no
      PermitRootLogin no   # Optional, for additional security
      ```
    - **Restart the SSH Service:**
        - On Ubuntu, use:
          ```bash
          sudo systemctl restart ssh
          ```
    - **Test Again:**
        - Open a new terminal and verify that only key-based login is allowed.

---

### 4. Map the Hostname on Windows 11

- **Edit the Hosts File on Windows:**
    - Open Notepad as an Administrator.
    - Open the file located at:
      ```
      C:\Windows\System32\drivers\etc\hosts
      ```
    - Add an entry like:
      ```
      192.168.10.234 nexus-01
      ```
    - Save the file.

- **Test Name Resolution:**
    - Open Command Prompt and run:
      ```cmd
      ping nexus-01
      ```
    - Ensure it resolves to the correct IP.

---

### 5. Backup Your SSH Private Key

- **Important:**
    - Only the private key (e.g., `id_rsa` or `id_ed25519`) needs to be backed up.
    - Store the private key in a secure location (encrypted external drive or secure cloud storage) to ensure you can recover access if it is ever lost.
