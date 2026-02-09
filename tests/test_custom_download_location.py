"""
Simple tests for custom download location functionality.
"""
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from src.youtube_downloader import YouTubeDownloader
import gui


def test_path_validation(temp_downloads_dir):
    with patch('src.youtube_downloader.DOWNLOADS_DIR', temp_downloads_dir):
        downloader = YouTubeDownloader()
        
    temp_dir = Path(tempfile.mkdtemp())
    is_valid, result = downloader._validate_path(str(temp_dir))
    assert is_valid is True
    
    is_valid, error_msg = downloader._validate_path("invalid<>path")
    assert is_valid is False
    assert "Invalid path" in error_msg


def test_file_copying(temp_downloads_dir):
    with patch('src.youtube_downloader.DOWNLOADS_DIR', temp_downloads_dir):
        downloader = YouTubeDownloader()
        
    test_file = downloader.output_dir / "test.mp4"
    test_file.write_text("test content")
    
    custom_dir = Path(tempfile.mkdtemp())
    downloader._copy_specific_files(str(custom_dir), ["test.mp4"])
    
    copied_file = custom_dir / "test.mp4"
    assert copied_file.exists()
    assert copied_file.read_text() == "test content"


def test_flask_endpoint_with_custom_directory():
    gui.download_status['in_progress'] = False
    
    with gui.app.test_client() as client:
        with patch('gui.threading.Thread') as mock_thread:
            response = client.post('/download', data={
                'url': 'https://www.youtube.com/watch?v=test',
                'custom_directory': '/custom/path'
            })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == 'Download started'
    
    args = mock_thread.call_args[1]['args']
    assert args[4] == '/custom/path'


def test_flask_endpoint_without_custom_directory():
    gui.download_status['in_progress'] = False
    
    with gui.app.test_client() as client:
        with patch('gui.threading.Thread') as mock_thread:
            response = client.post('/download', data={
                'url': 'https://www.youtube.com/watch?v=test'
            })
    
    assert response.status_code == 200
    
    args = mock_thread.call_args[1]['args']
    assert args[4] is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
