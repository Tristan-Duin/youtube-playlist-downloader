"""
Test different ways to use the application's CLI and ensure it functions within expected behavior.
"""
import pytest
from unittest.mock import patch, Mock
from typer.testing import CliRunner
import cli

runner = CliRunner()


def test_main_no_arguments():
    result = runner.invoke(cli.app, [])

    assert result.exit_code != 0
    assert "Missing argument" in result.stderr


def test_main_invalid_url():
    result = runner.invoke(cli.app, ['https://example.com/video'])

    assert result.exit_code != 0
    assert "valid YouTube URL." in str(result.exception)


@patch('cli.verify_ffmpeg')
@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_successful_download(mock_downloader_class, mock_setup, mock_ffmpeg, mock_video_info):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.is_playlist_url.return_value = False
    mock_downloader.get_video_info.return_value = mock_video_info
    mock_downloader.download.return_value = True
    
    url = 'https://www.youtube.com/watch?v=test'

    result = runner.invoke(cli.app, [url])

    mock_setup.assert_called_once()
    mock_downloader.is_playlist_url.assert_called_once_with(url)
    mock_downloader.get_video_info.assert_called_once_with(url)
    mock_downloader.download.assert_called_once_with(url, format='mp4', resolution=None, bitrate=None, output_dir=None)
    
    assert result.exit_code == 0
    assert "Download completed!" in result.stdout


@patch('cli.verify_ffmpeg')
@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_download_failure(mock_downloader_class, mock_setup, mock_ffmpeg):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.is_playlist_url.return_value = False
    mock_downloader.get_video_info.return_value = None
    mock_downloader.download.return_value = False

    url = 'https://www.youtube.com/watch?v=test'

    result = runner.invoke(cli.app, [url])

    assert result.exit_code != 0
    assert "Error: Download failed." in str(result.exception)


@patch('cli.verify_ffmpeg')
@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_with_audio_only(mock_downloader_class, mock_setup, mock_ffmpeg, mock_video_info):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.is_playlist_url.return_value = False
    mock_downloader.get_video_info.return_value = mock_video_info
    mock_downloader.download.return_value = True
    
    url = 'https://www.youtube.com/watch?v=test'

    result = runner.invoke(cli.app, [url, '--audio', 'true'])

    mock_downloader.download.assert_called_once_with(url, format='mp3', resolution=None, bitrate='true', output_dir=None)
    assert result.exit_code == 0
    assert "Download completed!" in result.stdout


@patch('cli.verify_ffmpeg')
@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_with_output_dir(mock_downloader_class, mock_setup, mock_ffmpeg, mock_video_info):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.is_playlist_url.return_value = False
    mock_downloader.get_video_info.return_value = mock_video_info
    mock_downloader.download.return_value = True
    
    url = 'https://www.youtube.com/watch?v=test'
    output_dir = '/custom/path'

    result = runner.invoke(cli.app, [url, '--output-dir', output_dir])

    mock_downloader.download.assert_called_once_with(url, format='mp4', resolution=None, bitrate=None, output_dir=output_dir)
    assert result.exit_code == 0
    assert "Download completed!" in result.stdout


@patch('cli.verify_ffmpeg')
@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_with_both_options(mock_downloader_class, mock_setup, mock_ffmpeg, mock_video_info):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.is_playlist_url.return_value = False
    mock_downloader.get_video_info.return_value = mock_video_info
    mock_downloader.download.return_value = True
    
    url = 'https://www.youtube.com/watch?v=test'
    output_dir = '/custom/path'

    result = runner.invoke(cli.app, [url, '-a', 'true', '-o', output_dir])

    mock_downloader.download.assert_called_once_with(url, format='mp3', resolution=None, bitrate='true', output_dir=output_dir)
    assert result.exit_code == 0
    assert "Download completed!" in result.stdout


@patch('cli.verify_ffmpeg')
@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_with_playlist_url(mock_downloader_class, mock_setup, mock_ffmpeg):
    """Test CLI with playlist URL."""
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.is_playlist_url.return_value = True
    mock_playlist_info = {
        'title': 'Test Playlist',
        'uploader': 'Test Channel',
        'video_count': 3
    }
    mock_downloader.get_playlist_info.return_value = mock_playlist_info
    mock_downloader.download.return_value = True
    
    url = 'https://www.youtube.com/playlist?list=PL123'

    result = runner.invoke(cli.app, [url])

    mock_setup.assert_called_once()
    mock_downloader.is_playlist_url.assert_called_once_with(url)
    mock_downloader.get_playlist_info.assert_called_once_with(url)
    mock_downloader.download.assert_called_once()
    
    assert result.exit_code == 0
    assert "Starting playlist download..." in result.stdout
    assert "Playlist: Test Playlist" in result.stdout
    assert "Videos in playlist: 3" in result.stdout
    assert "Download completed!" in result.stdout


def test_main_entry_point():
    """Test the if __name__ == '__main__' entry point."""
    with patch('cli.app') as mock_app:
        # Import and execute the module
        import importlib
        import sys
        
        # Temporarily modify sys.argv to avoid issues
        original_argv = sys.argv
        try:
            sys.argv = ['cli.py']
            # Execute the module's main block
            exec(open('cli.py').read())
        except SystemExit:
            pass  # Expected behavior when running CLI
        finally:
            sys.argv = original_argv
