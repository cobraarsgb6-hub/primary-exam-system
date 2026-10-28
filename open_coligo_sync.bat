@echo off
title Coligo LMS Auto-Sync Engine
echo ========================================================
echo   Coligo LMS Materials and Worksheets Auto-Sync
echo ========================================================
echo.
cd /d "%~dp0"
python crawl_coligo.py
pause
