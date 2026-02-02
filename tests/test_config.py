"""
Testing basic configuration defaults work and directories are successfully created if needed.
"""
import pytest
from pathlib import Path
from unittest.mock import patch

from src.config import setup_directories, DOWNLOADS_DIR, DEFAULT_FORMAT


def test_constants():
    assert isinstance(DOWNLOADS_DIR, Path)
    assert str(DOWNLOADS_DIR) == "downloads"
    assert DEFAULT_FORMAT == "mp4"


def test_setup_directories_creates_dir(temp_downloads_dir):
    test_dir = temp_downloads_dir / 'test_downloads'
    with patch('src.config.DOWNLOADS_DIR', test_dir):
        assert not test_dir.exists()
        
        setup_directories()
        
        assert test_dir.exists()
        assert test_dir.is_dir()


def test_setup_directories_existing_dir(temp_downloads_dir):
    test_dir = temp_downloads_dir / 'existing_downloads'
    test_dir.mkdir()
    
    with patch('src.config.DOWNLOADS_DIR', test_dir):
        setup_directories()
        assert test_dir.exists()
