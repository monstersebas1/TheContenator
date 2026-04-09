"""YouTube Scraper — uses YouTube Data API / yt-dlp for channels, shorts, and stats."""

from platforms.base import BaseScraper


class YouTubeScraper(BaseScraper):
    """YouTube platform scraper."""

    @property
    def platform_name(self) -> str:
        return "youtube"

    def search_creators(self, keyword: str, limit: int = 20) -> list[dict]:
        raise NotImplementedError("YouTube search_creators not yet built")

    def get_account_videos(self, username: str, limit: int = 50) -> list[dict]:
        raise NotImplementedError("YouTube get_account_videos not yet built")

    def get_video_details(self, video_url: str) -> dict:
        raise NotImplementedError("YouTube get_video_details not yet built")

    def get_trending(self, category: str = None, limit: int = 50) -> list[dict]:
        raise NotImplementedError("YouTube get_trending not yet built")
