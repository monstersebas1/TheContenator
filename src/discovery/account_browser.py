"""Account Browser — list and sort videos from any creator account."""

from core.constants import SORT_OPTIONS
from core.utils import log
from platforms import get_scraper

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
    if sort_by not in SORT_KEYS:
        raise ValueError(f"Unsupported sort: {sort_by}. Use: {list(SORT_KEYS.keys())}")

    scraper = get_scraper(platform)
    videos = scraper.get_account_videos(username, limit=limit)

    sort_field, reverse = SORT_KEYS[sort_by]
    # Use str default for date fields, numeric default for everything else
    date_fields = ("posted_date",)
    if sort_field in date_fields:
        videos.sort(key=lambda x: str(x.get(sort_field, "") or ""), reverse=reverse)
    else:
        videos.sort(key=lambda x: float(x.get(sort_field, 0) or 0), reverse=reverse)

    log(f"Found {len(videos)} videos for @{username}, sorted by {sort_by}")
    return videos
