from pathlib import Path

DOWNLOADS_DIR = Path("downloads")
DEFAULT_FORMAT = "mp4"

def setup_directories():
    DOWNLOADS_DIR.mkdir(exist_ok=True)