"""
Test script to verify playlist functionality with real URLs.
"""

from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories

def test_playlist_urls():
    """Test the playlist URLs that were failing."""
    
    setup_directories()
    downloader = YouTubeDownloader()
    
    test_urls = [
        'https://www.youtube.com/watch?v=HerCR8bw_GE&list=PLRqwX-V7Uu6Zy51Q-x9tMWIv9cueOFTFA',
        'https://www.youtube.com/watch?v=9RfVp-GhKfs&list=PLardzfp0_hdqVWEaf598_7esicfyxXRy8'
    ]
    
    print("Testing playlist functionality...\n")
    
    for i, url in enumerate(test_urls, 1):
        print(f"Testing URL {i}:")
        print(f"{url}")
        
        is_playlist = downloader.is_playlist_url(url)
        print(f"Playlist detected: {is_playlist}")
        
        if is_playlist:
            try:
                info = downloader.get_playlist_info(url)
                if info:
                    print(f"Playlist info retrieved successfully:")
                    print(f"- Title: {info['title']}")
                    print(f"- Uploader: {info['uploader']}")  
                    print(f"- Video count: {info['video_count']}")
                    print(f"- ID: {info['id']}")
                else:
                    print("Failed to get playlist info")
            except Exception as e:
                print(f"Error getting playlist info: {e}")
        else:
            print("URL not detected as playlist")
        
        print()
    
    print("Test completed! If you see checkmarks above, playlist downloads should work.")
    print("\nTo download a playlist, you can now use:")
    print("python cli.py \"<playlist_url>\"")
    print("or")
    print("python gui.py  (and paste the playlist URL in the web interface)")

if __name__ == "__main__":
    test_playlist_urls()