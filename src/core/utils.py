"""Shared utility functions."""

import os
from datetime import datetime

from core.constants import APP_NAME

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
)


def ensure_data_dirs():
    """Create data directories if they don't exist."""
    for subdir in ["downloads", "transcripts"]:
        os.makedirs(os.path.join(DATA_DIR, subdir), exist_ok=True)


def format_number(n: int) -> str:
    """Format large numbers for display: 1234567 -> 1.2M"""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def engagement_rate(likes: int, comments: int, shares: int, views: int) -> float:
    """Calculate engagement rate as a percentage."""
    if views == 0:
        return 0.0
    return ((likes + comments + shares) / views) * 100


def timestamp() -> str:
    """Return current ISO timestamp."""
    return datetime.now().isoformat()


def log(message: str):
    """Simple console logger."""
    print(f"[{APP_NAME}] {message}")
