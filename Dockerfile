FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install FFmpeg, Git, and CUDA dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg git wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies (this layer will be cached if requirements.txt doesn't change)
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

# The app directory will be mounted as a volume in docker-compose.yml
# This allows code changes without rebuilding the image

# Start the FastAPI app with reload for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 