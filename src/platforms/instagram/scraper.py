"""Instagram Scraper — uses Instaloader for profiles, reels, and stats."""

import instaloader

from core.config import config_get
from core.utils import log, engagement_rate, timestamp
from platforms.base import BaseScraper


class InstagramScraper(BaseScraper):
    """Instagram platform scraper using Instaloader."""

    def __init__(self):
        self._loader = instaloader.Instaloader(
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            quiet=True,
        )
        self._logged_in = False

    def _login(self):
        """Login if credentials are configured and not already logged in."""
        if self._logged_in:
            return
        ig_config = config_get("instagram", {}) or {}
        username = ig_config.get("username", "")
        password = ig_config.get("password", "")
        if username and password:
            try:
                self._loader.login(username, password)
                self._logged_in = True
                log("Instagram login successful")
            except Exception as e:
                log(f"Instagram login failed: {e} — continuing without auth")

    @property
    def platform_name(self) -> str:
        return "instagram"

    def _profile_to_dict(self, profile: instaloader.Profile) -> dict:
        """Convert an Instaloader Profile to our standard dict format."""
        return {
            "username": profile.username,
            "display_name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "total_videos": profile.mediacount,
            "profile_url": f"https://www.instagram.com/{profile.username}/",
            "profile_pic_url": profile.profile_pic_url,
            "is_verified": profile.is_verified,
            "is_private": profile.is_private,
            "platform": "instagram",
            "scraped_at": timestamp(),
        }

    def search_creators(self, keyword: str, limit: int = 20) -> list[dict]:
        """
        Search Instagram profiles by keyword.
        Note: Instaloader's search requires login.
        """
        log(f"Searching Instagram creators for: {keyword}")
        self._login()

        results = []
        try:
            profiles = instaloader.TopSearchResults(self._loader.context, keyword)
            for profile in profiles.get_profiles():
                results.append(self._profile_to_dict(profile))
                if len(results) >= limit:
                    break
        except Exception as e:
            log(f"Instagram search failed: {e}")

        return results

    def get_account_videos(self, username: str, limit: int = 50) -> list[dict]:
        """Get posts/reels from an Instagram account."""
        log(f"Fetching posts for Instagram user: @{username}")
        self._login()

        profile = instaloader.Profile.from_username(self._loader.context, username)
        results = []

        for post in profile.get_posts():
            if len(results) >= limit:
                break

            views = post.video_view_count if post.is_video else 0
            likes = post.likes
            comments = post.comments

            results.append({
                "video_id": post.shortcode,
                "title": (post.caption or "")[:100],
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "views": views or 0,
                "likes": likes,
                "comments": comments,
                "shares": 0,
                "engagement_rate": engagement_rate(likes, comments, 0, views) if views else 0.0,
                "duration": (post.video_duration or 0) if post.is_video else 0,
                "posted_date": post.date_utc.isoformat() if post.date_utc else "",
                "thumbnail_url": post.url,
                "hashtags": list(post.caption_hashtags) if post.caption_hashtags else [],
                "is_video": post.is_video,
                "creator_username": username,
                "platform": "instagram",
                "scraped_at": timestamp(),
            })

        return results

    def get_video_details(self, video_url: str) -> dict:
        """Get full details for a single Instagram post/reel."""
        log(f"Getting Instagram post details: {video_url}")
        self._login()

        shortcode = video_url.rstrip("/").split("/")[-1]
        post = instaloader.Post.from_shortcode(self._loader.context, shortcode)

        views = post.video_view_count if post.is_video else 0
        likes = post.likes
        comments = post.comments

        return {
            "video_id": post.shortcode,
            "title": (post.caption or "")[:100],
            "description": post.caption or "",
            "url": video_url,
            "views": views or 0,
            "likes": likes,
            "comments": comments,
            "shares": 0,
            "saves": 0,
            "engagement_rate": engagement_rate(likes, comments, 0, views) if views else 0.0,
            "duration": (post.video_duration or 0) if post.is_video else 0,
            "posted_date": post.date_utc.isoformat() if post.date_utc else "",
            "creator_username": post.owner_username,
            "thumbnail_url": post.url,
            "hashtags": list(post.caption_hashtags) if post.caption_hashtags else [],
            "is_video": post.is_video,
            "video_url": post.video_url if post.is_video else None,
            "platform": "instagram",
            "scraped_at": timestamp(),
        }

    def get_trending(self, category: str = None, limit: int = 50) -> list[dict]:
        """
        Instagram doesn't expose a public trending API.
        Use search_creators + get_account_videos as an alternative.
        """
        log("Instagram trending not available — use search_creators + get_account_videos instead")
        return []
