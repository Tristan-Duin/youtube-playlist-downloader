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
    validate_install: Annotated[
        bool | None,
        typer.Option("--ffmpeg", help='Verify FFmpeg is installed.')
    ] = None

):

    print("\nYouTube Downloader - College Project\n")

    verify_ffmpeg(validate_install)
    
    # Catch Invalid Video URL
    if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
        raise ValueError(f"Error: {url} is not a valid YouTube URL.")

    setup_directories()
    
    downloader = YouTubeDownloader()
    
    # Check if this is a playlist
    if downloader.is_playlist_url(url):
        print(f"Getting playlist information...")
        playlist_info = downloader.get_playlist_info(url)
        
        if playlist_info:
            print(f"Playlist: {playlist_info['title']}")
            print(f"Uploader: {playlist_info['uploader']}")
            print(f"Videos in playlist: {playlist_info['video_count']}")
            print()
        
        # How we are tracking the status
        def progress_callback(current: int, total: int, video_title: str) -> None:
            print(f"[{current}/{total}] {video_title}")
        
        print("Starting playlist download...")
        format = 'mp3' if audio_only else 'mp4'
        success = downloader.download(url, format=format, resolution=resolution, output_dir=output_dir, progress_callback=progress_callback)
    else:
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
        success = downloader.download(url, format=format, resolution=resolution, bitrate=audio_only, output_dir=output_dir)
    
    if success:
        print("Download completed!")
    else:
        raise Exception("Error: Download failed.")
      
def verify_ffmpeg(validate_install):
    ffmpeg_path = shutil.which('ffmpeg')
    if not ffmpeg_path:
        raise Exception(f"Error: FFmpeg is not installed.\n")

    verified = subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            text=True,
            timeout=3
        )
    
    if not verified:
        raise Exception(f"Error: FFmpeg validation failed.\n")
    
    if validate_install != None:
        print(f"FFmpeg Install Verified.\n")

if __name__ == "__main__":
    app()