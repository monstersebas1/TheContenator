# platforms — per-platform scraper connectors

from platforms.base import BaseScraper


def get_scraper(platform: str) -> BaseScraper:
    """Factory — lazily import and return the scraper for a given platform."""
    if platform == "tiktok":
        from platforms.tiktok.scraper import TikTokScraper
        return TikTokScraper()
    elif platform == "youtube":
        from platforms.youtube.scraper import YouTubeScraper
        return YouTubeScraper()
    elif platform == "instagram":
        from platforms.instagram.scraper import InstagramScraper
        return InstagramScraper()
    else:
        raise ValueError(f"Unsupported platform: {platform}. Use: tiktok, youtube, instagram")
