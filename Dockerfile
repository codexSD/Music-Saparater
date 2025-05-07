FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install FFmpeg and Git
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
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

# Set environment variable for Demucs to avoid CUDA errors
ENV CONDA_OVERRIDE_CUDA=11.8

# Expose port for the web server
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 