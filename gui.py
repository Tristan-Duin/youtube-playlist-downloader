from flask import Flask, render_template, request, jsonify
import threading
from typing import Optional
import shutil
import subprocess
from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories
from pathlib import Path
app = Flask(__name__)

setup_directories()
downloader = YouTubeDownloader()
download_status = {
    'in_progress': False,
    'messages': [],
    'current_video': None,
    'is_playlist': False,
    'playlist_info': None,
    'current_video_index': 0,
    'total_videos': 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.get('/api/verify-ffmpeg')
def verify_ffmpeg():
    ffmpeg_path = shutil.which('ffmpeg')
    if not ffmpeg_path:
        return jsonify({'ok': False}), 200

    try:
        completed = subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            text=True,
            timeout=3
        )
        return jsonify({'ok': completed.returncode == 0}), 200
    except Exception:
        return jsonify({'ok': False}), 200

@app.route('/download', methods=['POST'])
def download():
    if download_status['in_progress']:
        return jsonify({'error': 'Download already in progress'}), 400

    url = request.form.get('url', '').strip()

    selected_format = (request.form.get('format', 'mp3') or 'mp3').strip().lower()
    resolution = (request.form.get('resolution', '720') or '720').strip()
    bitrate = (request.form.get('bitrate', 'best') or 'best').strip()

    custom_directory = request.form.get('custom_directory', '').strip() or None

    if not url:
        return jsonify({'error': 'Please enter a YouTube URL'}), 400

    if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
        return jsonify({'error': 'Please provide a valid YouTube URL'}), 400

    if selected_format not in ('mp3', 'mp4'):
        return jsonify({'error': 'Please choose MP3 or MP4'}), 400

    if selected_format == 'mp4' and resolution not in ('1080', '720', '480', '360'):
        return jsonify({'error': 'Invalid resolution selection'}), 400

    if selected_format == 'mp3' and bitrate not in ('best', '320', '256', '192', '160', '128', '96'):
        return jsonify({'error': 'Invalid bitrate selection'}), 400

    download_status['messages'] = []
    download_status['in_progress'] = True
    download_status['current_video'] = None
    download_status['is_playlist'] = False
    download_status['playlist_info'] = None
    download_status['current_video_index'] = 0
    download_status['total_videos'] = 0

    thread = threading.Thread(
        target=download_worker,
        args=(url, selected_format, resolution, bitrate, custom_directory)
    )
    thread.daemon = True
    thread.start()

    return jsonify({'success': 'Download started'})

@app.route('/status')
def status():
    return jsonify(download_status)

def add_message(message: str) -> None:
    download_status['messages'].append(message)

def download_worker(url: str, selected_format: str, resolution: str, bitrate: str, custom_directory: Optional[str] = None) -> None:
    try:
        # Check if this is a playlist
        if downloader.is_playlist_url(url):
            download_status['is_playlist'] = True
            add_message("Getting playlist information...")
            
            playlist_info = downloader.get_playlist_info(url)
            if playlist_info:
                download_status['playlist_info'] = playlist_info
                download_status['total_videos'] = playlist_info['video_count']
                add_message(f"Playlist: {playlist_info['title']}")
                add_message(f"Uploader: {playlist_info['uploader']}")
                add_message(f"Videos in playlist: {playlist_info['video_count']}")
                add_message("")
            
            # Enable tracking for GUI
            def progress_callback(current: int, total: int, video_title: str) -> None:
                download_status['current_video_index'] = current
                download_status['total_videos'] = total
                add_message(f"Downloading video {current}/{total}: {video_title}")
            
            add_message("Starting playlist download...")
            success = downloader.download(
                url=url,
                format=selected_format,
                resolution=resolution,
                bitrate=bitrate,
                output_dir=custom_directory,
                progress_callback=progress_callback
            )
        else:
            # Not downloading a playlist
            add_message("Getting video information...")
            info = downloader.get_video_info(url)

            if info:
                download_status['current_video'] = info
                add_message(f"Title: {info['title']}")
                add_message(f"Uploader: {info['uploader']}")
                if info['duration']:
                    minutes = info['duration'] // 60
                    seconds = info['duration'] % 60
                    add_message(f"Duration: {minutes}m {seconds}s")
                add_message("")

            add_message("Starting download...")
            success = downloader.download(
                url=url,
                format=selected_format,
                resolution=resolution,
                bitrate=bitrate,
                output_dir=custom_directory
            )

        if success:
            if download_status['is_playlist']:
                if custom_directory:
                    add_message(f"Playlist download completed and copied to: {custom_directory}")
                else:
                    add_message("Playlist download completed!")
            else:
                if custom_directory:
                    add_message(f"Download completed and copied to: {custom_directory}")
                else:
                    add_message("Download completed!")
        else:
            if download_status['is_playlist']:
                add_message("Playlist download failed.")
            else:
                add_message("Download failed.")

    except Exception as e:
        add_message(f"Error: {str(e)}")

    finally:
        download_status['in_progress'] = False  

def get_download_history():
    downloads_path = Path("downloads")
    if not downloads_path.exists():
        return []
    
    files = []
    for file_path in downloads_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.mp4', '.mp3']:
            files.append({
                'filename': file_path.name,
                'format': file_path.suffix[1:].upper(),
                'size': file_path.stat().st_size,
                'downloaded': file_path.stat().st_mtime
            })
    print(files)
    return sorted(files, key=lambda x: x['downloaded'], reverse=True)
@app.route('/history')
def history():
    return jsonify({'history': get_download_history()})
def main() -> None:
    """Entry point for the GUI application."""
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
