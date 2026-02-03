import sys
from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories

def main():
    print("\nYouTube Downloader MVP - College Project\n")

    # Initialize Option variables to default values
    copyDest = "none"
    noVid = False
    
    # Rudimentary parsing of args. We might need additional logic for validation.
    
    i = 0
    while i < len(sys.argv):
        match sys.argv[i].casefold():
            case '--copy' | '--c':
                copyDest = str(sys.argv[(i+1)])
            
            case '--audio' | '--a':
                noVid = True

            case '--help' | '--?':
           
                print("USAGE: python cli.py [options] [videolink]")
                print("\nwhere")
                print("\n    videolink:                   \"https://www.youtube.com/watch?v=VIDEO_ID\"")
                print("\n    options:")
                print("         --help  | --?           Display this help message.")      
                print("         --audio | --a           Download audio (Mp3) only.")
                print("         --copy  | --c  [path]   Copy download to specified folder path.\n")
                sys.exit(1)
        i=i+1

    # Required Arg for URL should be at end of the array
    url = sys.argv[(len(sys.argv)-1)]

    if len(sys.argv) < 2:
        print("Usage: python cli.py \"https://www.youtube.com/watch?v=VIDEO_ID\"")
        sys.exit(1)
    
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
    success = downloader.download_video(url, noVid, copyDest)
    
    if success:
        print("Download completed!")
    else:
        print("Download failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()