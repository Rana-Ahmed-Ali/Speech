# Whisper Speech Recognition System (Bilingual Urdu & English)

Optimized for **real-time microphone dictation** and **batch audio/video file transcription** on Windows CPU using `faster-whisper` (CTranslate2 INT8 quantization).

---

## Features
- **Mixed Urdu-English ("Urdish") Optimization**: Primed with bilingual vocabulary cues so the model transcribes code-switching sentences without forcing an all-English or all-Urdu bias.
- **CPU Optimized (INT8)**: Runs on standard CPU hardware (Intel Core i5) with 4-thread parallel execution and ~1.5 GB memory footprint.
- **Voice Activity Detection (Silero VAD)**: Automatically detects speech pauses and avoids transcribing dead silence or background noise.
- **Live Microphone Dictation**: Speaks directly into the terminal, printing timestamps, detected language probability, and transcribing in real-time.
- **Automatic Session Logging**: All live transcripts and file transcripts are saved to the `transcripts/` directory.

---

## Quick Start

### 0. Pre-Download Models with Visual Progress Bar
To watch the download with speed and percentage progress bars:
- Double-click **`download_model.bat`**, or run:
  ```powershell
  .\venv\Scripts\python.exe download_model.py medium
  ```

### 1. Real-Time Microphone Dictation
Double click `run_live.bat` or run:
```powershell
.\venv\Scripts\python.exe live_transcribe.py
```

#### Choose Model Size:
- High accuracy (default):
  ```powershell
  .\venv\Scripts\python.exe live_transcribe.py --model medium
  ```
- Faster response on CPU (~2.5x faster):
  ```powershell
  .\venv\Scripts\python.exe live_transcribe.py --model small
  ```
- Cutting-edge multilingual model:
  ```powershell
  .\venv\Scripts\python.exe live_transcribe.py --model large-v3-turbo
  ```

#### Force Language (Optional):
By default, auto-detection with Urdu-English priming is active. To force Urdu script:
```powershell
.\venv\Scripts\python.exe live_transcribe.py --lang ur
```
Or force English:
```powershell
.\venv\Scripts\python.exe live_transcribe.py --lang en
```

#### List Available Microphones:
```powershell
.\venv\Scripts\python.exe live_transcribe.py --list-devices
```

---

### 2. Transcribe Audio or Video Files
Drag and drop any `.mp3`, `.wav`, `.m4a`, `.mp4`, or `.mkv` file onto `transcribe_file.bat`, or run:
```powershell
.\venv\Scripts\python.exe transcribe_file.py "path\to\recording.mp3" --model medium
```

---

## Configuration
Edit [config.py](file:///d:/Speach/config.py) to customize:
- `DEFAULT_MODEL_SIZE`: Choose `small`, `medium`, or `large-v3-turbo`
- `INITIAL_PROMPT`: Add custom jargon, names, or frequently used mixed words
- `SILENCE_DURATION_SEC`: Pause duration in seconds before triggering transcription (default: 1.0s)
- `CPU_THREADS`: Number of CPU inference threads (default: 4)
