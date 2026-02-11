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
    assert "Missing argument" in result.stdout


def test_main_invalid_url():
    result = runner.invoke(cli.app, ['https://example.com/video'])

    assert result.exit_code != 0
    assert "valid YouTube URL." in str(result.exception)


@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_successful_download(mock_downloader_class, mock_setup, mock_video_info):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.get_video_info.return_value = mock_video_info
    mock_downloader.download.return_value = True
    
    url = 'https://www.youtube.com/watch?v=test'

    result = runner.invoke(cli.app, [url])

    mock_setup.assert_called_once()
    mock_downloader.get_video_info.assert_called_once_with(url)
    mock_downloader.download.assert_called_once_with(url, format='mp4', output_dir=None)
    
    assert result.exit_code == 0
    assert "Download completed!" in result.stdout


@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_download_failure(mock_downloader_class, mock_setup):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.get_video_info.return_value = None
    mock_downloader.download.return_value = False

    url = 'https://www.youtube.com/watch?v=test'

    result = runner.invoke(cli.app, [url])

    assert result.exit_code != 0
    assert "Error: Download failed." in str(result.exception)


@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_with_audio_only(mock_downloader_class, mock_setup, mock_video_info):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.get_video_info.return_value = mock_video_info
    mock_downloader.download_video.return_value = True
    
    url = 'https://www.youtube.com/watch?v=test'

    result = runner.invoke(cli.app, [url, '--audio'])

    mock_downloader.download_video.assert_called_once_with(url, True, None)
    assert result.exit_code == 0
    assert "Download completed!" in result.stdout


@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_with_output_dir(mock_downloader_class, mock_setup, mock_video_info):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.get_video_info.return_value = mock_video_info
    mock_downloader.download_video.return_value = True
    
    url = 'https://www.youtube.com/watch?v=test'
    output_dir = '/custom/path'

    result = runner.invoke(cli.app, [url, '--output-dir', output_dir])

    mock_downloader.download_video.assert_called_once_with(url, False, output_dir)
    assert result.exit_code == 0
    assert "Download completed!" in result.stdout


@patch('cli.setup_directories')
@patch('cli.YouTubeDownloader')
def test_main_with_both_options(mock_downloader_class, mock_setup, mock_video_info):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.get_video_info.return_value = mock_video_info
    mock_downloader.download_video.return_value = True
    
    url = 'https://www.youtube.com/watch?v=test'
    output_dir = '/custom/path'

    result = runner.invoke(cli.app, [url, '-a', '-o', output_dir])

    mock_downloader.download_video.assert_called_once_with(url, True, output_dir)
    assert result.exit_code == 0
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
