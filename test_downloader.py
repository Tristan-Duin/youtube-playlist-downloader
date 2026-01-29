from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories

def test_basic_functionality():
    print("Testing YouTube Downloader")

    setup_directories()
    downloader = YouTubeDownloader()

    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    print("Testing video info extraction...")
    info = downloader.get_video_info(test_url)

    assert info is not None, "Failed to get video info"
    assert "title" in info, "Video info missing title"

    print(f"Video info retrieved: {info['title']}")


def test_example_gui_start():
    print("Example test")

if __name__ == "__main__":
    test_basic_functionality()
