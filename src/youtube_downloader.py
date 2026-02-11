import yt_dlp
import shutil
import os
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List
from .config import DOWNLOADS_DIR, DEFAULT_FORMAT

class YouTubeDownloader:
    # Common HTTP headers used across requests
    _COMMON_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Sec-Fetch-Mode': 'navigate',
    }

    _FALLBACK_HEADERS = {
        'User-Agent': 'com.google.android.youtube/19.02.39 (Linux; U; Android 11) gzip'
    }
    
    def __init__(self) -> None:
        self.output_dir = DOWNLOADS_DIR
        self.output_dir.mkdir(exist_ok=True)

    def download(self, url: str, format: str = 'mp4', resolution: str = '720', bitrate: str = 'best', output_dir: Optional[str] = None) -> bool:
        """Unified download method for both video and audio downloads.
            
        Returns:
            bool: True if download succeeded, False otherwise
        """
        try:
            downloads_path = Path(self.output_dir)
            files_before = set(f.name for f in downloads_path.iterdir() if f.is_file()) if downloads_path.exists() else set()

            ydl_opts = self._get_download_options(format, resolution, bitrate)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"Successfully downloaded {format.upper()} from: {url}")

            if output_dir:
                files_after = set(f.name for f in downloads_path.iterdir() if f.is_file()) if downloads_path.exists() else set()
                new_files = files_after - files_before
                if new_files:
                    self._copy_specific_files(output_dir, list(new_files))
                else:
                    print("Warning: No new files detected after download")
            return True

        except Exception as e:
            print(f"Primary download failed: {str(e)}")
            print("Trying fallback with simpler format selection...")
            return self._try_fallback(url, format, resolution, bitrate, output_dir)
    

    def _get_download_options(self, format: str, resolution: str, bitrate: str) -> Dict[str, Any]:
        """Get yt-dlp download options based on format and quality settings."""
        base_opts: Dict[str, Any] = {
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'retries': 10,
            'fragment_retries': 10,
            'socket_timeout': 30,
            'extractor_retries': 10,
            'http_headers': self._COMMON_HEADERS,
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
            'noplaylist': True,
        }

        if format == 'mp3':
            base_opts['format'] = 'bestaudio/best'
            base_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
            if bitrate and bitrate != 'best':
                base_opts['postprocessor_args'] = ['-b:a', f'{bitrate}k']
        else:
            # mp4
            if resolution and resolution in ('1080', '720', '480', '360'):
                base_opts['format'] = (
                    f"bestvideo[ext=mp4][height<={resolution}]+bestaudio[ext=m4a]/"
                    f"best[ext=mp4][height<={resolution}]/"
                    f"best[height<={resolution}]/"
                    f"best[protocol!*=m3u8][height<={resolution}]/best[protocol!*=m3u8]/best"
                )
            else:
                base_opts['format'] = (
                    "bestvideo[ext=mp4]+bestaudio[ext=m4a]/"
                    "best[ext=mp4]/"
                    "best[protocol!*=m3u8]/best"
                )
            base_opts['merge_output_format'] = 'mp4'

        return base_opts

    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        try:
            ydl_opts = {
                'quiet': True,
                'retries': 5,
                'socket_timeout': 30,
                'http_headers': self._COMMON_HEADERS,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'player_skip': ['configs'],
                    }
                },
                'ignoreerrors': True,
                'noplaylist': True,
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

    def _try_fallback(self, url: str, format: str, resolution: str, bitrate: str, output_dir: Optional[str]) -> bool:
        """Try a fallback download with simplified options when the primary download fails."""
        try:
            downloads_path = Path(self.output_dir)
            files_before = set(f.name for f in downloads_path.iterdir() if f.is_file()) if downloads_path.exists() else set()

            ydl_opts: Dict[str, Any] = {
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'retries': 5,
                'fragment_retries': 5,
                'socket_timeout': 45,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android'],
                    }
                },
                'http_headers': self._FALLBACK_HEADERS,
                'sleep_interval': 2,
                'max_sleep_interval': 10,
                'ignoreerrors': True,
                'noplaylist': True,
            }

            # Configure specific options for fallback
            if format == 'mp3':
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
                if bitrate and bitrate != 'best':
                    ydl_opts['postprocessor_args'] = ['-b:a', f'{bitrate}k']
            else:
                if resolution and resolution in ('1080', '720', '480', '360'):
                    ydl_opts['format'] = f"best[height<={resolution}]/best"
                else:
                    ydl_opts['format'] = 'best'
                ydl_opts['merge_output_format'] = 'mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"Fallback download successful for: {url}")

            if output_dir:
                files_after = set(f.name for f in downloads_path.iterdir() if f.is_file()) if downloads_path.exists() else set()
                new_files = files_after - files_before
                if new_files:
                    self._copy_specific_files(output_dir, list(new_files))
                else:
                    print("Warning: No new files detected after fallback download")
            return True

        except Exception as e:
            print(f"Fallback download also failed: {str(e)}")
            print("Media may not be available or have restrictions.")
            return False

    def _validate_path(self, path: str) -> Tuple[bool, str]:
        """Validate that the destination path is safe and accessible."""
        try:
            path_obj = Path(path).resolve()
            # Ensure path is an absolute path
            if not path_obj.is_absolute():
                return False, "Path must be absolute"
            # Create directory structure if it doesn't already exist
            path_obj.mkdir(parents=True, exist_ok=True)
            # Verify write permissions
            if not os.access(path_obj.parent, os.W_OK):
                return False, "No write permission to destination directory"
            return True, str(path_obj)
        except Exception as e:
            return False, f"Invalid path: {str(e)}"

    def _copy_specific_files(self, copyDest: str, filenames: List[str]) -> None:
        """Copy specified files from downloads directory to custom destination."""
        if not copyDest or not filenames:
            return

        is_valid, result = self._validate_path(copyDest)
        if not is_valid:
            print(f"Invalid destination path: {result}")
            return

        try:
            dest_path = Path(result)
            downloads_path = Path(self.output_dir)

            print(f"Copying {len(filenames)} file(s) to '{dest_path}'")

            copied_files = []
            for filename in filenames:
                source_file = downloads_path / filename

                if not source_file.exists():
                    print(f"File {filename} not found in downloads directory")
                    continue

                try:
                    dest_file_path = dest_path / filename
                    shutil.copy2(source_file, dest_file_path)
                    copied_files.append(filename)
                    print(f"Copied: {filename} to {dest_file_path}")
                except Exception as file_error:
                    print(f"Failed to copy {filename}: {str(file_error)}")

            if copied_files:
                print(f"Successfully copied {len(copied_files)} file(s) to {dest_path}")
            else:
                print("No files were copied")

        except Exception as e:
            print(f"Copy failed: {str(e)}")
            raise
