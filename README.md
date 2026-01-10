# YouTube Downloader Project

## Team Members

Tristan Duin, Patrick Kahle, Mike Watts, Jacob Agbetor

## Setup Tooling

1) Install Python 3 (includes pip)

Windows (recommended)

Download Python 3.x (64-bit) from python.org (Recommend 3.9 at a minimum)

Run the installer and check: “Add Python to PATH”

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

2) Verify installation

Run these commands and make sure you see version output (Python 3.x):

```
python --version
pip --version
```

If python doesn’t work but python3 does, use python3/pip3 for the rest of the steps.

3) Install Git (to download the project)

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

4) Download the project

```
git clone https://github.com/Tristan-Duin/youtube-playlist-downloader
cd <REPO_FOLDER_HERE>
```

5) Create and activate a virtual environment (recommended)

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

6) Upgrade pip (recommended)
python -m pip install --upgrade pip

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run The Downloader

```bash
python downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Tools Used By Team

Communication: Discord
Project Management: Monday.com Kanban Boards
Code Repository: Github.com
IDE(s): VSCode & Pycharm
Language(s): Python
