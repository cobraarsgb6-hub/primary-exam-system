@echo off
title Educational Video Streaming Server
echo ========================================================
echo   Educational Video Streaming Server (Port 8085)
echo   High-Performance Local MP4 Streamer with Byte-Range
echo ========================================================
echo.
cd /d "%~dp0"
python serve_videos.py
pause
