"""Base Platform Scraper — abstract interface all platform scrapers must implement."""

from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """Abstract base class for platform scrapers."""

    @abstractmethod
    def search_creators(self, keyword: str, limit: int = 20) -> list[dict]:
        """
        Search for creators/accounts by niche keyword.

        Returns:
            List of dicts with: username, display_name, followers, profile_url,
            bio, avg_views, engagement_rate
        """

    @abstractmethod
    def get_account_videos(self, username: str, limit: int = 50) -> list[dict]:
        """
        Get all videos from a creator account.

        Returns:
            List of dicts with: video_id, title, url, views, likes, comments,
            shares, posted_date, duration, thumbnail_url, hashtags
        """

    @abstractmethod
    def get_video_details(self, video_url: str) -> dict:
        """
        Get full details for a single video.

        Returns:
            Dict with all available stats and metadata.
        """

    @abstractmethod
    def get_trending(self, category: str = None, limit: int = 50) -> list[dict]:
        """
        Get trending videos on this platform.

        Returns:
            List of video dicts with stats and creator info.
        """

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return the platform name (e.g. 'tiktok', 'youtube', 'instagram')."""
