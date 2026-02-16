# YouTube Downloader

YouTube videos, audio, and playlist downloading with both CLI and web interfaces

## Features

- Download individual videos or entire playlists
- Command-line interface for power users
- Web interface for easy use
- Docker support for easy deployment
- Built with modern Python packaging (pyproject.toml)

## Get Er' Runnin' Guide

### Docker (Recommended)

```bash
git clone https://github.com/Tristan-Duin/youtube-playlist-downloader
cd youtube-playlist-downloader
docker-compose up -d
```

Open http://localhost:5000 in your browser.

## Requirements Installation

```bash
git clone https://github.com/Tristan-Duin/youtube-playlist-downloader
cd youtube-playlist-downloader
pip install -e .
```

## Usage

### Web Interface

```bash
python gui.py
# Or
youtube-downloader-gui
```

### Command Line

```bash
python cli.py "https://www.youtube.com/watch?v=VIDEO_ID"
# Or
youtube-downloader "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Docker Commands

```bash
docker-compose up -d

docker-compose logs -f

docker-compose down
```


## Requirements

- Python 3.9+
- Node.js (for yt-dlp JavaScript execution)
- FFmpeg (optional, for video processing)


## Disclaimer & Legal Information

This project is provided for educational purposes only.  It demonstrates the use of tools and techniques related to downloading content from YouTube.  We strongly encourage responsible usage and a thorough understanding of copyright law and YouTube's Terms of Service (ToS).

Users are solely responsible for ensuring their downloads comply with all applicable laws, regulations, and YouTube’s ToS. Downloading copyrighted material without permission is illegal and violates YouTube’s policies. We do not endorse or encourage any activity that infringes on intellectual property rights.  Please respect the creators' rights and use this tool ethically.


## Contributing

Please read through [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License - see the [LICENSE](LICENSE) for more information.
