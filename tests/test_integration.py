from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories


def test_video_info_extraction():
    setup_directories()
    downloader = YouTubeDownloader()
    
    # Stable video for testing ;D
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    info = downloader.get_video_info(test_url)
    
    assert info is not None, "Failed to get video info"
    assert "title" in info, "Video info missing title"
    assert "uploader" in info, "Video info missing uploader"
    
    print(f"Successfully retrieved info for: {info['title']}")


if __name__ == "__main__":
    # We handle the testing uniquely here because we are using real network traffic
    print("Integration testing...")
    print("NOTE: This makes real network requests and may take time.")
    test_video_info_extraction()
    print("Integration test completed!")
