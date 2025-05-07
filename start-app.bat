@echo off
echo ===============================================
echo   Vocal & Music Separator - Starting Up...
echo ===============================================

REM Check if NVIDIA GPU is available
nvidia-smi >nul 2>&1
if %errorlevel% == 0 (
  echo [INFO] NVIDIA GPU detected! Using GPU acceleration.
) else (
  echo [WARNING] No NVIDIA GPU detected or drivers not installed.
  echo [WARNING] The application will run on CPU, which is significantly slower.
  echo [WARNING] For optimal performance, install NVIDIA GPU drivers.
  echo.
  timeout /t 3 >nul
)

echo [INFO] Starting Docker container...
docker-compose up -d

echo.
echo ===============================================
echo   Application started successfully!
echo   Visit http://localhost:8000 in your browser
echo ===============================================
echo.
echo Press any key to close this window...
pause >nul 