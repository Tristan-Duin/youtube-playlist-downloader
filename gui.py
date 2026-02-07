from flask import Flask, render_template, request, jsonify
import threading
from src.youtube_downloader import YouTubeDownloader
from src.config import setup_directories

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

@app.route('/download', methods=['POST'])
def download():
    if download_status['in_progress']:
        return jsonify({'error': 'Download already in progress'}), 400
    
    url = request.form.get('url', '').strip()
    custom_directory = request.form.get('custom_directory', '').strip() or None
    
    if not url:
        return jsonify({'error': 'Please enter a YouTube URL'}), 400
    
    if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
        return jsonify({'error': 'Please provide a valid YouTube URL'}), 400
    
    download_status['messages'] = []
    download_status['in_progress'] = True
    download_status['current_video'] = None
    thread = threading.Thread(target=download_worker, args=(url, custom_directory))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': 'Download started'})

@app.route('/status')
def status():
    return jsonify(download_status)

def add_message(message):
    download_status['messages'].append(message)

def download_worker(url, custom_directory=None):
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
        success = downloader.download_video(url, False, custom_directory)
        
        if success:
            if custom_directory:
                add_message(f"Download completed and copied to: {custom_directory}")
            else:
                add_message("Download completed!")
        else:
            add_message("Download failed.")
            
    except Exception as e:
        add_message(f"Error: {str(e)}")
    
    finally:
        download_status['in_progress'] = False

def main():
    """Entry point for the GUI application."""
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
