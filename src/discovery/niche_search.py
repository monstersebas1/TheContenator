"""Niche Search — find top creators in any niche across platforms."""

from core.utils import log
from platforms.tiktok.scraper import TikTokScraper
from platforms.youtube.scraper import YouTubeScraper
from platforms.instagram.scraper import InstagramScraper

SCRAPERS = {
    "tiktok": TikTokScraper,
    "youtube": YouTubeScraper,
    "instagram": InstagramScraper,
}


def search_niche(keyword: str, platform: str = "tiktok", limit: int = 20) -> list[dict]:
    """
    Search a niche keyword and return top accounts ranked by engagement.

    Args:
        keyword: Niche to search (e.g. "fitness", "cooking", "gaming")
        platform: Which platform to search ("tiktok", "youtube", "instagram")
        limit: Max number of accounts to return

    Returns:
        List of account dicts sorted by followers (descending)
    """
    if platform not in SCRAPERS:
        raise ValueError(f"Unsupported platform: {platform}. Use: {list(SCRAPERS.keys())}")

    scraper = SCRAPERS[platform]()
    results = scraper.search_creators(keyword, limit=limit)

    # Sort by followers descending
    results.sort(key=lambda x: x.get("followers", 0), reverse=True)

    return results


def search_all_platforms(keyword: str, limit_per_platform: int = 10) -> dict[str, list[dict]]:
    """
    Search across all platforms simultaneously.

    Returns:
        Dict with platform name as key, list of accounts as value
    """
    log(f"Searching all platforms for: {keyword}")
    results = {}
    for platform_name, scraper_class in SCRAPERS.items():
        try:
            scraper = scraper_class()
            results[platform_name] = scraper.search_creators(keyword, limit=limit_per_platform)
        except Exception as e:
            log(f"Failed to search {platform_name}: {e}")
            results[platform_name] = []
    return results
