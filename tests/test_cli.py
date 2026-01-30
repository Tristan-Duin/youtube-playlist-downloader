import pytest
import sys
from unittest.mock import patch, Mock
import cli

def test_main_no_arguments(capsys):
    with patch.object(sys, 'argv', ['cli.py']):
        with pytest.raises(SystemExit) as exc_info:
            cli.main()
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Usage: python cli.py" in captured.out


def test_main_invalid_url(capsys):
    with patch.object(sys, 'argv', ['cli.py', 'https://example.com/video']):
        with pytest.raises(SystemExit) as exc_info:
            cli.main()
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Please provide a valid YouTube URL" in captured.out


@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_successful_download(mock_downloader_class, mock_setup, mock_video_info, capsys):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.get_video_info.return_value = mock_video_info
    mock_downloader.download_video.return_value = True
    
    url = 'https://www.youtube.com/watch?v=test'
    with patch.object(sys, 'argv', ['cli.py', url]):
        cli.main()
    
    mock_setup.assert_called_once()
    mock_downloader.get_video_info.assert_called_once_with(url)
    mock_downloader.download_video.assert_called_once_with(url)
    
    captured = capsys.readouterr()
    assert "Download completed!" in captured.out


@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_download_failure(mock_downloader_class, mock_setup, capsys):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.get_video_info.return_value = None
    mock_downloader.download_video.return_value = False
    
    with patch.object(sys, 'argv', ['cli.py', 'https://www.youtube.com/watch?v=test']):
        with pytest.raises(SystemExit) as exc_info:
            cli.main()
    
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Download failed." in captured.out
