from pathlib import Path

DOWNLOADS_DIR = Path("downloads")
DEFAULT_FORMAT = "mp4"
HISTORY_FILE = Path('downloads/download_history.txt')


def setup_directories():
    DOWNLOADS_DIR.mkdir(exist_ok=True)