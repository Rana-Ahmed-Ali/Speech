"""
Batch Audio / Video File Transcription using faster-whisper
Optimized for mixed Urdu-English speech on CPU (INT8).
"""
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
from faster_whisper import WhisperModel
import colorama
from colorama import Fore, Style

import config

colorama.init(autoreset=True)


def transcribe_file(file_path: str, model_size: str, language: str = None, output_format: str = "txt"):
    path = Path(file_path)
    if not path.exists():
        print(f"{Fore.RED}Error: File not found: {file_path}{Style.RESET_ALL}")
        sys.exit(1)

    print(f"\n{Fore.CYAN}=== Transcribing: {path.name} ==={Style.RESET_ALL}")
    print(f"File: {path.resolve()}")
    print(f"Model: {model_size} | Language: {language or 'Auto-Detect (Urdu/English Primed)'}\n")

    t0 = time.time()
    model = WhisperModel(
        model_size,
        device=config.DEVICE,
        compute_type=config.COMPUTE_TYPE,
        cpu_threads=config.CPU_THREADS,
        num_workers=1
    )
    print(f"{Fore.GREEN}Model loaded in {time.time() - t0:.2f}s. Starting transcription...{Style.RESET_ALL}\n")

    t_start = time.time()
    segments, info = model.transcribe(
        str(path),
        language=language,
        initial_prompt=config.INITIAL_PROMPT,
        beam_size=3,
        vad_filter=config.VAD_FILTER
    )

    detected_lang = info.language if hasattr(info, "language") else "unknown"
    duration = info.duration if hasattr(info, "duration") else 0
    print(f"Detected Language: {Fore.YELLOW}{detected_lang}{Style.RESET_ALL} (Duration: {duration:.1f}s)\n")

    lines = []
    for segment in segments:
        start_m, start_s = divmod(segment.start, 60)
        end_m, end_s = divmod(segment.end, 60)
        time_tag = f"[{int(start_m):02d}:{start_s:05.2f} -> {int(end_m):02d}:{end_s:05.2f}]"
        line_str = f"{time_tag}  {segment.text.strip()}"
        lines.append(line_str)
        print(f"{Fore.BLACK}{Style.BRIGHT}{time_tag}{Style.RESET_ALL} {segment.text.strip()}")

    total_time = time.time() - t_start
    print(f"\n{Fore.GREEN}Transcription completed in {total_time:.2f}s ({duration / max(total_time, 0.001):.1f}x real-time){Style.RESET_ALL}")

    # Output file
    out_file = config.TRANSCRIPTS_DIR / f"{path.stem}_transcript.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"File: {path.name}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model: {model_size} | Language: {detected_lang}\n")
        f.write("=" * 60 + "\n\n")
        f.write("\n".join(lines) + "\n")

    print(f"Saved full transcript to: {Fore.BLUE}{out_file}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(description="Transcribe Audio/Video Files (Urdu & English)")
    parser.add_argument("file", type=str, help="Path to audio/video file (mp3, wav, m4a, mp4, etc.)")
    parser.add_argument("--model", type=str, default=config.DEFAULT_MODEL_SIZE,
                        choices=["tiny", "base", "small", "medium", "large-v3-turbo"],
                        help="Model size (default: medium)")
    parser.add_argument("--lang", type=str, default=config.DEFAULT_LANGUAGE,
                        help="Language code ('ur' for Urdu, 'en' for English, or omit for auto-detect)")
    args = parser.parse_args()

    transcribe_file(args.file, model_size=args.model, language=args.lang)


if __name__ == "__main__":
    main()
