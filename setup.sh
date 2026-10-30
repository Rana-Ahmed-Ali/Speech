#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================="
echo "   Whisper Speech Recognition - Linux Setup"
echo "======================================================="
echo ""

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    echo "Please install Python 3 (e.g. sudo apt install python3 python3-venv python3-pip)"
    exit 1
fi

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "[Notice] 'ffmpeg' was not found in PATH."
    echo "Audio/video conversion for transcribe_file.py requires ffmpeg."
    echo "Install it via: sudo apt install ffmpeg (Debian/Ubuntu) or sudo dnf install ffmpeg (Fedora)"
    echo ""
fi

# Check for portaudio
if ! ldconfig -p 2>/dev/null | grep -qi "libportaudio"; then
    echo "[Notice] libportaudio may not be installed."
    echo "Microphone recording requires portaudio."
    echo "Install it via: sudo apt install libportaudio2 (Debian/Ubuntu) or sudo dnf install portaudio (Fedora)"
    echo ""
fi

# Create or reuse virtual environment
if [ ! -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    echo "Creating virtual environment in ./venv..."
    python3 -m venv "$SCRIPT_DIR/venv"
fi

echo "Activating virtual environment..."
source "$SCRIPT_DIR/venv/bin/activate"

echo "Upgrading pip and installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "======================================================="
echo "✔ Setup completed successfully!"
echo "======================================================="
echo "You can now run:"
echo "  ./download_model.sh        # Pre-download models"
echo "  ./run_live.sh              # Start live microphone dictation"
echo "  ./transcribe_file.sh <file># Transcribe an audio/video file"
echo "======================================================="

