import yt_dlp
import os
from pathlib import Path
from .config import DOWNLOADS_DIR, DEFAULT_FORMAT

class YouTubeDownloader:
    def __init__(self):
        self.output_dir = DOWNLOADS_DIR
        self.output_dir.mkdir(exist_ok=True)
    
    """ Parameters added for arguments: Refactor for clarity 
        noVid = {bool} option to DL mp3 only
        copyVid = {bool} option to copy the download to a specified folder
        copyDest = {str} path of destination folder for copy """
    def download_video(self, url, noVid, copyVid, copyDest):
        try:
            ydl_opts = {
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'format': 'best[protocol!*=m3u8][height<=720]/best[protocol!*=m3u8]/best[height<=720]/best',
                'retries': 10,
                'fragment_retries': 10,
                'socket_timeout': 30,
                'extractor_retries': 10,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'player_skip': ['configs'],
                    }
                },
                'sleep_interval': 1,
                'max_sleep_interval': 5,
                'ignoreerrors': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"Successfully downloaded video from: {url}") 

            if (copyVid):
                waffle = str(ydl('%(title)s.%(ext)s'))
                print(waffle)
                self._copy_to_destination(copyDest)

            return True
            
        except Exception as e:
            print(f"Primary download failed: {str(e)}")
            print("Trying fallback with simpler format selection...")
            return self._try_fallback_download(url, noVid, copyVid, copyDest)
    
    def get_video_info(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'retries': 5,
                'socket_timeout': 30,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                },
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'player_skip': ['configs'],
                    }
                },
                'ignoreerrors': True,
            }
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
    
    def _try_fallback_download(self, url, noVid, copyVid, copyDest):
        try:
            ydl_opts = {
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'format': 'worst[protocol!=m3u8]/best[protocol!=m3u8]/worst',
                'retries': 5,
                'fragment_retries': 5,
                'socket_timeout': 45,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android'],
                    }
                },
                'http_headers': {
                    'User-Agent': 'com.google.android.youtube/19.02.39 (Linux; U; Android 11) gzip'
                },
                'sleep_interval': 2,
                'max_sleep_interval': 10,
                'ignoreerrors': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"Fallback download successful for: {url}")

            if (copyVid):
                self._copy_to_destination(copyDest)

            return True
            
        except Exception as e:
            print(f"Fallback download also failed: {str(e)}")
            print("Video may not be available or have restrictions.")
            return False
        
    def _copy_to_destination(self, copyDest):
        """ TO-DO: Clean-up messaging and exceptions.
          (currently reports "Created" if already exists)
          Add specific cases for created, blank if exists, exception types."""
        try:
            os.makedirs(copyDest,exist_ok=True)
            print(f"Directory '{copyDest}' created")
        
        except Exception as e:
            print(f"Copy Destination Path Invalid.")
            print({str(e)})

        """ TO-DO: Code for copying the actual downloaded file.
            Get filename from YT-DLP???"""
        
                              
                              