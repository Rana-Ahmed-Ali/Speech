@echo off
title Download Whisper Models (With Live Progress)
echo =======================================================
echo    Whisper Model Downloader with Progress Bar
echo =======================================================
echo.
echo Choose which model to pre-download:
echo [1] medium (Recommended for Urdu/English accuracy - ~1.5 GB)
echo [2] small  (Faster on CPU - ~460 MB)
echo [3] large-v3-turbo (State-of-the-art multilingual - ~1.6 GB)
echo [4] tiny   (Ultra fast - ~75 MB)
echo.

set /p CHOICE="Select an option (1-4, default is 1): "

if "%CHOICE%"=="2" (
    set MODEL=small
) else if "%CHOICE%"=="3" (
    set MODEL=large-v3-turbo
) else if "%CHOICE%"=="4" (
    set MODEL=tiny
) else (
    set MODEL=medium
)

echo.
call .\venv\Scripts\activate
python download_model.py %MODEL%

echo.
echo =======================================================
echo Now you can run run_live.bat and it will start instantly!
echo =======================================================
pause
