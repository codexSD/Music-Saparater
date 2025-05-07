FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install FFmpeg, Git, and CUDA dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg git wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app/ ./app/

# Create necessary directories
RUN mkdir -p uploads outputs app/static

# Set environment variables for GPU acceleration
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
ENV CUDA_VISIBLE_DEVICES=0
ENV TORCH_AUDIOMENTATIONS_DATA_DIR=/tmp

# Expose port for the web server
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 