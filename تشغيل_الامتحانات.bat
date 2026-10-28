@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================================
echo   Primary Exam System - Starting...
echo ========================================================
start "" "%~dp0Index.html"
echo Local network: http://192.168.1.96:8080
python -m http.server 8080
