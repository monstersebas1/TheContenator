"""Trending — discover trending content by platform and category."""

from core.utils import log
from platforms.tiktok.scraper import TikTokScraper
from platforms.youtube.scraper import YouTubeScraper
from platforms.instagram.scraper import InstagramScraper

SCRAPERS = {
    "tiktok": TikTokScraper,
    "youtube": YouTubeScraper,
    "instagram": InstagramScraper,
}


def get_trending(platform: str = "tiktok", category: str = None, limit: int = 50) -> list[dict]:
    """
    Get currently trending videos on a platform.

    Args:
        platform: Which platform ("tiktok", "youtube", "instagram")
        category: Optional category/niche filter
        limit: Max results

    Returns:
        List of video dicts with stats and creator info
    """
    if platform not in SCRAPERS:
        raise ValueError(f"Unsupported platform: {platform}. Use: {list(SCRAPERS.keys())}")

    scraper = SCRAPERS[platform]()
    return scraper.get_trending(category=category, limit=limit)
