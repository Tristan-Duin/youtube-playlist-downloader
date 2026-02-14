from flask import Flask, render_template, request, jsonify
import threading
from typing import Optional
import shutil
import subprocess
from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories, HISTORY_FILE
app = Flask(__name__)

setup_directories()
downloader = YouTubeDownloader()
download_status = {
    'in_progress': False,
    'messages': [],
    'current_video': None
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

    lowered = url.lower()
    if 'list=' in lowered or '/playlist' in lowered:
        return jsonify({'error': 'Playlist downloads are not supported in this release'}), 400

    if selected_format not in ('mp3', 'mp4'):
        return jsonify({'error': 'Please choose MP3 or MP4'}), 400

    if selected_format == 'mp4' and resolution not in ('1080', '720', '480', '360'):
        return jsonify({'error': 'Invalid resolution selection'}), 400

    if selected_format == 'mp3' and bitrate not in ('best', '320', '256', '192', '160', '128', '96'):
        return jsonify({'error': 'Invalid bitrate selection'}), 400

    download_status['messages'] = []
    download_status['in_progress'] = True
    download_status['current_video'] = None

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
            if custom_directory:
                add_message(f"Download completed and copied to: {custom_directory}")
            else:
                add_message("Download completed!")
            write_history(info['title'])
        else:
            add_message("Download failed.")

    except Exception as e:
        add_message(f"Error: {str(e)}")

    finally:
        download_status['in_progress'] = False
def write_history(title: str) -> None:
    try:
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(title + '\n')   
    except Exception as e:
        print(f"Error writing to history file: {e}")    

def read_history() -> list[str]:
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return [line for line in f if line.strip()]
    except FileNotFoundError:
        return []
@app.route('/history')
def history():
    return jsonify({'history': read_history()})
def main() -> None:
    """Entry point for the GUI application."""
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
