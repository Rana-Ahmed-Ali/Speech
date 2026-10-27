"""
Whisper Model Downloader with Live Visual Progress Bar
Pre-downloads Whisper models so live transcription starts instantaneously.
"""
import sys
import argparse
from huggingface_hub import snapshot_download
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

MODEL_REPOS = {
    "tiny": "Systran/faster-whisper-tiny",
    "base": "Systran/faster-whisper-base",
    "small": "Systran/faster-whisper-small",
    "medium": "Systran/faster-whisper-medium",
    "large-v3-turbo": "Systran/faster-whisper-large-v3-turbo",
    "large-v3": "Systran/faster-whisper-large-v3",
}

APPROX_SIZES = {
    "tiny": "~75 MB",
    "base": "~145 MB",
    "small": "~460 MB",
    "medium": "~1.5 GB",
    "large-v3-turbo": "~1.6 GB",
    "large-v3": "~3.1 GB",
}


def download_model(model_name: str):
    if model_name not in MODEL_REPOS:
        print(f"{Fore.RED}Error: Unknown model '{model_name}'. Choose from: {list(MODEL_REPOS.keys())}{Style.RESET_ALL}")
        return False

    repo_id = MODEL_REPOS[model_name]
    size_est = APPROX_SIZES.get(model_name, "unknown")

    print(f"\n{Fore.CYAN}=======================================================")
    print(f"   Downloading Whisper Model: {Fore.YELLOW}{model_name}{Fore.CYAN} ({size_est})")
    print(f"   Repo: {Fore.WHITE}{repo_id}")
    print(f"======================================================={Style.RESET_ALL}\n")

    try:
        # snapshot_download displays a live tqdm progress bar for every file
        download_path = snapshot_download(
            repo_id=repo_id,
            repo_type="model",
            tqdm_class=None  # Uses default active tqdm progress bar
        )
        print(f"\n{Fore.GREEN} Download Complete for '{model_name}'!{Style.RESET_ALL}")
        print(f"Cached at: {Fore.BLUE}{download_path}{Style.RESET_ALL}\n")
        return True
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Download cancelled by user.{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"\n{Fore.RED}Download failed: {e}{Style.RESET_ALL}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Download Whisper Models with Live Progress Bar")
    parser.add_argument("model", type=str, nargs="?", default="medium",
                        choices=["tiny", "base", "small", "medium", "large-v3-turbo", "large-v3", "all"],
                        help="Model to download (default: medium)")
    args = parser.parse_args()

    if args.model == "all":
        for m in ["small", "medium", "large-v3-turbo"]:
            success = download_model(m)
            if not success:
                break
    else:
        download_model(args.model)


if __name__ == "__main__":
    main()
