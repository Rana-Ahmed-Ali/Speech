"""
Configuration for Whisper Speech Recognition
Optimized for: Mixed Urdu-English ("Urdish") Real-Time & Batch Transcription
Hardware: CPU Intel Core i5-6500 (4 cores, INT8 quantization)
"""
import os
from pathlib import Path

# Suppress Hugging Face Windows symlink cache warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

# Whisper Model Configuration
# Options: "tiny", "base", "small", "medium", "large-v3-turbo"
# "medium" offers high accuracy for Urdu/English code-switching
# "small" is ~2.5x faster if lower latency is preferred on CPU
# "large-v3-turbo" is cutting-edge multilingual with fast 4-layer decoder
DEFAULT_MODEL_SIZE = "medium"

# Hardware / Inference Configuration
DEVICE = "cpu"
COMPUTE_TYPE = "int8"   # Fast INT8 quantized inference via CTranslate2
CPU_THREADS = 4         # Match physical cores of i5-6500

# Mixed Urdu-English Bilingual Prompt Priming
# Priming the decoder with both Urdu and English vocabulary guides Whisper
# to recognize code-switching accurately rather than forcing one language.
INITIAL_PROMPT = (
    "Yeh Urdu aur English ki mixed conversation hai. "
    "We use mixed words like meeting, project, theek hai, office, bilkul, "
    "laptop, computer, internet, call karna, message bhejna, shukriya."
)

# Language setting:
# None = auto-detect per speech segment
# "ur" = prioritize Urdu script / mixed Urdu
# "en" = English transcription
DEFAULT_LANGUAGE = None

# Audio / Real-Time Dictation Settings
SAMPLE_RATE = 16000           # 16kHz mono required by Whisper
CHANNELS = 1                  # Mono
CHUNK_DURATION_SEC = 0.5      # Audio input buffer slice duration
SILENCE_DURATION_SEC = 1.0    # Transcribe when silence exceeds this length
MAX_PHRASE_DURATION_SEC = 15  # Max duration before forcing a transcription
MIN_SPEECH_DURATION_SEC = 0.6 # Minimum speech duration to prevent empty noise
VAD_FILTER = True             # Enable Silero Voice Activity Filter
