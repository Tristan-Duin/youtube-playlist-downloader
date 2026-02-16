from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories
from typing import Annotated
import shutil
import subprocess
import typer

app = typer.Typer()

@app.command()
def main(
    url: Annotated[
        str,
        typer.Argument(help='\"https://www.youtube.com/watch?v=VIDEO_ID\"')
    ],
    audio_only: Annotated[
        str,
        typer.Option("--audio", "-a", help='Download MP3 Audio only.')
    ] = None,
    resolution: Annotated[
        str,
        typer.Option("--video-res","-v", help='Video Resolution.')
    ] = None,
    output_dir: Annotated[
        str | None,
        typer.Option("--output-dir", "-o", help='Copy download to specified folder.')
    ] = None,
):

    print("\nYouTube Downloader - College Project\n")

    # Catch Invalid Video URL
    if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
        raise ValueError(f"Error: {url} is not a valid YouTube URL.")

    verify_ffmpeg()

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
    format = 'mp3' if audio_only else 'mp4'
    
    success = downloader.download(url, format, resolution, bitrate=audio_only, output_dir=output_dir)
    
    if success:
        print("Download completed!")
    else:
        raise Exception("Error: Download failed.")
      
def verify_ffmpeg():
    ffmpeg_path = shutil.which('ffmpeg')
    if not ffmpeg_path:
        raise Exception("Error: FFmpeg is not installed.")

    verified = subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            text=True,
            timeout=3
        )
    
    if not verified:
        raise Exception("Error: FFmpeg validation failed.")
    
    print("FFmpeg Install Verified.")

if __name__ == "__main__":
    app()