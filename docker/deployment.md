# Deployment Guide

## 🚀 Quick Start Deployment (Pre-Built Image)

This project uses a "frozen" Docker image (`codesys-runtime-live:v1`) that contains the fully installed CODESYS Control runtime and Edge Gateway. Follow these steps to deploy the system on a new Linux host without needing to manually install the CODESYS `.deb` packages.

### Prerequisites
* A Linux host (Ubuntu/Debian recommended)
* **Git** installed (`sudo apt install git`)
* **Docker** and **Docker Compose** installed

### Step 1: Clone the Repository
First, download the project files, which include the `docker-compose.yml` and the local volume directory structure.

```bash
git clone https://github.com/attilapeterszucs/Cipher-Bay.git
cd Cipher-Bay/docker
```

### Step 2: Download the Frozen Runtime Image
Because the CODESYS runtime is proprietary and cannot be hosted on public Docker Hub registries, we distribute the pre-built image as a `.tar` archive. Download it directly into your project folder.

```bash
# Example URL - Replace with the actual hosting link for your .tar file
wget https://example.com/downloads/codesys-live-backup.tar
```

### Step 3: Load the Image into Docker
Tell Docker to unpack the `.tar` file and load the `codesys-runtime-live:v1` image into its local registry. Note: Depending on your system configuration, you may need to use `sudo` for Docker commands.

```bash
sudo docker load -i codesys-live-backup.tar
```
You should see an output confirming: `Loaded image: codesys-runtime-live:v1`

### Step 4: Start the System
With the project files in place and the image loaded, you can now spin up the container. The `docker-compose.yml` is configured to use host networking and will automatically boot the PLC, the Edge Gateway, and the SSH daemon.

```bash
sudo docker compose up -d
```

### Step 5: Verify Deployment

**Check Container Status:**
```bash
sudo docker ps
```
Ensure `codesys-runtime` is running and hasn't restarted.

**Access the WebVisu:**
Open a browser on the same network and navigate to:
`http://<SERVER_IP>:8080/webvisu.htm`

**Connect the IDE:**
Open CODESYS on your Windows machine, add a Gateway pointing to `<SERVER_IP>`, and log in to download your latest logic!
