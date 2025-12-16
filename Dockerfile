# We use the Nvidia CUDA base image for maximum compatibility with bitsandbytes
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Set up Python environment
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Alias python3 to python
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app/ ./app/

# Create a volume directory for the models so we don't download them every time
RUN mkdir -p /root/.cache/huggingface

CMD ["python", "app/main.py"]