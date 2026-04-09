"""Data models — typed representations of accounts, videos, stats, transcripts."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Account:
    username: str
    platform: str
    display_name: str = ""
    bio: str = ""
    followers: int = 0
    following: int = 0
    total_videos: int = 0
    avg_views: int = 0
    engagement_rate: float = 0.0
    profile_url: str = ""
    scraped_at: str = ""


@dataclass
class Video:
    video_id: str
    platform: str
    url: str
    title: str = ""
    description: str = ""
    creator_username: str = ""
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    duration: float = 0.0
    posted_date: str = ""
    thumbnail_url: str = ""
    hashtags: list[str] = field(default_factory=list)
    engagement_rate: float = 0.0
    local_path: str = ""
    scraped_at: str = ""


@dataclass
class Transcript:
    video_id: str
    language: str = "en"
    full_text: str = ""
    segments: list[dict] = field(default_factory=list)
    duration: float = 0.0
    file_path: str = ""
    created_at: str = ""
