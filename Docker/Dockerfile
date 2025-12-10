# 3D Zebrafish nnUNet Docker Container
# Production-ready containerization for reproducible research

FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-venv \
    git \
    vim \
    wget \
    curl \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links for python
RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/python3.10 /usr/bin/python3

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install PyTorch with CUDA 11.8
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Clone and install nnUNet
RUN git clone https://github.com/MIC-DKFZ/nnUNet.git && \
    cd nnUNet && \
    pip install -e . && \
    pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git

# Install PDM
RUN python -m pip install pdm

# Install dependencies
RUN pip install \
    tqdm \
    pathlib \
    rich \
    smile-config \
    tifffile \
    scipy \
    scikit-image \
    numpy \
    pandas \
    matplotlib

# Set environment variables for nnU-Net
ENV nnUNet_raw_data_base=/workspace/zebrafish/data/raw
ENV nnUNet_raw=/workspace/zebrafish/data/raw/nnUNet_raw_data
ENV nnUNet_results=/workspace/zebrafish/data/results
ENV nnUNet_preprocessed=/workspace/zebrafish/data/preprocessed
ENV RESULTS_FOLDER=/workspace/zebrafish/data/results

# Create directory structure
RUN mkdir -p /workspace/zebrafish/data/{raw,ori,segmented,results,preprocessed,cropped,inference}

# Set working directory where user code will be mounted
WORKDIR /workspace/zebrafish

# Default command
CMD ["/bin/bash"]
