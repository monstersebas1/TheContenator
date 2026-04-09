"""Database — SQLite connection, table creation, and basic CRUD."""

import os
import sqlite3

from core.constants import DB_NAME
from core.utils import DATA_DIR


DB_PATH = os.path.join(DATA_DIR, DB_NAME)


def get_connection() -> sqlite3.Connection:
    """Get a SQLite connection with row factory."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            platform TEXT NOT NULL,
            display_name TEXT DEFAULT '',
            bio TEXT DEFAULT '',
            followers INTEGER DEFAULT 0,
            following INTEGER DEFAULT 0,
            total_videos INTEGER DEFAULT 0,
            avg_views INTEGER DEFAULT 0,
            engagement_rate REAL DEFAULT 0.0,
            profile_url TEXT DEFAULT '',
            scraped_at TEXT DEFAULT '',
            UNIQUE(username, platform)
        );

        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            url TEXT NOT NULL,
            title TEXT DEFAULT '',
            description TEXT DEFAULT '',
            creator_username TEXT DEFAULT '',
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            saves INTEGER DEFAULT 0,
            duration REAL DEFAULT 0.0,
            posted_date TEXT DEFAULT '',
            thumbnail_url TEXT DEFAULT '',
            hashtags TEXT DEFAULT '[]',
            engagement_rate REAL DEFAULT 0.0,
            local_path TEXT DEFAULT '',
            scraped_at TEXT DEFAULT '',
            UNIQUE(video_id, platform)
        );

        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            language TEXT DEFAULT 'en',
            full_text TEXT DEFAULT '',
            segments TEXT DEFAULT '[]',
            duration REAL DEFAULT 0.0,
            file_path TEXT DEFAULT '',
            created_at TEXT DEFAULT '',
            UNIQUE(video_id)
        );
    """)
    conn.commit()
    conn.close()
