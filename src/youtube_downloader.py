import yt_dlp
from pathlib import Path
from .config import DOWNLOADS_DIR, DEFAULT_FORMAT

class YouTubeDownloader:
    def __init__(self):
        self.output_dir = DOWNLOADS_DIR
        self.output_dir.mkdir(exist_ok=True)
    
    def download_video(self, url):
        try:
            ydl_opts = {
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'format': 'best[ext=mp4]/best',  # Prefer MP4 format for ease
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"Successfully downloaded video from: {url}")
            return True
            
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return False
    
    def get_video_info(self, url):
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0)
                }
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None