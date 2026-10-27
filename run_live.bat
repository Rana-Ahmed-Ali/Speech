@echo off
title Whisper Live Dictation (Urdu - English)
echo =======================================================
echo    Whisper Live Real-Time Microphone Transcription
echo =======================================================
echo.

REM Activate Virtual Environment
call .\venv\Scripts\activate

REM Run live transcription
REM Default uses medium model. You can also specify --model small for lower latency.
".\venv\Scripts\python.exe" live_transcribe.py %*

pause
