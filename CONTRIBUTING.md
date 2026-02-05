# Contributing

## Prerequisites

- Python 3.9+
- Node.js (for yt-dlp)
- FFmpeg (optional for improved quality)
- Git

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/Tristan-Duin/youtube-playlist-downloader
   cd youtube-playlist-downloader
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

## Testing

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_cli.py
```

## Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation if needed

3. **Test your changes**
   ```bash
   python -m pytest
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "brief description of changes"
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Go to GitHub and create a PR
   - Describe your changes
   - Wait for review

## Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates

## Pull Request Guidelines

- Target the `main` branch
- Include a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed