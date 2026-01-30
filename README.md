# YouTube Downloader Project

## Team Members

Tristan Duin, Patrick Kahle, Mike Watts, Jacob Agbetor

## Tools Used By Team

- Communication: Discord
- Project Management: Monday.com Kanban Boards
- Code Repository: Github.com
- IDE(s): VSCode & Pycharm
- Language(s): Python

---

## Setup Options

### Option 1: Docker Setup (Recommended for usage)

The easiest way to run this project is with Docker. This approach handles all dependencies automatically and works consistently across all platforms.

**Prerequisites:**
- Docker Desktop (includes Docker Compose)
- Git

**Installation:**
1. Install Docker Desktop from https://docker.com/products/docker-desktop
2. Clone the repository:
   ```bash
   git clone https://github.com/Tristan-Duin/youtube-playlist-downloader
   cd youtube-playlist-downloader
   ```
3. Start the application:
   ```bash
   docker-compose up -d youtube-downloader-web
   ```
4. Open http://localhost:5000

That's it! Skip to the "Run The Downloader" section below.

### Option 2: Manual Python Setup (Recommended for development)

1) Install Python 3 (includes pip)

2) Install Node.js (required for yt-dlp JavaScript execution)

3) Install FFmpeg (recommended for video processing)

**Python Installation:**

Windows (recommended)

Download Python 3.x (64-bit) from python.org (Recommend 3.9 at a minimum)

Run the installer and check: "Add Python to PATH"

Click Install Now

macOS

Install Homebrew (if you don’t have it)

Install Python:

```bash
brew install python
```

Linux (Ubuntu/Debian)

```
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

**Node.js Installation:**

Windows

Download Node.js from nodejs.org (LTS version recommended)

Run the installer with default settings

macOS

```bash
brew install node
```

Linux (Ubuntu/Debian)

```bash
sudo apt install -y nodejs npm
```

**FFmpeg Installation:**

Windows

Download FFmpeg from ffmpeg.org/download.html

Extract to a folder (e.g., C:\ffmpeg)

Add C:\ffmpeg\bin to your PATH environment variable

OR powershell: `winget install --id=Gyan.FFmpeg -e

macOS

```bash
brew install ffmpeg
```

Linux (Ubuntu/Debian)

```bash
sudo apt install -y ffmpeg
```

4) Verify installation

Run these commands and make sure you see version output:

```
python --version
pip --version
node --version
npm --version
ffmpeg -version
```

If python doesn't work but python3 does, use python3/pip3 for the rest of the steps.

Note: Node.js helps yt-dlp handle YouTube's JavaScript-based protections, and FFmpeg is strongly recommended for video processing and format conversion.

5) Install Git (to download the project)

Windows: install Git for Windows
macOS:

```bash
brew install git
```

Linux (Ubuntu/Debian):

```bash
sudo apt install -y git
```

Verify:

```
git --version
```

6) Download the project

```
git clone https://github.com/Tristan-Duin/youtube-playlist-downloader
cd <REPO_FOLDER_HERE>
```

7) Create and activate a virtual environment (recommended)

Windows (PowerShell)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

8) Upgrade pip (recommended)
```bash
python -m pip install --upgrade pip
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run The Downloader

### Traditional Python Setup

```bash
python cli.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

For Web GUI:
```bash
python gui.py
```
Then visit http://localhost:5000

### Docker Setup (Recommended)

🐳 **The easiest way to run this project!** Docker handles all dependencies automatically and works the same on Windows, Mac, and Linux.

#### Prerequisites

1. **Install Docker Desktop**
   - **Windows/Mac**: Download from https://docker.com/products/docker-desktop
   - **Linux**: Install Docker Engine and Docker Compose
   
2. **Install Git** (if not already installed)
   - **Windows**: Download from https://git-scm.com/download/win
   - **Mac**: `brew install git` or download from git-scm.com
   - **Linux**: `sudo apt install git` (Ubuntu/Debian) or equivalent

#### Complete Setup Guide

**Step 1: Clone the Repository**
```bash
git clone https://github.com/Tristan-Duin/youtube-playlist-downloader
cd youtube-playlist-downloader
```

**Step 2: Start the Application**
```bash
docker-compose up -d
docker-compose ps
```

**Step 3: Access the Web Interface**
- Open your browser and go to: **http://localhost:5000**
- You should see the YouTube Downloader interface
- Downloaded videos will automatically appear in the `./downloads` folder

**Step 4: Test It Out**
- Paste any YouTube video URL into the interface
- Click "Download" and watch the progress
- Videos are saved to `./downloads` on your computer

#### Alternative Usage Methods

**Command Line Interface (CLI)**
```bash
# Download a video using CLI
docker-compose run --rm youtube-downloader-web python cli.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Download a playlist
docker-compose run --rm youtube-downloader-web python cli.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

**Interactive Shell Access**
```bash
docker-compose run --rm youtube-downloader-web bash
```

#### Container Management

**View Application Status**
```bash
docker-compose ps
docker-compose logs -f
docker-compose logs youtube-downloader-web
```

**Stop and Start**
```bash
docker-compose down
docker-compose up -d

docker-compose restart
```

**Updates and Rebuilding**
```bash
docker-compose build
docker-compose up -d --build

# Force rebuild without cache (if having issues)
docker-compose build --no-cache
```

#### Troubleshooting

**Port Already in Use**
```bash
docker ps | grep 5000
docker stop <container_id>
```

**Container Won't Start**
```bash
docker-compose logs youtube-downloader-web

docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Downloads Folder Permissions (Linux/Mac)**
```bash
sudo chown -R $USER:$USER ./downloads
```

**Complete Reset**
```bash
docker-compose down
docker system prune -a  # WARNING: removes all unused Docker data
docker-compose build
docker-compose up -d
```

---

## Testing

### PyTest commands unit tests and integration tests
```bash
python -m pytest .\tests\

python -m pytest .\tests\ -v
```

---

## Development Workflow

### Direct pushes to `main` are NOT allowed
All work **must** be done in branches and merged through **Pull Requests (PRs)**.

## Creating a Branch

### GitHub Desktop
1. Open the repository
2. Click **Current Branch → New Branch**
3. Name your branch (examples below)
4. Click **Create Branch**

### Git CLI
```bash
git checkout -b feature/your-feature-name
```

**Branch naming examples**
- `feature/download-logging`
- `bugfix/fix-playlist-error`
- `docs/readme-update`

---

## Committing Changes

### GitHub Desktop
1. Review changed files
2. Write a clear commit message
3. Click **Commit to branch-name**

### Git CLI
```bash
git status
git add .
git commit -m "Short clear description of change"
```

---

## Pushing Your Branch

### GitHub Desktop
- Click **Push origin**

### Git CLI
```bash
git push origin feature/your-feature-name
```

---

## Creating a Pull Request (PR)

### Using GitHub Website
1. Go to the repository on GitHub
2. You will see **Compare & pull request**
3. Click it
4. Add:
   - Clear title
   - Brief description of changes
5. Submit the PR

### Rules for PRs
- PR must target `main`
- PR should be reviewed before merging
- Fix requested changes if asked

---

## Merging
- Only approved PRs may be merged into `main`
- Do **not** merge your own PR unless explicitly allowed
- After merge, you may delete your branch

---

## Keeping Your Branch Up To Date

### GitHub Desktop
- Switch to `main`
- Click **Fetch / Pull**
- Switch back to your branch
- Click **Branch → Update from main**

### Git CLI
```bash
git checkout main
git pull origin main
git checkout feature/your-feature-name
git merge main
```