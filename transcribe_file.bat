@echo off
title Whisper Audio File Transcriber
echo =======================================================
echo    Whisper Batch Audio / Video File Transcription
echo =======================================================
echo.

if "%~1"=="" (
    echo Usage: Drag and drop an audio/video file onto this script,
    echo or run: transcribe_file.bat [path_to_audio_file]
    echo.
    set /p "AUDIO_FILE=Enter audio file path: "
) else (
    set "AUDIO_FILE=%~1"
)

call .\venv\Scripts\activate
python transcribe_file.py "%AUDIO_FILE%" %2 %3 %4 %5

pause
