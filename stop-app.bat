@echo off
echo ===============================================
echo   Vocal & Music Separator - Shutting Down...
echo ===============================================

echo [INFO] Stopping Docker container...
docker-compose down

echo.
echo ===============================================
echo   Application stopped successfully!
echo ===============================================
echo.
echo Press any key to close this window...
pause >nul 