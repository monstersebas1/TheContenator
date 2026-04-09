"""Instagram Scraper — uses Instaloader for profiles, reels, and stats."""

from platforms.base import BaseScraper


class InstagramScraper(BaseScraper):
    """Instagram platform scraper using Instaloader."""

    @property
    def platform_name(self) -> str:
        return "instagram"

    def search_creators(self, keyword: str, limit: int = 20) -> list[dict]:
        raise NotImplementedError("Instagram search_creators not yet built")

    def get_account_videos(self, username: str, limit: int = 50) -> list[dict]:
        raise NotImplementedError("Instagram get_account_videos not yet built")

    def get_video_details(self, video_url: str) -> dict:
        raise NotImplementedError("Instagram get_video_details not yet built")

    def get_trending(self, category: str = None, limit: int = 50) -> list[dict]:
        raise NotImplementedError("Instagram get_trending not yet built")
