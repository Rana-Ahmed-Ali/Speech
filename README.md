# Whisper Speech Recognition System (Bilingual Urdu & English)

Optimized for **real-time microphone dictation** and **batch audio/video file transcription** on Linux and Windows CPU using `faster-whisper` (CTranslate2 INT8 quantization).

---

## Features
- **Cross-Platform Support**: Fully compatible with both **Linux** (Ubuntu, Debian, Fedora, Arch) and **Windows** (10/11).
- **Mixed Urdu-English ("Urdish") Optimization**: Primed with bilingual vocabulary cues so the model transcribes code-switching sentences without forcing an all-English or all-Urdu bias.
- **CPU Optimized (INT8)**: Runs on standard CPU hardware (Intel Core i5) with multi-threaded parallel execution and ~1.5 GB memory footprint.
- **Voice Activity Detection (Silero VAD)**: Automatically detects speech pauses and avoids transcribing dead silence or background noise.
- **Live Microphone Dictation**: Speaks directly into the terminal, printing timestamps, detected language probability, and transcribing in real-time.
- **Automatic Session Logging**: All live transcripts and file transcripts are saved to the `transcripts/` directory.

---

## 🐧 Linux Quick Start

### 1. Install System Dependencies
Make sure Python 3, virtual environment tools, ffmpeg, and PortAudio are installed:
```bash
# Ubuntu / Debian / Linux Mint:
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg libportaudio2

# Fedora / RHEL:
sudo dnf install -y python3 ffmpeg portaudio

# Arch Linux:
sudo pacman -S python ffmpeg portaudio
```

### 2. Setup Project Environment
Run the automated setup script to configure the Python virtual environment and install dependencies:
```bash
chmod +x *.sh
./setup.sh
```

### 3. Pre-Download Models (Recommended)
Download models with a live progress bar:
```bash
./download_model.sh
# Or pass a model name directly:
./download_model.sh medium
```

### 4. Real-Time Microphone Dictation
Launch live dictation:
```bash
./run_live.sh
```

#### Choose Model Size:
- **High accuracy (Urdu/English default)**:
  ```bash
  ./run_live.sh --model medium
  ```
- **Faster response on CPU (~2.5x faster)**:
  ```bash
  ./run_live.sh --model small
  ```
- **Cutting-edge multilingual model**:
  ```bash
  ./run_live.sh --model large-v3-turbo
  ```

#### Force Specific Language (Optional):
```bash
./run_live.sh --lang ur   # Force Urdu script
./run_live.sh --lang en   # Force English
```

#### Microphone Selection:
List all recognized input devices:
```bash
./run_live.sh --list-devices
```
Specify an input device ID:
```bash
./run_live.sh --device 0
```

### 5. Transcribe Audio or Video Files
Transcribe any `.mp3`, `.wav`, `.m4a`, `.mp4`, or `.mkv` file:
```bash
./transcribe_file.sh path/to/recording.mp3 --model medium
```

---

## 🪟 Windows Quick Start

### 1. Pre-Download Models
- Double-click **`download_model.bat`**, or run:
  ```powershell
  .\venv\Scripts\python.exe download_model.py medium
  ```

### 2. Real-Time Microphone Dictation
- Double-click **`run_live.bat`**, or run:
  ```powershell
  .\venv\Scripts\python.exe live_transcribe.py --model medium
  ```

- To list input devices:
  ```powershell
  .\venv\Scripts\python.exe live_transcribe.py --list-devices
  ```

### 3. Transcribe Audio or Video Files
Drag and drop any audio/video file onto **`transcribe_file.bat`**, or run:
```powershell
.\venv\Scripts\python.exe transcribe_file.py "path\to\recording.mp3" --model medium
```

---

## Configuration

Edit [`config.py`](config.py) to customize:
- `DEFAULT_MODEL_SIZE`: Choose `small`, `medium`, or `large-v3-turbo`
- `INITIAL_PROMPT`: Add custom jargon, names, or frequently used mixed vocabulary
- `SILENCE_DURATION_SEC`: Pause duration in seconds before triggering transcription (default: `1.0s`)
- `CPU_THREADS`: Number of CPU inference threads (default: `4`, or set via `WHISPER_THREADS` environment variable)
