@echo off
echo ===============================================
echo   Vocal & Music Separator - Restarting...
echo ===============================================

echo [INFO] Stopping Docker container...
docker compose stop

echo [INFO] Starting Docker container...
docker compose start

echo.
echo ===============================================
echo   Application restarted successfully!
echo   Visit http://localhost:8000 in your browser
echo ===============================================
echo.
echo Press any key to close this window...
pause >nul 