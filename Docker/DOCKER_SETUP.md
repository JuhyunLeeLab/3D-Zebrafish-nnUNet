# DOCKER SETUP GUIDE

Complete guide for setting up the 3D Zebrafish nnUNet platform using Docker.

================================================================================
PREREQUISITES
================================================================================

Required:
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- NVIDIA Docker runtime (for GPU support)
- NVIDIA GPU with CUDA support

Tested on:
- Windows 11 with WSL2 + Docker Desktop
- Ubuntu 22.04 with Docker Engine
- GPUs: RTX 2080 Ti, RTX 4090

================================================================================
INSTALLATION
================================================================================

Step 1: Install Docker
----------------------

**Windows:**
1. Download Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Choose "Download for Windows AMD64"
3. Run installer, enable "Use WSL 2 instead of Hyper-V"
4. Restart computer
5. Launch Docker Desktop

**Linux:**
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

**Verify installation:**
```bash
docker --version
# Expected: Docker version 24.x.x or higher
```

Step 2: Install NVIDIA Docker Runtime (GPU Support)
----------------------------------------------------

**Windows (WSL2):**
```bash
# In WSL2 Ubuntu terminal
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/deb/\$(ARCH) /" | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker Desktop (right-click whale icon → Restart)
```

**Linux:**
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/deb/\$(ARCH) /" | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

**Test GPU access:**
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
# Should display your GPU information
```

Step 3: Clone Repository
-------------------------

```bash
git clone https://github.com/JuhyunLeeLab/3D-Zebrafish-nnUNet.git
cd 3D-Zebrafish-nnUNet
```

================================================================================
USAGE
================================================================================

Build and Start Container
--------------------------

```bash
# Build the Docker image (takes 10-15 minutes first time)
docker compose build

# Start container in background
docker compose up -d

# Verify container is running
docker compose ps
# Should show: zebrafish-nnunet   Up
```

Access Container
----------------

```bash
# Enter the container
docker compose exec zebrafish-nnunet bash

# You're now inside the container at: /workspace/zebrafish
```

Run Your Workflow
-----------------

Inside the container, run your pipeline:

```bash
# Check GPU is accessible
nvidia-smi

# Check environment
echo $nnUNet_raw
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Dataset conversion
pdm run python -m src.dc --tod \
  --ori data/ori \
  --seg data/segmented \
  --name zebrafish_test \
  --t 777

# Plan and preprocess
pdm run nnUNetv2_plan_and_preprocess -d 777 -c 3d_fullres --verify_dataset_integrity

# Train
pdm run nnUNetv2_train 777 3d_fullres 0

# Inference
pdm run nnUNetv2_predict \
  -i data/inference/input \
  -o data/inference/output \
  -d 777 \
  -c 3d_fullres \
  -f 0
```

Exit and Stop
-------------

```bash
# Exit container
exit

# Stop container
docker compose down
```

================================================================================
KEY FEATURES
================================================================================

**Included in Container:**
- Ubuntu 22.04 with CUDA 11.8
- Python 3.10
- PyTorch 2.7.1 with GPU support
- nnU-Net v2 (from source)
- All dependencies (scipy, scikit-image, tifffile, tqdm, rich, etc.)
- Pre-configured environment variables

**Your Files:**
- Your local repository is mounted at `/workspace/zebrafish`
- Edit files on your machine → changes appear immediately in container
- Data persists in `data/` directory on your local machine

**Multi-GPU Support:**
- Automatically detects all GPUs
- Control with `CUDA_VISIBLE_DEVICES` environment variable
- Edit in docker-compose.yml: `CUDA_VISIBLE_DEVICES=0,1`

================================================================================
TROUBLESHOOTING
================================================================================

Container Won't Start
---------------------
```bash
# Check Docker is running
docker ps

# View logs
docker compose logs

# Restart Docker
# Windows: Right-click whale icon → Restart
# Linux: sudo systemctl restart docker
```

GPU Not Detected
----------------
```bash
# Test GPU access
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# If fails, reinstall NVIDIA Container Toolkit (Step 2 above)

# Check NVIDIA drivers
nvidia-smi  # On host system
```

Out of Memory
-------------
- Close other GPU applications
- Reduce batch size in nnU-Net
- Use single GPU: `CUDA_VISIBLE_DEVICES=0`
- Increase Docker memory limit (Docker Desktop Settings → Resources)

Build Fails
-----------
```bash
# Clean rebuild
docker compose down
docker system prune -a  # Warning: removes all unused images
docker compose build --no-cache
```

Permission Denied on Data
-------------------------
```bash
# Fix permissions
chmod -R 777 data/
# Or use your user:
sudo chown -R $USER:$USER data/
```

Slow Performance
----------------
**Windows Users:**
- Store project in WSL2 filesystem (not /mnt/c/)
- Faster: `~/3D-Zebrafish-nnUNet`
- Slower: `/mnt/c/Users/.../3D-Zebrafish-nnUNet`

Increase WSL2 resources:
Create `C:\Users\YourName\.wslconfig`:
```ini
[wsl2]
memory=32GB
processors=16
```
Then restart: `wsl --shutdown`

================================================================================
WORKFLOW TIPS
================================================================================

Edit Code Locally, Run in Docker
---------------------------------
1. Edit files on your machine (VS Code, PyCharm, etc.)
2. Changes appear immediately in container
3. Run commands inside container

Check GPU Usage During Training
--------------------------------
```bash
# In another terminal (outside container)
docker exec zebrafish-nnunet nvidia-smi

# Or continuously monitor
watch -n 1 docker exec zebrafish-nnunet nvidia-smi
```

Use Specific GPU
----------------
Edit `docker-compose.yml`:
```yaml
environment:
  - CUDA_VISIBLE_DEVICES=0  # Use GPU 0 only
  - CUDA_VISIBLE_DEVICES=0,1  # Use GPUs 0 and 1
```

Keep Container Running
----------------------
```bash
# Container runs in background with: docker compose up -d
# Access anytime with: docker compose exec zebrafish-nnunet bash
# Stop when finished: docker compose down
```

================================================================================
COMPUTATIONAL REQUIREMENTS
================================================================================

Minimum Configuration:
- GPU: NVIDIA RTX 3080 (10GB VRAM)
- CPU: 8+ cores
- RAM: 32 GB
- Storage: 500 GB SSD

Recommended Configuration:
- GPU: NVIDIA RTX 4090 (24GB) or 2× RTX 2080 Ti
- CPU: Intel Core i9-14900K (24 cores)
- RAM: 64 GB DDR5
- Storage: NVMe SSD (1TB+)

Performance:
- Training: ~12 hours per developmental day
- Inference: ~69 seconds per volume (RTX 4090)
- Throughput: ~52 cases per hour

================================================================================
VERIFICATION CHECKLIST
================================================================================

Before running experiments, verify:

[ ] Docker version 24.x or higher
[ ] Container builds without errors
[ ] Container starts successfully
[ ] GPU visible: `docker exec zebrafish-nnunet nvidia-smi`
[ ] PyTorch CUDA: `docker exec zebrafish-nnunet python -c "import torch; print(torch.cuda.is_available())"`
[ ] nnU-Net imports: `docker exec zebrafish-nnunet python -c "import nnunetv2"`
[ ] Repository files accessible in container
[ ] Data directory mounted and writable
[ ] Environment variables set correctly

================================================================================
GETTING HELP
================================================================================

If you encounter issues:
1. Check troubleshooting section above
2. View container logs: `docker compose logs`
3. Open issue on GitHub with error details
4. Contact: juhyun.lee@uta.edu

For Docker installation help:
- Docker docs: https://docs.docker.com/
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/

================================================================================
