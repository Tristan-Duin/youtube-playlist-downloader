"""
Simple GUI tests for coverage.
"""
import pytest
import json
from unittest.mock import patch, Mock
import gui


def test_index_route():
    """Test the index route."""
    with gui.app.test_client() as client:
        with patch('gui.render_template', return_value="test"):
            response = client.get('/')
            assert response.status_code == 200


def test_verify_ffmpeg_not_found():
    """Test FFmpeg verification when not found."""
    with gui.app.test_client() as client:
        with patch('gui.shutil.which', return_value=None):
            response = client.get('/api/verify-ffmpeg')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['ok'] is False


def test_verify_ffmpeg_success():
    """Test FFmpeg verification success."""
    with gui.app.test_client() as client:
        with patch('gui.shutil.which', return_value='/usr/bin/ffmpeg'):
            with patch('gui.subprocess.run') as mock_run:
                mock_run.return_value.returncode = 0
                response = client.get('/api/verify-ffmpeg')
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data['ok'] is True


def test_verify_ffmpeg_exception():
    """Test FFmpeg verification with exception."""
    with gui.app.test_client() as client:
        with patch('gui.shutil.which', return_value='/usr/bin/ffmpeg'):
            with patch('gui.subprocess.run', side_effect=Exception()):
                response = client.get('/api/verify-ffmpeg')
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data['ok'] is False


def test_download_in_progress():
    """Test download when already in progress."""
    gui.download_status['in_progress'] = True
    try:
        with gui.app.test_client() as client:
            response = client.post('/download', data={'url': 'https://www.youtube.com/watch?v=test'})
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'already in progress' in data['error']
    finally:
        gui.download_status['in_progress'] = False


def test_download_no_url():
    """Test download with no URL."""
    gui.download_status['in_progress'] = False
    with gui.app.test_client() as client:
        response = client.post('/download', data={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'enter a YouTube URL' in data['error']


def test_download_invalid_url():
    """Test download with invalid URL."""
    gui.download_status['in_progress'] = False
    with gui.app.test_client() as client:
        response = client.post('/download', data={'url': 'https://example.com'})
        assert response.status_code == 400


def test_download_playlist_url():
    """Test download with playlist URL."""
    gui.download_status['in_progress'] = False
    with gui.app.test_client() as client:
        response = client.post('/download', data={'url': 'https://www.youtube.com/playlist?list=test'})
        assert response.status_code == 400


def test_download_success():
    """Test successful download initiation."""
    gui.download_status['in_progress'] = False
    with gui.app.test_client() as client:
        with patch('gui.threading.Thread') as mock_thread:
            response = client.post('/download', data={'url': 'https://www.youtube.com/watch?v=test'})
            assert response.status_code == 200
            mock_thread.assert_called_once()


def test_status_route():
    """Test status route."""
    gui.download_status['messages'] = ['test']
    with gui.app.test_client() as client:
        response = client.get('/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'messages' in data


@patch('gui.downloader')
def test_download_worker_success(mock_downloader):
    """Test download worker."""
    mock_downloader.get_video_info.return_value = {'title': 'Test', 'uploader': 'Test', 'duration': 60}
    mock_downloader.download.return_value = True
    
    gui.download_status = {'in_progress': True, 'messages': [], 'current_video': None}
    gui.download_worker('https://www.youtube.com/watch?v=test', 'mp3', '720', 'best', None)
    
    assert not gui.download_status['in_progress']
    assert 'Download completed!' in gui.download_status['messages']


@patch('gui.downloader')
def test_download_worker_failure(mock_downloader):
    """Test download worker failure."""
    mock_downloader.get_video_info.return_value = None
    mock_downloader.download.return_value = False
    
    gui.download_status = {'in_progress': True, 'messages': [], 'current_video': None}
    gui.download_worker('https://www.youtube.com/watch?v=test', 'mp3', '720', 'best', None)
    
    assert not gui.download_status['in_progress']
    assert 'Download failed.' in gui.download_status['messages']


@patch('gui.downloader')
def test_download_worker_exception(mock_downloader):
    """Test download worker with exception."""
    mock_downloader.get_video_info.side_effect = Exception("Test error")
    
    gui.download_status = {'in_progress': True, 'messages': [], 'current_video': None}
    gui.download_worker('https://www.youtube.com/watch?v=test', 'mp3', '720', 'best', None)
    
    assert not gui.download_status['in_progress']
    assert 'Error: Test error' in gui.download_status['messages']


def test_add_message():
    """Test add_message function."""
    gui.download_status['messages'] = []
    gui.add_message("test")
    assert "test" in gui.download_status['messages']


@patch('gui.app.run')
def test_main_function(mock_run):
    """Test main function."""
    gui.main()
    mock_run.assert_called_once_with(debug=False, host='0.0.0.0', port=5000)


def test_gui_invalid_format():
    """Test GUI with invalid format."""
    gui.download_status['in_progress'] = False
    with gui.app.test_client() as client:
        response = client.post('/download', data={
            'url': 'https://www.youtube.com/watch?v=test',
            'format': 'avi'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'choose MP3 or MP4' in data['error']


def test_gui_invalid_resolution():
    """Test GUI with invalid resolution."""
    gui.download_status['in_progress'] = False
    with gui.app.test_client() as client:
        response = client.post('/download', data={
            'url': 'https://www.youtube.com/watch?v=test',
            'format': 'mp4',
            'resolution': '4K'
        })
        assert response.status_code == 400


def test_gui_invalid_bitrate():
    """Test GUI with invalid bitrate."""
    gui.download_status['in_progress'] = False
    with gui.app.test_client() as client:
        response = client.post('/download', data={
            'url': 'https://www.youtube.com/watch?v=test',
            'format': 'mp3',
            'bitrate': '999'
        })
        assert response.status_code == 400


@patch('gui.downloader')
def test_download_worker_with_custom_dir(mock_downloader):
    """Test download worker with custom directory."""
    mock_downloader.get_video_info.return_value = None
    mock_downloader.download.return_value = True
    
    gui.download_status = {'in_progress': True, 'messages': [], 'current_video': None}
    gui.download_worker('https://www.youtube.com/watch?v=test', 'mp3', '720', 'best', '/custom')
    
    assert not gui.download_status['in_progress']
    assert 'copied to: /custom' in ' '.join(gui.download_status['messages'])
