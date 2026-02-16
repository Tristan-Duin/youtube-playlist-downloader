"""
Simplified tests for playlist functionality in YouTubeDownloader.
"""
import pytest
from unittest.mock import patch, Mock
from src.youtube_downloader import YouTubeDownloader


@pytest.fixture
def downloader(temp_downloads_dir):
    with patch('src.youtube_downloader.DOWNLOADS_DIR', temp_downloads_dir):
        return YouTubeDownloader()


class TestPlaylistDetection:
    """Test playlist URL detection."""
    
    def test_playlist_urls_detected(self, downloader):
        """Test that various playlist URL formats are detected correctly."""
        playlist_urls = [
            'https://www.youtube.com/watch?v=video123&list=playlist456',
            'https://www.youtube.com/playlist?list=PLtest123',
            'https://youtu.be/video123?list=playlist456',
            'https://www.YouTube.com/watch?v=video123&LIST=playlist456',  # case insensitive
        ]
        
        for url in playlist_urls:
            assert downloader.is_playlist_url(url)
    
    def test_single_video_urls_not_detected(self, downloader):
        """Test that single video URLs are not detected as playlists."""
        single_video_urls = [
            'https://www.youtube.com/watch?v=video123',
            'https://youtu.be/video123',
            'https://www.youtube.com/watch?v=video123&t=30s',
        ]
        
        for url in single_video_urls:
            assert not downloader.is_playlist_url(url)


class TestPlaylistInfo:
    """Test playlist information extraction."""
    
    @patch('src.youtube_downloader.yt_dlp.YoutubeDL')
    def test_get_playlist_info_success(self, mock_ytdl_class, downloader):
        """Test successful playlist info extraction."""
        mock_data = {
            'title': 'Test Playlist',
            'uploader': 'Test Channel',
            'id': 'PLtest123',
            'webpage_url': 'https://www.youtube.com/playlist?list=PLtest123',
            'entries': [{'title': 'Video 1'}, {'title': 'Video 2'}]
        }
        
        mock_ytdl = Mock()
        mock_ytdl.extract_info.return_value = mock_data
        mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
        
        result = downloader.get_playlist_info('https://www.youtube.com/playlist?list=PLtest123')
        
        assert result['title'] == 'Test Playlist'
        assert result['uploader'] == 'Test Channel'
        assert result['video_count'] == 2
    
    @patch('src.youtube_downloader.yt_dlp.YoutubeDL')
    def test_get_playlist_info_with_redirect(self, mock_ytdl_class, downloader):
        """Test playlist info extraction with URL redirect."""
        redirect_data = {'_type': 'url', 'url': 'https://www.youtube.com/playlist?list=PLtest123'}
        playlist_data = {
            'title': 'Test Playlist',
            'uploader': 'Test Channel', 
            'entries': [{'title': 'Video 1'}]
        }
        
        mock_ytdl = Mock()
        mock_ytdl.extract_info.side_effect = [redirect_data, playlist_data]
        mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
        
        result = downloader.get_playlist_info('https://www.youtube.com/watch?v=test&list=PLtest123')
        
        assert result['title'] == 'Test Playlist'
        assert mock_ytdl.extract_info.call_count == 2
    
    @patch('src.youtube_downloader.yt_dlp.YoutubeDL')
    def test_get_playlist_info_no_entries(self, mock_ytdl_class, downloader):
        """Test playlist info extraction returns None when no entries found."""
        mock_data = {'title': 'Empty Playlist', 'uploader': 'Test Channel'}
        
        mock_ytdl = Mock()
        mock_ytdl.extract_info.return_value = mock_data
        mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
        
        result = downloader.get_playlist_info('https://www.youtube.com/playlist?list=PLempty')
        
        assert result is None


class TestPlaylistDownload:
    """Test playlist download functionality."""
    
    @patch('src.youtube_downloader.yt_dlp.YoutubeDL')
    @patch.object(YouTubeDownloader, 'get_playlist_info')
    def test_download_playlist_success(self, mock_get_info, mock_ytdl_class, downloader):
        """Test successful playlist download."""
        mock_get_info.return_value = {'title': 'Test Playlist', 'video_count': 2}
        
        mock_ytdl = Mock()
        mock_ytdl.download.return_value = None
        mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
        
        result = downloader.download_playlist('https://www.youtube.com/playlist?list=PLtest123')
        
        assert result is True
        mock_ytdl.download.assert_called_once()
    
    @patch.object(YouTubeDownloader, 'get_playlist_info')
    def test_download_playlist_no_info(self, mock_get_info, downloader):
        """Test playlist download fails when no info available."""
        mock_get_info.return_value = None
        
        result = downloader.download_playlist('https://www.youtube.com/playlist?list=PLerror')
        
        assert result is False


class TestMainDownloadIntegration:
    """Test integration with main download method."""
    
    @patch.object(YouTubeDownloader, 'download_playlist')
    @patch.object(YouTubeDownloader, 'is_playlist_url')
    def test_main_download_delegates_to_playlist(self, mock_is_playlist, mock_download_playlist, downloader):
        """Test that main download method delegates to playlist download when appropriate."""
        mock_is_playlist.return_value = True
        mock_download_playlist.return_value = True
        
        result = downloader.download('https://www.youtube.com/playlist?list=PLtest123')
        
        assert result is True
        mock_download_playlist.assert_called_once()
    
    @patch('src.youtube_downloader.yt_dlp.YoutubeDL')
    @patch.object(YouTubeDownloader, 'is_playlist_url')
    def test_main_download_handles_single_video(self, mock_is_playlist, mock_ytdl_class, downloader):
        """Test that main download method handles single videos correctly."""
        mock_is_playlist.return_value = False
        
        mock_ytdl = Mock()
        mock_ytdl.download.return_value = None
        mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
        
        result = downloader.download('https://www.youtube.com/watch?v=single123')
        
        assert result is True
        mock_ytdl.download.assert_called_once()