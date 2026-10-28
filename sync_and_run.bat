@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================================
echo   [Step 1/2] Coligo LMS Live Sync - Fetching Data...
echo ========================================================
python coligo_sync_engine.py

echo.
echo ========================================================
echo   [Step 2/2] Launching Exam Dashboard ^& Local Server...
echo ========================================================
start "" "%~dp0Index.html"
echo Local network endpoint: http://192.168.1.96:8080
python -m http.server 8080
