# 🎵 Vocal & Music Separator 🎵

AI-powered application that separates vocals and music from audio/video files, **now with GPU acceleration!** 🚀

![Powered by AI](https://img.shields.io/badge/Powered%20by-AI-blue) ![GPU Acceleration](https://img.shields.io/badge/GPU-Acceleration-green) ![Offline Processing](https://img.shields.io/badge/Offline-Processing-orange)

<p align="center">
  <img src="https://user-images.githubusercontent.com/1118293/133933532-a6b81586-9177-48de-8081-cc6c8a6b7259.png" width="400px" alt="Demucs Vocal Separation">
</p>

## ✨ Features

- 🎤 **Isolate Vocals**: Remove background music and keep just the vocals
- 🎹 **Extract Music**: Remove vocals and keep just the instrumental music
- 📁 Upload **multiple formats**: MP3, WAV, MP4, MKV, MOV
- 💻 100% **local processing** with no data sent to external servers
- 🔥 **GPU acceleration** for fast and high-quality separation
- 🖥️ Beautiful, easy-to-use web interface

## 🖥️ Requirements

- 🐳 [Docker](https://www.docker.com/products/docker-desktop/) & Docker Compose (included with Docker Desktop)
- 🎮 NVIDIA GPU + CUDA drivers (for GPU acceleration) *(optional but recommended)*

## 🚀 How to Run

### 🏎️ Easy Method (Recommended)

#### On Windows
Simply double-click on the `start-app.bat` file to start the application.
When done, close the app by double-clicking on the `stop-app.bat` file.

#### On macOS/Linux
Run the application with:
```bash
docker-compose up -d
```

Stop the application with:
```bash
docker-compose down
```

### 🔧 Manual Method

1. Clone this repository:
   ```bash
   git clone [repository-url]
   cd [repository-directory]
   ```

2. Build the Docker image:
   ```bash
   docker build -t vocal-remover .
   ```

3. Run the container with GPU support:
   ```bash
   docker run --gpus all -p 8000:8000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/outputs:/app/outputs vocal-remover
   ```
   
   For Windows Command Prompt:
   ```
   docker run --gpus all -p 8000:8000 -v %cd%/uploads:/app/uploads -v %cd%/outputs:/app/outputs vocal-remover
   ```
   
   For Windows PowerShell:
   ```
   docker run --gpus all -p 8000:8000 -v ${PWD}/uploads:/app/uploads -v ${PWD}/outputs:/app/outputs vocal-remover
   ```

4. Open your browser and go to:
   ```
   http://localhost:8000
   ```

## 🔍 How It Works

1. 📤 Upload a video or audio file through the web interface
2. 🎛️ Select whether you want to isolate vocals or music
3. ⚙️ The application processes the file:
   - 🎬 For video files, it extracts the audio first using FFmpeg
   - 🧠 It runs the Demucs AI model with GPU acceleration to separate vocals from music
   - 🔄 For video files, it combines the selected audio with the original video
4. 📥 Download the processed file when complete

## 🔧 GPU Acceleration Setup

### Windows
1. Install [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
2. Install [NVIDIA Docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)
3. Ensure Docker Desktop is configured to use NVIDIA runtime

### Linux
1. Install NVIDIA drivers and CUDA:
   ```bash
   sudo apt-get update
   sudo apt-get install -y nvidia-driver-525 nvidia-cuda-toolkit
   ```
2. Install NVIDIA Docker:
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

## 🛠️ Technology Stack

- 🧠 **Demucs**: State-of-the-art AI model for separating vocals and music
- 🎬 **FFmpeg**: Handles video/audio extraction and merging
- ⚡ **FastAPI**: High-performance Python backend API
- 🖌️ **HTML/JavaScript**: Clean, responsive frontend interface
- 🐳 **Docker**: Containerization with GPU support

## 📝 Note

- 🕒 The first time you run the application, it will download the Demucs model (~1GB), which may take some time
- 🔥 Processing is **much faster with GPU acceleration** enabled
- 💻 All processing happens locally on your computer - your files never leave your machine
- 🔊 Higher quality audio separation yields better results but takes more processing time 