# Vocal & Music Separator

A local web application that allows you to separate vocals and music from audio or video files using AI.

## Features

- Upload audio (MP3, WAV) or video files (MP4, MKV, MOV)
- Choose to isolate vocals or music
- Process files locally without internet (after initial setup)
- Download the processed results

## Requirements

- Docker (https://www.docker.com/products/docker-desktop/)
- Docker Compose (included with Docker Desktop)

## How to Run

### Easy Method (Recommended)

#### On Windows
Simply double-click on the `start-app.bat` file to start the application.
When done, close the app by double-clicking on the `stop-app.bat` file.

#### On macOS/Linux
Run the application with:
```
docker-compose up -d
```

Stop the application with:
```
docker-compose down
```

### Manual Method

1. Clone this repository:
   ```
   git clone [repository-url]
   cd [repository-directory]
   ```

2. Build the Docker image:
   ```
   docker build -t vocal-remover .
   ```

3. Run the container:
   ```
   docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/outputs:/app/outputs vocal-remover
   ```
   
   For Windows Command Prompt:
   ```
   docker run -p 8000:8000 -v %cd%/uploads:/app/uploads -v %cd%/outputs:/app/outputs vocal-remover
   ```
   
   For Windows PowerShell:
   ```
   docker run -p 8000:8000 -v ${PWD}/uploads:/app/uploads -v ${PWD}/outputs:/app/outputs vocal-remover
   ```

4. Open your browser and go to:
   ```
   http://localhost:8000
   ```

## How It Works

1. Upload a video or audio file through the web interface
2. Select whether you want to isolate vocals or music
3. The application processes the file:
   - For video files, it extracts the audio first
   - It runs the Demucs AI model to separate vocals from music
   - For video files, it combines the selected audio with the original video
4. Download the processed file when complete

## Technology Stack

- **Demucs**: AI model for separating vocals and music
- **FFmpeg**: Handles video/audio extraction and merging
- **FastAPI**: Python backend API
- **HTML/JavaScript**: Frontend interface
- **Docker**: Containerization

## Note

- The first time you run the application, it will download the Demucs model, which may take some time
- Processing large files can be resource-intensive and may take several minutes
- All processing happens locally on your computer 