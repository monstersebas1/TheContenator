"""TikTok Scraper — uses TikTok-Api to fetch accounts, videos, and stats."""

from platforms.base import BaseScraper


class TikTokScraper(BaseScraper):
    """TikTok platform scraper using the unofficial TikTok-Api."""

    @property
    def platform_name(self) -> str:
        return "tiktok"

    def search_creators(self, keyword: str, limit: int = 20) -> list[dict]:
        raise NotImplementedError("TikTok search_creators not yet built")

    def get_account_videos(self, username: str, limit: int = 50) -> list[dict]:
        raise NotImplementedError("TikTok get_account_videos not yet built")

    def get_video_details(self, video_url: str) -> dict:
        raise NotImplementedError("TikTok get_video_details not yet built")

    def get_trending(self, category: str = None, limit: int = 50) -> list[dict]:
        raise NotImplementedError("TikTok get_trending not yet built")
