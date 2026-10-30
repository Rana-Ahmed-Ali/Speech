"""
Real-Time Microphone Dictation & Transcription using faster-whisper
Optimized for mixed Urdu-English speech on CPU (INT8).
"""
import sys
import time
import queue
import argparse
from datetime import datetime
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
import colorama
from colorama import Fore, Style

import config

colorama.init(autoreset=True)


def list_audio_devices():
    """Print all available input devices."""
    print(f"\n{Fore.CYAN}=== Available Audio Input Devices ==={Style.RESET_ALL}")
    try:
        devices = sd.query_devices()
        try:
            default_in = sd.default.device[0]
        except Exception:
            default_in = None
        
        found = False
        for idx, dev in enumerate(devices):
            if dev.get("max_input_channels", 0) > 0:
                found = True
                default_marker = " [DEFAULT]" if default_in is not None and idx == default_in and default_in >= 0 else ""
                print(f"[{idx}] {dev['name']} ({dev.get('hostapi', 'Unknown')}){default_marker}")
        if not found:
            print(f"{Fore.YELLOW}No input devices found. Please ensure your microphone is connected and recognized.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error listing devices: {e}{Style.RESET_ALL}")
    print()


def load_model(model_size: str):
    """Load faster-whisper model with INT8 CPU optimization."""
    print(f"\n{Fore.YELLOW}Loading Whisper model '{model_size}' (Device: {config.DEVICE}, Compute: {config.COMPUTE_TYPE}, Threads: {config.CPU_THREADS})...{Style.RESET_ALL}")
    print(f"{Fore.BLACK}{Style.BRIGHT}Note: The first time a model runs, weights are downloaded to your HuggingFace cache automatically.{Style.RESET_ALL}")
    t0 = time.time()
    model = WhisperModel(
        model_size,
        device=config.DEVICE,
        compute_type=config.COMPUTE_TYPE,
        cpu_threads=config.CPU_THREADS,
        num_workers=1
    )
    print(f"{Fore.GREEN}Model loaded successfully in {time.time() - t0:.2f} seconds!{Style.RESET_ALL}\n")
    return model


def run_live_transcription(model_size: str, language: str = None, device_id: int = None):
    # Set up session transcript file
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_file = config.TRANSCRIPTS_DIR / f"live_{model_size}_{timestamp_str}.txt"

    print(f"{Fore.CYAN}=====================================================")
    print(f"   Whisper Live Speech Recognition (Urdu / English)   ")
    print(f"====================================================={Style.RESET_ALL}")
    print(f"Model: {Fore.YELLOW}{model_size}{Style.RESET_ALL} | Language: {Fore.YELLOW}{language or 'Auto-Detect (Urdu/English Primed)'}{Style.RESET_ALL}")
    print(f"Saving transcript to: {Fore.BLUE}{session_file}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Press Ctrl+C at any time to stop.{Style.RESET_ALL}\n")

    model = load_model(model_size)

    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"{Fore.RED}Audio callback warning: {status}{Style.RESET_ALL}", file=sys.stderr)
        audio_queue.put(indata.copy())

    samplerate = config.SAMPLE_RATE
    block_size = int(samplerate * config.CHUNK_DURATION_SEC)

    # VAD energy baseline tracking
    speech_buffer = []
    silence_frames = 0
    silence_frames_threshold = int(config.SILENCE_DURATION_SEC / config.CHUNK_DURATION_SEC)
    max_frames = int(config.MAX_PHRASE_DURATION_SEC / config.CHUNK_DURATION_SEC)
    is_speaking = False

    # Auto-calibrate ambient noise level for 1 second
    print(f"{Fore.CYAN}Calibrating microphone for ambient room noise (please stay quiet for 1s)...{Style.RESET_ALL}")
    calibration_samples = []
    try:
        with sd.InputStream(samplerate=samplerate, channels=config.CHANNELS, dtype="float32", blocksize=block_size, device=device_id, callback=audio_callback):
            for _ in range(3):
                chunk = audio_queue.get(timeout=2.0)
                calibration_samples.append(np.sqrt(np.mean(chunk.flatten() ** 2)))
    except Exception as e:
        print(f"{Fore.RED}Audio device error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Tip: Use --list-devices to view input device IDs, then specify --device <id>.{Style.RESET_ALL}")
        return

    ambient_energy = np.mean(calibration_samples) if calibration_samples else 0.001
    # Speech threshold: 2.5x ambient noise, bounded between 0.003 and 0.02
    energy_threshold = max(min(ambient_energy * 2.5, 0.02), 0.003)
    print(f"{Fore.GREEN}Calibration done! (Ambient: {ambient_energy:.4f}, Trigger Threshold: {energy_threshold:.4f}){Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}>>> Microphone is LIVE! Start speaking now... <<<{Style.RESET_ALL}\n")

    with open(session_file, "a", encoding="utf-8") as log_file:
        log_file.write(f"=== Session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        log_file.write(f"Model: {model_size} | Language: {language}\n\n")

        try:
            with sd.InputStream(
                samplerate=samplerate,
                channels=config.CHANNELS,
                dtype="float32",
                blocksize=block_size,
                device=device_id,
                callback=audio_callback
            ):
                while True:
                    chunk = audio_queue.get()
                    audio_flat = chunk.flatten()
                    energy = np.sqrt(np.mean(audio_flat ** 2))

                    # Visual feedback bar for voice activity
                    meter_len = int(min(energy / (energy_threshold * 2.0), 1.0) * 15)
                    bar = "█" * meter_len + "░" * (15 - meter_len)

                    if energy > energy_threshold:
                        if not is_speaking:
                            is_speaking = True
                            print(f"\r{Fore.YELLOW}🎤 [Speaking...] [{bar}] {Style.RESET_ALL}   ", end="", flush=True)
                        else:
                            print(f"\r{Fore.YELLOW}🎤 [Speaking...] [{bar}] {Style.RESET_ALL}   ", end="", flush=True)
                        speech_buffer.append(audio_flat)
                        silence_frames = 0
                    else:
                        if is_speaking:
                            speech_buffer.append(audio_flat)
                            silence_frames += 1
                            print(f"\r{Fore.CYAN}👂 [Listening...] [{bar}] {Style.RESET_ALL}   ", end="", flush=True)

                    # Trigger transcription when silence threshold reached or max duration hit
                    should_transcribe = False
                    if is_speaking:
                        if silence_frames >= silence_frames_threshold:
                            should_transcribe = True
                        elif len(speech_buffer) >= max_frames:
                            should_transcribe = True

                    if should_transcribe and speech_buffer:
                        full_audio = np.concatenate(speech_buffer)
                        duration_sec = len(full_audio) / samplerate

                        # Only transcribe if duration exceeds minimum threshold
                        if duration_sec >= config.MIN_SPEECH_DURATION_SEC:
                            print(f"\r{Fore.MAGENTA}⏳ [Transcribing {duration_sec:.1f}s speech...]            {Style.RESET_ALL}", end="", flush=True)
                            t_start = time.time()
                            segments, info = model.transcribe(
                                full_audio,
                                language=language,
                                initial_prompt=config.INITIAL_PROMPT,
                                beam_size=2,
                                vad_filter=config.VAD_FILTER,
                                vad_parameters=dict(min_silence_duration_ms=300)
                            )

                            transcript_parts = []
                            for segment in segments:
                                text = segment.text.strip()
                                if text:
                                    transcript_parts.append(text)

                            transcription = " ".join(transcript_parts)
                            inference_time = time.time() - t_start

                            # Clear the status line
                            print("\r" + " " * 60 + "\r", end="")

                            if transcription:
                                time_now = datetime.now().strftime("%H:%M:%S")
                                detected_lang = info.language if hasattr(info, "language") else (language or "unknown")
                                lang_prob = f"{info.language_probability * 100:.0f}%" if hasattr(info, "language_probability") else ""

                                # Console output
                                print(f"{Fore.BLACK}{Style.BRIGHT}[{time_now}] ({detected_lang} {lang_prob} | {duration_sec:.1f}s audio in {inference_time:.2f}s):{Style.RESET_ALL}")
                                print(f"{Fore.GREEN}{Style.BRIGHT}{transcription}{Style.RESET_ALL}\n")

                                # File logging
                                log_file.write(f"[{time_now}] ({detected_lang}) {transcription}\n")
                                log_file.flush()
                        else:
                            # Clear short noise
                            print("\r" + " " * 60 + "\r", end="")

                        # Reset buffers
                        speech_buffer = []
                        silence_frames = 0
                        is_speaking = False


        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Stopping live transcription...{Style.RESET_ALL}")
            log_file.write(f"\n=== Session stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            print(f"{Fore.GREEN}Session transcript saved to: {session_file}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(description="Real-Time Whisper Live Microphone Transcription (Urdu / English)")
    parser.add_argument("--model", type=str, default=config.DEFAULT_MODEL_SIZE,
                        choices=["tiny", "base", "small", "medium", "large-v3-turbo"],
                        help="Model size (default: medium, or small for faster CPU response)")
    parser.add_argument("--lang", type=str, default=config.DEFAULT_LANGUAGE,
                        help="Language code ('ur' for Urdu, 'en' for English, or omit for auto-detect)")
    parser.add_argument("--device", type=int, default=None,
                        help="Microphone input device index (run --list-devices to view)")
    parser.add_argument("--list-devices", action="store_true",
                        help="List all audio input devices and exit")

    args = parser.parse_args()

    if args.list_devices:
        list_audio_devices()
        return

    run_live_transcription(model_size=args.model, language=args.lang, device_id=args.device)


if __name__ == "__main__":
    main()
