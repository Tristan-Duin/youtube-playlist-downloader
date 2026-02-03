import sys
from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories


def main():
    print("YouTube Downloader MVP - College Project")

    """ Initialize Option variables to default values """
    copyVid = False
    copyDest = ""
    noVid = False
    
    if len(sys.argv) < 2:
        print("Usage: python cli.py \"https://www.youtube.com/watch?v=VIDEO_ID\"")
        sys.exit(1)
    
    """Required Arg for URL should be at end of the array"""
    url = sys.argv[(len(sys.argv)-1)]
    
    if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
        print("Error: Please provide a valid YouTube URL")
        sys.exit(1)

    """ Rudimentary parsing of args. We might need additional logic for validation """    
    if len(sys.argv) > 2:
        i = 0
        while i < len(sys.argv):
            print("Testing index: ", i, " is ", sys.argv[i])
            match sys.argv[i]:

                case '-d':
                    print("Copy enabled")
                    """ TO-DO: This arg needs to verify the folder string following -d is valid """
                    """ TO-DO: Add parameters to  main script to receive a boolean and the path string """
                    copyVid = True
                    copyDest = str(sys.argv[(i+1)])
                    print("copyVid value: ", copyVid)
                    print("destination: ", copyDest)
                
                case '-a':
                    print("Mp3 enabled")
                    """ TO-DO: Add a parameter to the main script to recieve the boolean value """
                    noVid = True
                    print("noVid value: ", noVid)

                case '-x':
                    """ TO-DO: Add more option args here, or remove this placeholder """
                    print("I Want To Believe ☺")

            i=i+1
            print("\n<-= Iterate =->\n")
    
    
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
    success = downloader.download_video(url,noVid,copyVid,copyDest)
    
    if success:
        print("Download completed!")
    else:
        print("Download failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()