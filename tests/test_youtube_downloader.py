"""
Comprehensive tests for YouTubeDownloader functionality.
"""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
import os

from src.youtube_downloader import YouTubeDownloader


@pytest.fixture
def downloader(temp_downloads_dir):
    with patch('src.youtube_downloader.DOWNLOADS_DIR', temp_downloads_dir):
        return YouTubeDownloader()


# Initialization Tests
def test_init_creates_output_directory(temp_downloads_dir):
    """Test that YouTubeDownloader creates output directory."""
    test_dir = temp_downloads_dir / 'new_dir'
    with patch('src.youtube_downloader.DOWNLOADS_DIR', test_dir):
        assert not test_dir.exists()
        
        downloader = YouTubeDownloader()
        
        assert test_dir.exists()
        assert downloader.output_dir == test_dir


# Video Info Tests
@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_get_video_info_success(mock_ytdl_class, downloader, mock_video_info):
    """Test successful video info extraction."""
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
    """Test video info extraction failure."""
    mock_ytdl = Mock()
    mock_ytdl.extract_info.side_effect = Exception("Test error")
    mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
    
    result = downloader.get_video_info('https://www.youtube.com/watch?v=test')
    
    assert result is None
    captured = capsys.readouterr()
    assert "Error getting video info: Test error" in captured.out


# Download Video Tests
@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_download_video_success(mock_ytdl_class, downloader, capsys):
    """Test successful video download."""
    mock_ytdl = Mock()
    mock_ytdl.download.return_value = None
    mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
    
    result = downloader.download_video('https://www.youtube.com/watch?v=test', False, None)
    
    assert result is True
    mock_ytdl.download.assert_called_once_with(['https://www.youtube.com/watch?v=test'])
    captured = capsys.readouterr()
    assert "Successfully downloaded video from: https://www.youtube.com/watch?v=test" in captured.out


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
@patch.object(YouTubeDownloader, '_try_fallback_download')
def test_download_video_with_fallback(mock_fallback, mock_ytdl_class, downloader, capsys):
    """Test video download with fallback."""
    mock_ytdl = Mock()
    mock_ytdl.download.side_effect = Exception("Primary download error")
    mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
    mock_fallback.return_value = True
    
    result = downloader.download_video('https://www.youtube.com/watch?v=test', False, None)
    
    assert result is True
    mock_fallback.assert_called_once_with('https://www.youtube.com/watch?v=test', False, None)
    captured = capsys.readouterr()
    assert "Primary download failed" in captured.out


# Download Media Tests
@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_download_media_success(mock_ytdl, downloader):
    """Test download_media method."""
    mock_ytdl_instance = Mock()
    mock_ytdl_instance.download.return_value = None
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
    
    result = downloader.download_media('https://www.youtube.com/watch?v=test', 'mp3', '720', '320', None)
    assert result is True


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
@patch.object(YouTubeDownloader, '_try_fallback_download_media')
def test_download_media_fallback(mock_fallback, mock_ytdl, downloader):
    """Test download_media with fallback."""
    mock_ytdl_instance = Mock()
    mock_ytdl_instance.download.side_effect = Exception("Error")
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
    mock_fallback.return_value = True
    
    result = downloader.download_media('https://www.youtube.com/watch?v=test', 'mp3', '720', '320', None)
    assert result is True
    mock_fallback.assert_called_once()


# YDL Options Builder Tests
def test_build_ydl_opts_mp3(downloader):
    """Test _build_ydl_opts for MP3."""
    opts = downloader._build_ydl_opts('mp3', '720', '320')
    assert opts['format'] == 'bestaudio/best'
    assert opts['postprocessors'][0]['preferredcodec'] == 'mp3'
    assert opts['postprocessor_args'] == ['-b:a', '320k']


def test_build_ydl_opts_mp3_best(downloader):
    """Test _build_ydl_opts for MP3 with best bitrate."""
    opts = downloader._build_ydl_opts('mp3', '720', 'best')
    assert 'postprocessor_args' not in opts


def test_build_ydl_opts_mp4(downloader):
    """Test _build_ydl_opts for MP4."""
    opts = downloader._build_ydl_opts('mp4', '720', 'best')
    assert 'bestvideo[ext=mp4][height<=720]' in opts['format']
    assert opts['merge_output_format'] == 'mp4'


def test_build_ydl_opts_mp4_no_resolution(downloader):
    """Test _build_ydl_opts for MP4 without resolution."""
    opts = downloader._build_ydl_opts('mp4', None, 'best')
    assert 'bestvideo[ext=mp4]+bestaudio[ext=m4a]' in opts['format']


# Fallback Download Tests
@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_try_fallback_download_success(mock_ytdl, downloader):
    """Test _try_fallback_download success."""
    mock_ytdl_instance = Mock()
    mock_ytdl_instance.download.return_value = None
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
    
    result = downloader._try_fallback_download('https://www.youtube.com/watch?v=test', False, None)
    assert result is True


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_try_fallback_download_failure(mock_ytdl, downloader):
    """Test _try_fallback_download failure."""
    mock_ytdl_instance = Mock()
    mock_ytdl_instance.download.side_effect = Exception("Error")
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
    
    result = downloader._try_fallback_download('https://www.youtube.com/watch?v=test', False, None)
    assert result is False


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_try_fallback_download_media_mp3(mock_ytdl, downloader):
    """Test _try_fallback_download_media for MP3."""
    mock_ytdl_instance = Mock()
    mock_ytdl_instance.download.return_value = None
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
    
    result = downloader._try_fallback_download_media('https://www.youtube.com/watch?v=test', 'mp3', '720', '320', None)
    assert result is True


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_try_fallback_download_media_mp4(mock_ytdl, downloader):
    """Test _try_fallback_download_media for MP4."""
    mock_ytdl_instance = Mock()
    mock_ytdl_instance.download.return_value = None
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
    
    result = downloader._try_fallback_download_media('https://www.youtube.com/watch?v=test', 'mp4', '720', 'best', None)
    assert result is True


@patch('src.youtube_downloader.yt_dlp.YoutubeDL')
def test_try_fallback_download_media_failure(mock_ytdl, downloader):
    """Test _try_fallback_download_media failure."""
    mock_ytdl_instance = Mock()
    mock_ytdl_instance.download.side_effect = Exception("Error")
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
    
    result = downloader._try_fallback_download_media('https://www.youtube.com/watch?v=test', 'mp3', '720', '320', None)
    assert result is False


# Path Validation Tests
def test_validate_path_success(downloader):
    """Test _validate_path success."""
    temp_dir = Path(tempfile.mkdtemp())
    is_valid, result = downloader._validate_path(str(temp_dir))
    assert is_valid is True


@patch('os.access')
def test_validate_path_no_write_permission(mock_access, downloader):
    """Test _validate_path with no write permission."""
    mock_access.return_value = False
    temp_dir = Path(tempfile.mkdtemp())
    is_valid, error = downloader._validate_path(str(temp_dir))
    assert is_valid is False
    assert "No write permission" in error


def test_validate_path_exception(downloader):
    """Test _validate_path with exception."""
    with patch('pathlib.Path.resolve', side_effect=Exception("Error")):
        is_valid, error = downloader._validate_path("/some/path")
        assert is_valid is False
        assert "Invalid path: Error" in error


# File Copying Tests
def test_copy_specific_files_success(downloader, temp_downloads_dir):
    """Test _copy_specific_files success."""
    test_file = temp_downloads_dir / "test.mp4"
    test_file.write_text("content")
    
    dest_dir = Path(tempfile.mkdtemp())
    downloader._copy_specific_files(str(dest_dir), ["test.mp4"])
    
    assert (dest_dir / "test.mp4").exists()


def test_copy_specific_files_no_dest(downloader):
    """Test _copy_specific_files with no destination."""
    downloader._copy_specific_files("", ["test.mp4"])


def test_copy_specific_files_no_files(downloader):
    """Test _copy_specific_files with no files."""
    downloader._copy_specific_files("/some/path", [])


def test_copy_specific_files_invalid_path(downloader):
    """Test _copy_specific_files with invalid path."""
    with patch.object(downloader, '_validate_path', return_value=(False, "Invalid")):
        downloader._copy_specific_files("invalid", ["test.mp4"])


def test_copy_specific_files_source_not_found(downloader, temp_downloads_dir):
    """Test _copy_specific_files with missing source file."""
    dest_dir = Path(tempfile.mkdtemp())
    downloader._copy_specific_files(str(dest_dir), ["missing.mp4"])


def test_copy_specific_files_copy_error(downloader, temp_downloads_dir):
    """Test _copy_specific_files with copy error."""
    test_file = temp_downloads_dir / "test.mp4"
    test_file.write_text("content")
    
    dest_dir = Path(tempfile.mkdtemp())
    with patch('shutil.copy2', side_effect=Exception("Copy error")):
        downloader._copy_specific_files(str(dest_dir), ["test.mp4"])