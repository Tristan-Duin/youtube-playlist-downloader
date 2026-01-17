import sys
from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories

def main():
    print("YouTube Downloader MVP - College Project")
    
    if len(sys.argv) != 2:
        print("Usage: python cli.py \"https://www.youtube.com/watch?v=VIDEO_ID\"")
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
        print("Download completed!")
    else:
        print("Download failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()