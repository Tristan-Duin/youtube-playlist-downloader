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