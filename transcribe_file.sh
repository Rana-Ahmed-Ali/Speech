#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment if present
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
elif [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
else
    echo "Virtual environment not found. Running ./setup.sh first..."
    bash "$SCRIPT_DIR/setup.sh"
    source "$SCRIPT_DIR/venv/bin/activate"
fi

if [ -z "$1" ]; then
    echo "Usage: ./transcribe_file.sh <path_to_audio_file> [--model MODEL] [--lang LANG]"
    echo ""
    read -rp "Enter audio or video file path: " AUDIO_FILE
    if [ -z "$AUDIO_FILE" ]; then
        echo "No file provided. Exiting."
        exit 1
    fi
    python3 transcribe_file.py "$AUDIO_FILE"
else
    python3 transcribe_file.py "$@"
fi

