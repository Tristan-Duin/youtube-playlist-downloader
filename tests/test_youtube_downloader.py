"""
Test core functionality of the downloader and ensure it is within expected behavior.
"""
import pytest
from unittest.mock import Mock, patch
from src.youtube_downloader import YouTubeDownloader


@pytest.fixture
def downloader(temp_downloads_dir):
    with patch('src.youtube_downloader.DOWNLOADS_DIR', temp_downloads_dir):
        return YouTubeDownloader()

def test_init_creates_output_directory(temp_downloads_dir):
    test_dir = temp_downloads_dir / 'new_dir'
    with patch('src.youtube_downloader.DOWNLOADS_DIR', test_dir):
        assert not test_dir.exists()
        
        downloader = YouTubeDownloader()
        
        assert test_dir.exists()
        assert downloader.output_dir == test_dir


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_get_video_info_success(mock_ytdl_class, downloader, mock_video_info):
    mock_ytdl = Mock()
    mock_ytdl.extract_info.return_value = mock_video_info
    mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
    
    result = downloader.get_video_info('https://www.youtube.com/watch?v=test')
    
    assert result == mock_video_info
    mock_ytdl.extract_info.assert_called_once_with(
        'https://www.youtube.com/watch?v=test', download=False
    )


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_get_video_info_failure(mock_ytdl_class, downloader, capsys):
    mock_ytdl = Mock()
    mock_ytdl.extract_info.side_effect = Exception("Test error")
    mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
    
    result = downloader.get_video_info('https://www.youtube.com/watch?v=test')
    
    assert result is None
    captured = capsys.readouterr()
    assert "Error getting video info: Test error" in captured.out


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_download_success(mock_ytdl_class, downloader, capsys):
    mock_ytdl = Mock()
    mock_ytdl.download.return_value = None  # Pretty sure if no exception is thrown that means success
    mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
    
    result = downloader.download('https://www.youtube.com/watch?v=test', format='mp4')
    
    assert result is True
    mock_ytdl.download.assert_called_once_with(['https://www.youtube.com/watch?v=test'])
    captured = capsys.readouterr()
    assert "Successfully downloaded MP4 from: https://www.youtube.com/watch?v=test" in captured.out


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
@patch.object(YouTubeDownloader, '_try_fallback')
def test_download_with_fallback(mock_fallback, mock_ytdl_class, downloader, capsys):
    mock_ytdl = Mock()
    mock_ytdl.download.side_effect = Exception("Primary download error")
    mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
    
    mock_fallback.return_value = True
    
    result = downloader.download('https://www.youtube.com/watch?v=test', format='mp4')
    
    assert result is True
    mock_fallback.assert_called_once_with('https://www.youtube.com/watch?v=test', 'mp4', '720', 'best', None)
    captured = capsys.readouterr()
    assert "Primary download failed" in captured.out
