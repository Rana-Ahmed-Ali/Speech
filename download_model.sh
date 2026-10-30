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

if [ -n "$1" ]; then
    python3 download_model.py "$@"
    exit 0
fi

echo "======================================================="
echo "   Whisper Model Downloader with Progress Bar"
echo "======================================================="
echo ""
echo "Choose which model to pre-download:"
echo "[1] medium (Recommended for Urdu/English accuracy - ~1.5 GB)"
echo "[2] small  (Faster on CPU - ~460 MB)"
echo "[3] large-v3-turbo (State-of-the-art multilingual - ~1.6 GB)"
echo "[4] tiny   (Ultra fast - ~75 MB)"
echo ""
read -rp "Select an option (1-4, default is 1): " CHOICE

case "$CHOICE" in
    2)
        MODEL="small"
        ;;
    3)
        MODEL="large-v3-turbo"
        ;;
    4)
        MODEL="tiny"
        ;;
    *)
        MODEL="medium"
        ;;
esac

echo ""
python3 download_model.py "$MODEL"

echo ""
echo "======================================================="
echo "Now you can run ./run_live.sh and it will start instantly!"
echo "======================================================="

