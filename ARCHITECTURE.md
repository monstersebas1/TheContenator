# TheContenator — Architecture Map

```
TheContenator/
├── ARCHITECTURE.md                 # <-- you are here
├── CLAUDE.md                       # Claude Code project instructions
├── README.md                       # Project overview
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
│
├── config/
│   └── config.example.json         # Template config — copy to config.json
├── config.json                     # Runtime config (gitignored)
│
├── src/
│   ├── __init__.py
│   ├── main.py                     # CLI menu — single entry point
│   │
│   ├── core/                       # SHARED — do NOT edit during parallel work
│   │   ├── __init__.py
│   │   ├── config.py               # Config reader (loads config.json)
│   │   ├── constants.py            # App-wide constants, menu strings
│   │   └── utils.py                # Shared helpers (logging, formatting)
│   │
│   ├── discovery/                  # TERMINAL 1 — Niche & Account Search
│   │   ├── __init__.py
│   │   ├── niche_search.py         # Search a niche -> ranked list of top accounts
│   │   ├── account_browser.py      # Browse account videos, sort by metrics
│   │   └── trending.py             # Trending content discovery by platform
│   │
│   ├── analyzer/                   # TERMINAL 2 — Video Intelligence
│   │   ├── __init__.py
│   │   ├── video_stats.py          # Full stats: views, likes, comments, shares, engagement %
│   │   ├── transcript.py           # Faster-Whisper transcription -> readable script
│   │   └── comparator.py           # Side-by-side account/video comparison
│   │
│   ├── video/                      # TERMINAL 3 — Download & Processing
│   │   ├── __init__.py
│   │   ├── downloader.py           # yt-dlp multi-platform video download
│   │   ├── metadata.py             # Extract/read video metadata
│   │   └── processor.py            # Trim, overlay text, re-encode
│   │
│   ├── platforms/                   # TERMINAL 4 — Platform Connectors
│   │   ├── __init__.py
│   │   ├── base.py                 # Abstract base class for all platform scrapers
│   │   ├── tiktok/
│   │   │   ├── __init__.py
│   │   │   └── scraper.py          # TikTok-Api wrapper — accounts, videos, stats
│   │   ├── youtube/
│   │   │   ├── __init__.py
│   │   │   └── scraper.py          # YouTube Data API — channels, shorts, stats
│   │   └── instagram/
│   │       ├── __init__.py
│   │       └── scraper.py          # Instaloader wrapper — profiles, reels, stats
│   │
│   └── storage/                    # TERMINAL 5 — Data Layer
│       ├── __init__.py
│       ├── db.py                   # SQLite connection + migrations
│       └── models.py               # Data models: Account, Video, Stats, Transcript
│
├── data/                           # Runtime data (gitignored)
│   ├── downloads/                  # Downloaded video files
│   ├── transcripts/                # Extracted scripts (.txt)
│   └── contenator.db               # SQLite database
│
└── tests/
    ├── __init__.py
    ├── test_discovery/
    │   └── __init__.py
    ├── test_analyzer/
    │   └── __init__.py
    ├── test_video/
    │   └── __init__.py
    ├── test_platforms/
    │   └── __init__.py
    └── test_storage/
        └── __init__.py
```

## Parallel Terminal Strategy

| Terminal | Module             | Owner     | Can Work Alone? | Imports From          |
|----------|--------------------|-----------|-----------------|-----------------------|
| T1       | `discovery/`       | —         | Yes             | `platforms/`, `storage/` |
| T2       | `analyzer/`        | —         | Yes             | `storage/`, `video/`  |
| T3       | `video/`           | —         | Yes             | `core/`               |
| T4       | `platforms/*/`     | —         | Yes             | `core/`               |
| T5       | `storage/`         | —         | Yes             | `core/`               |

## Rules for Parallel Work

1. **`core/` is frozen** — nobody edits it during parallel sessions
2. **Each platform scraper is its own file** — TikTok / YouTube / IG never conflict
3. **`storage/` is the single source of truth** — all modules read/write through it
4. **`data/` is gitignored** — no merge conflicts on downloaded content
5. **New modules only import from `core/` and `storage/`** — never cross-import between feature modules

## Module Responsibilities

### discovery/ — "What's hot?"
- Search a niche keyword -> returns top creators ranked by engagement
- Browse any account's videos with sorting (views, comments, date, engagement rate, trending)
- Surface trending content across platforms

### analyzer/ — "How good is it?"
- Full stats breakdown for any video (views, likes, comments, shares, engagement %)
- Transcribe video audio to a readable script via Faster-Whisper
- Compare accounts or videos side-by-side

### video/ — "Get the content"
- Download videos from any supported platform via yt-dlp
- Extract and read video metadata
- Basic processing: trim, add text overlays, re-encode

### platforms/ — "Talk to the APIs"
- Each platform gets its own scraper behind a common interface
- Scrapers handle authentication, rate limiting, pagination
- Returns normalized data that storage/ can persist

### storage/ — "Remember everything"
- SQLite database for accounts, videos, stats, transcripts
- Clean data models with typed fields
- Single point of truth — no module stores its own state
