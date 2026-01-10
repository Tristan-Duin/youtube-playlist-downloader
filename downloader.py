import sys
from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories

def main():
    print("YouTube Downloader MVP - College Project")
    print("=" * 40)
    
    if len(sys.argv) != 2:
        print("Usage: python downloader.py \"https://www.youtube.com/watch?v=VIDEO_ID\"")
        print("\nExample:")
        print("python downloader.py \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"")
        sys.exit(1)
    
    url = sys.argv[1]
    
    if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
        print("Error: Please provide a valid YouTube URL")
        sys.exit(1)
    
    setup_directories()
    
    downloader = YouTubeDownloader()
    
    print(f"Getting video information...")
    info = downloader.get_video_info(url)
    
    if info:
        print(f"Title: {info['title']}")
        print(f"Uploader: {info['uploader']}")
        if info['duration']:
            minutes = info['duration'] // 60
            seconds = info['duration'] % 60
            print(f"Duration: {minutes}m {seconds}s")
        print()
    
    print("Starting download...")
    success = downloader.download_video(url)
    
    if success:
        print("Download completed check the  downloads folder.")
    else:
        print("Download failed please try again and double check the URL is valid.")
        sys.exit(1)

if __name__ == "__main__":
    main()