# CLAUDE.md

## Project Overview

**TheContenator** is a Python 3.12 CLI tool for creator research and content intelligence. It helps users discover top creators in any niche, analyze video performance, extract scripts via transcription, and download content — across TikTok, YouTube, and Instagram.

There is no web UI yet. The app runs via `python src/main.py` from the project root.

## Running the Application

```bash
# First-time setup
python -m venv venv && source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
cp config/config.example.json config.json  # then fill in values

# Run
python src/main.py
```

The app must be run from the project root. `src/main.py` adds `src/` to `sys.path`, so all imports use bare module names (e.g., `from core.config import load_config`).

## Architecture

See `ARCHITECTURE.md` for the full visual map and module responsibilities.

### Key Modules
- **`src/discovery/`** — niche search, account browsing, trending content
- **`src/analyzer/`** — video stats, Faster-Whisper transcription, comparisons
- **`src/video/`** — yt-dlp downloading, metadata extraction, processing
- **`src/platforms/`** — per-platform scrapers (TikTok, YouTube, Instagram) behind a common interface
- **`src/storage/`** — SQLite database, data models (Account, Video, Transcript)
- **`src/core/`** — shared config reader, constants, utilities

### Data Storage
- SQLite database at `data/contenator.db`
- Downloaded videos in `data/downloads/`
- Transcripts in `data/transcripts/`
- All runtime data is gitignored.

### Platform Scrapers
Each platform has its own scraper class in `src/platforms/<platform>/scraper.py`, all implementing `BaseScraper` from `src/platforms/base.py`. This means:
- Each scraper can be developed independently
- All scrapers return the same data shape
- Adding a new platform = one new file

## Configuration

Config lives in `config.json` at the project root. See `config/config.example.json` for the template.

## Parallel Development

This project is structured for parallel terminal work. See `ARCHITECTURE.md` for the terminal assignment map. Rule: **never edit `src/core/` during parallel sessions**.

## Dependencies

- **yt-dlp** — multi-platform video downloading
- **TikTokApi** — TikTok scraping (unofficial API)
- **instaloader** — Instagram scraping
- **faster-whisper** — speech-to-text transcription
- **sqlite3** — built-in, no install needed

## Contributing

One module per terminal. One feature per PR. Don't cross-import between feature modules — only import from `core/` and `storage/`.
