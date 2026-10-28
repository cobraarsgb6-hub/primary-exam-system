@echo off
chcp 65001 >nul
cd /d "%~dp0"

where wt.exe >nul 2>nul
if %ERRORLEVEL% equ 0 if not defined WT_SESSION (
    start wt.exe -d "%~dp0" cmd /k "python coligo_sync_engine.py"
    exit /b
)

echo ========================================================
echo   Coligo LMS Live Sync Engine
echo ========================================================
python coligo_sync_engine.py
pause
