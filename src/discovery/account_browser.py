"""Account Browser — list and sort videos from any creator account."""

from core.constants import SORT_OPTIONS
from core.utils import log
from platforms.tiktok.scraper import TikTokScraper
from platforms.youtube.scraper import YouTubeScraper
from platforms.instagram.scraper import InstagramScraper

SCRAPERS = {
    "tiktok": TikTokScraper,
    "youtube": YouTubeScraper,
    "instagram": InstagramScraper,
}

SORT_KEYS = {
    "most_views": ("views", True),
    "most_comments": ("comments", True),
    "most_likes": ("likes", True),
    "most_shares": ("shares", True),
    "highest_engagement": ("engagement_rate", True),
    "newest": ("posted_date", True),
    "oldest": ("posted_date", False),
    "trending": ("engagement_rate", True),
}


def browse_account(username: str, platform: str = "tiktok", sort_by: str = "most_views", limit: int = 50) -> list[dict]:
    """
    Fetch all videos from an account and sort them.

    Args:
        username: Creator's username/handle
        platform: Platform to query
        sort_by: Sort order (most_views, most_comments, most_likes, most_shares,
                 highest_engagement, newest, oldest, trending)
        limit: Max videos to fetch

    Returns:
        Sorted list of video dicts
    """
    if platform not in SCRAPERS:
        raise ValueError(f"Unsupported platform: {platform}. Use: {list(SCRAPERS.keys())}")

    if sort_by not in SORT_KEYS:
        raise ValueError(f"Unsupported sort: {sort_by}. Use: {list(SORT_KEYS.keys())}")

    scraper = SCRAPERS[platform]()
    videos = scraper.get_account_videos(username, limit=limit)

    sort_field, reverse = SORT_KEYS[sort_by]
    videos.sort(key=lambda x: x.get(sort_field, 0), reverse=reverse)

    log(f"Found {len(videos)} videos for @{username}, sorted by {sort_by}")
    return videos
