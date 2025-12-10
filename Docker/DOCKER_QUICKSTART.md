# DOCKER QUICK START - 3D Zebrafish nnUNet

5-minute setup guide for the Docker container.

---

## Step 1: Prerequisites (One-time setup)

```bash
# Install Docker (Ubuntu/Linux)
sudo apt-get update && sudo apt-get install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
# Log out and log back in

# Install NVIDIA Docker (for GPU)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Test GPU
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

---

## Step 2: Get the Files

```bash
# Clone repository
git clone https://github.com/JuhyunLeeLab/3D-Zebrafish-nnUNet.git
cd 3D-Zebrafish-nnUNet

# Add Docker files to repository root:
# - Dockerfile
# - docker-compose.yml
# - .dockerignore
# - DOCKER_SETUP.md
```

---

## Step 3: Build and Run

```bash
# Build container (takes ~10-15 minutes first time)
docker-compose build

# Start container
docker-compose up -d

# Access container
docker-compose exec zebrafish-nnunet bash

# You're now inside the container!
```

---

## Step 4: Verify Installation

Inside the container:

```bash
# Check Python
python --version  # Should show Python 3.10

# Check PyTorch + CUDA
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"

# Check nnU-Net
python -c "import nnunetv2; print('nnU-Net installed successfully')"

# Check GPU
nvidia-smi
```

---

## Step 5: Run Your First Job

```bash
# Inside container
cd /workspace/3D-Zebrafish-nnUNet

# Convert your data (place raw images in data/ori, segmentations in data/segmented)
pdm run python -m src.dc --tod --name zebrafish_test --t 777

# Plan and preprocess
pdm run nnUNetv2_plan_and_preprocess -d 777 -c 3d_fullres

# Train (this will take hours depending on data size)
pdm run nnUNetv2_train 777 3d_fullres 0

# Results will be in data/results/
```

---

## Common Commands

```bash
# Start container
docker-compose up -d

# Access container
docker-compose exec zebrafish-nnunet bash

# Stop container
docker-compose down

# View logs
docker-compose logs -f

# Check GPU usage
docker exec zebrafish-container nvidia-smi
```

---

## Folder Structure

```
Your data should be organized as:
data/
├── ori/              # Your raw .tif/.tiff images
├── segmented/        # Your ground truth segmentations
├── raw/             # Auto-generated nnU-Net format
├── preprocessed/    # Auto-generated
├── results/         # Training outputs
└── inference/       # For running predictions
    ├── input/       # Put test images here
    └── output/      # Predictions appear here
```

---

## Troubleshooting

**Container won't start:**
```bash
docker-compose down
docker-compose up
```

**GPU not detected:**
```bash
# Inside container
nvidia-smi  # Should show your GPU

# If fails, restart Docker
sudo systemctl restart docker
```

**Permission errors:**
```bash
# Make sure data directories exist
mkdir -p data/ori data/segmented data/results
chmod -R 777 data/
```

**Out of memory:**
```bash
# Edit docker-compose.yml, add under 'deploy':
    resources:
      limits:
        memory: 32G
```

---

## Next Steps

- Read full documentation: `DOCKER_SETUP.md`
- Check nnU-Net docs: https://github.com/MIC-DKFZ/nnUNet
- Customize training parameters in nnU-Net config files

---

**You're all set!** 🐳🐟

For questions, open an issue on GitHub:
https://github.com/JuhyunLeeLab/3D-Zebrafish-nnUNet/issues
