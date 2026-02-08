from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(url: Annotated[str, typer.Argument(help='\"https://www.youtube.com/watch?v=VIDEO_ID\"')],
         noVid: Annotated[bool,typer.Option("--audio", "-a", help="Download MP3 Audio only.")] = False,
         copyDest: Annotated[str, typer.Option("--copy", "-c", help="Copy download to specified folder.")] = None,
         ):

    print("\nYouTube Downloader - College Project\n")

    # Catch Invalid Video URL
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
    app()