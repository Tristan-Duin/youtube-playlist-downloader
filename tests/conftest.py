"""
Configuration provided to support, simplify, and standardize across our tests.
"""
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_downloads_dir():
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_video_info():
    return {
        'title': 'Test Video Title',
        'uploader': 'Test Uploader', 
        'duration': 180
    }
