# 3D Zebrafish Cardiac Segmentation Platform

Automated cell tracking platform using 3D nnU-Net and light sheet microscopy to quantify myocardial deformation in zebrafish embryos.

## Overview

This platform provides an integrated pipeline for:
- **3D nuclear segmentation** using nnU-Net with novel preprocessing (DoG + watershed)
- **4D cell tracking** across cardiac cycles using LAP (Linear Assignment Problem) tracking
- **Contractility analysis** for zebrafish cardiac development (Days 3-6)

**Key Features:**
- Robust segmentation across developmental stages with superior cross-day generalization
- Preprocessing pipeline specifically designed for dense cardiac tissue
- Multi-GPU support for high-throughput processing
- Reproducible environment via Docker containerization

## 🐳 Docker Setup (Recommended)

**For reproducible environment with all dependencies pre-installed.**

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/JuhyunLeeLab/3D-Zebrafish-nnUNet.git
cd 3D-Zebrafish-nnUNet

# 2. Build and start container
docker compose up -d

# 3. Access container
docker compose exec zebrafish-nnunet bash

# 4. Inside container - run your workflow
pdm run python -m src.dc --tod --ori data/ori --seg data/segmented --name zebrafish_test --t 777
pdm run nnUNetv2_plan_and_preprocess -d 777 -c 3d_fullres --verify_dataset_integrity
pdm run nnUNetv2_train 777 3d_fullres 0

# 5. Stop when done
docker compose down
```

### Requirements

- **Docker Desktop** with WSL2 (Windows) or **Docker Engine** (Linux)
- **NVIDIA Docker runtime** (for GPU support)
- **NVIDIA GPU** with CUDA support (tested with RTX 2080 Ti, RTX 4090)

### Documentation

- **Complete setup guide:** [DOCKER_SETUP.md](DOCKER_SETUP.md) - Comprehensive 15-page guide with troubleshooting
- **Quick setup (5-10 min):** [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) - Fast track for experienced users

### What's Included in the Container

- Ubuntu 22.04 with CUDA 11.8
- PyTorch 2.7.1 with GPU support
- nnU-Net v2 (installed from source: [MIC-DKFZ/nnUNet](https://github.com/MIC-DKFZ/nnUNet))
- All preprocessing dependencies (scipy, scikit-image, tifffile)
- Pre-configured environment variables
- Multi-GPU support

### Computational Requirements

**Minimum:**
- GPU: NVIDIA RTX 3080 (10GB VRAM)
- CPU: 8+ cores
- RAM: 32 GB
- Storage: 500 GB SSD

**Recommended (used in study):**
- GPU: NVIDIA RTX 4090 (24GB VRAM) or 2× RTX 2080 Ti
- CPU: Intel Core i9-14900K or equivalent
- RAM: 64 GB DDR5
- Storage: NVMe SSD (1TB+)

**Performance:**
- Training: ~12 hours per developmental day
- Inference: ~69 seconds per 3D volume (RTX 4090)
- Throughput: ~52 cases per hour

See [Table 2 in manuscript] for complete performance benchmarks.

---

## 📦 Manual Installation (Alternative)

If you prefer not to use Docker, follow these steps for manual installation.

### Prerequisites

- Python 3.10
- CUDA 11.8 or higher
- Git
- Conda or venv

### Step 1: Create Environment

```bash
# Create conda environment
conda create -n zebrafish_seg python==3.10
conda activate zebrafish_seg

# Verify Python version
python --version  # Should show Python 3.10.x
```

### Step 2: Install PyTorch

```bash
# Install PyTorch with CUDA support
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

### Step 3: Clone and Install nnU-Net

```bash
# Clone nnU-Net repository
git clone https://github.com/MIC-DKFZ/nnUNet.git
cd nnUNet
pip install -e .
pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git
cd ..
```

### Step 4: Clone This Repository

```bash
git clone https://github.com/JuhyunLeeLab/3D-Zebrafish-nnUNet.git
cd 3D-Zebrafish-nnUNet
```

### Step 5: Install Dependencies

```bash
# Install PDM
python -m pip install pdm

# Initialize PDM project (follow prompts)
pdm init

# Install dependencies
pdm run pip install tqdm
pdm run pip install pathlib
pdm run pip install rich
pdm run pip install smile_config
pdm run pip install tifffile
pdm run pip install scipy
pdm run pip install scikit-image
```

### Step 6: Setup Environment Variables

```bash
# Edit your shell configuration
vim ~/.bashrc

# Add these lines (adjust paths to your setup):
export nnUNet_raw_data_base=/path/to/3D-Zebrafish-nnUNet/data/raw/
export nnUNet_raw=/path/to/3D-Zebrafish-nnUNet/data/raw/nnUNet_raw_data
export nnUNet_results=/path/to/3D-Zebrafish-nnUNet/data/results/
export nnUNet_preprocessed=/path/to/3D-Zebrafish-nnUNet/data/preprocessed/
export RESULTS_FOLDER=/path/to/3D-Zebrafish-nnUNet/data/results/

# Save and source
source ~/.bashrc
```

### Step 7: Create Data Directories

```bash
mkdir -p data/{raw,ori,segmented,results,preprocessed,cropped,inference}
```

---

## 🚀 Usage

### Data Preparation

1. Place raw images in `data/ori/`
2. Place segmentation masks in `data/segmented/`

### Dataset Conversion

Convert your data to nnU-Net format:

```bash
pdm run python -m src.dc --tod \
  --ori data/ori \
  --seg data/segmented \
  --database data/ \
  --name zebrafish_segv2 \
  --t 777
```

Convert Task (nnUNetv1) to Dataset (nnUNetv2):

```bash
pdm run nnUNetv2_convert_old_nnUNet_dataset \
  data/raw/nnUNet_raw_data/Task777_zebrafish_segv2 \
  Dataset777_zebrafish_segv2
```

### Training

Plan and preprocess:

```bash
pdm run nnUNetv2_plan_and_preprocess -d 777 -c 3d_fullres --verify_dataset_integrity
```

Train model:

```bash
pdm run nnUNetv2_train 777 3d_fullres 0
```

### Inference

```bash
pdm run nnUNetv2_predict \
  -i data/inference/input \
  -o data/inference/output \
  -d 777 \
  -c 3d_fullres \
  -f 0
```

---

## 📁 Repository Structure

```
3D-Zebrafish-nnUNet/
├── Dockerfile                    # Docker container definition
├── docker-compose.yml            # Docker orchestration
├── .dockerignore                 # Docker build optimization
├── DOCKER_SETUP.md              # Complete Docker setup guide
├── DOCKER_QUICKSTART.md         # Quick Docker setup
├── README.md                    # This file
├── src/                         # Source code
│   ├── dc.py                    # Dataset conversion
│   └── ...
├── data/                        # Data directory (create manually)
│   ├── raw/                     # nnU-Net raw data
│   ├── ori/                     # Original images
│   ├── segmented/               # Ground truth masks
│   ├── results/                 # Training results
│   ├── preprocessed/            # Preprocessed data
│   ├── cropped/                 # Cropped volumes
│   └── inference/               # Inference output
├── pdm.lock                     # PDM dependency lock
├── pyproject.toml               # PDM project configuration
└── ...
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

---

## 📧 Contact

- **PI:** Dr. Juhyun Lee - juhyun.lee@uta.edu
- **Lab:** [Lee Lab Website](https://juhyunleelab.com)
- **Institution:** University of Texas at Arlington

---

## 🙏 Acknowledgments

- nnU-Net framework: [MIC-DKFZ/nnUNet](https://github.com/MIC-DKFZ/nnUNet)
- NVIDIA for GPU support and CUDA toolkit

---

## 📚 References

1. Isensee, F., et al. "nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation." *Nature Methods* 18.2 (2021): 203-211.

---

## 🐛 Troubleshooting

### Common Issues

**Issue: CUDA out of memory**
- Reduce batch size in nnU-Net configuration
- Use smaller patch sizes
- Close other GPU-intensive processes

**Issue: Segmentation quality poor**
- Verify preprocessing applied correctly
- Check data quality and normalization
- Ensure sufficient training data

For more help, see [DOCKER_SETUP.md](DOCKER_SETUP.md) troubleshooting section or open an issue on GitHub.

---

**Last Updated:** December 2025  
**Platform Version:** 2.0  
**Docker Support:** ✅ Fully Containerized
