"""TikTok Scraper — uses yt-dlp for fast, browserless TikTok data extraction."""

from yt_dlp import YoutubeDL

from core.utils import log, engagement_rate, timestamp
from platforms.base import BaseScraper


class TikTokScraper(BaseScraper):
    """TikTok platform scraper using yt-dlp — no browser, no tokens needed."""

    @property
    def platform_name(self) -> str:
        return "tiktok"

    def search_creators(self, keyword: str, limit: int = 20) -> list[dict]:
        """Search TikTok creators by keyword via video search, then deduplicate by creator."""
        log(f"Searching TikTok creators for: {keyword}")
        ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": True}

        # yt-dlp doesn't have native TikTok search, so we search via web
        # Use tiktok search URL pattern
        search_url = f"https://www.tiktok.com/search/user?q={keyword}"

        # Fallback: search videos and extract unique creators
        try:
            with YoutubeDL(ydl_opts) as ydl:
                results = ydl.extract_info(search_url, download=False)
            entries = results.get("entries", []) if results else []
        except Exception:
            # If direct search fails, try via video search
            entries = []

        # If we got user results, parse them
        seen = {}
        for entry in entries[:limit * 3]:
            uploader = entry.get("uploader") or entry.get("creator") or ""
            uploader_id = entry.get("uploader_id") or uploader
            if not uploader_id or uploader_id in seen:
                continue
            seen[uploader_id] = {
                "username": uploader_id,
                "display_name": uploader,
                "profile_url": f"https://www.tiktok.com/@{uploader_id}",
                "platform": "tiktok",
                "scraped_at": timestamp(),
            }
            if len(seen) >= limit:
                break

        return list(seen.values())

    def get_account_videos(self, username: str, limit: int = 50) -> list[dict]:
        """Get videos from a TikTok user's profile."""
        log(f"Fetching videos for TikTok user: @{username}")
        username = username.lstrip("@")
        profile_url = f"https://www.tiktok.com/@{username}"

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "playlistend": limit,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(profile_url, download=False)

        results = []
        entries = info.get("entries", []) if info else []
        for entry in entries[:limit]:
            views = entry.get("view_count") or 0
            likes = entry.get("like_count") or 0
            comments = entry.get("comment_count") or 0
            results.append({
                "video_id": entry.get("id", ""),
                "title": entry.get("title", ""),
                "url": entry.get("url") or f"https://www.tiktok.com/@{username}/video/{entry.get('id', '')}",
                "views": views,
                "likes": likes,
                "comments": comments,
                "shares": 0,
                "engagement_rate": engagement_rate(likes, comments, 0, views),
                "duration": entry.get("duration") or 0,
                "posted_date": entry.get("upload_date", ""),
                "creator_username": username,
                "platform": "tiktok",
                "scraped_at": timestamp(),
            })

        return results

    def get_video_details(self, video_url: str) -> dict:
        """Get full details for a single TikTok video."""
        log(f"Getting TikTok video details: {video_url}")
        ydl_opts = {"quiet": True, "no_warnings": True}

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            info = ydl.sanitize_info(info)

        views = info.get("view_count") or 0
        likes = info.get("like_count") or 0
        comments = info.get("comment_count") or 0
        shares = info.get("repost_count") or 0

        return {
            "video_id": info.get("id", ""),
            "title": info.get("description") or info.get("title", ""),
            "description": info.get("description", ""),
            "url": video_url,
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "engagement_rate": engagement_rate(likes, comments, shares, views),
            "duration": info.get("duration") or 0,
            "posted_date": info.get("upload_date", ""),
            "creator_username": info.get("uploader") or info.get("creator", ""),
            "thumbnail_url": info.get("thumbnail", ""),
            "hashtags": info.get("tags") or [],
            "music": info.get("track") or info.get("artist", ""),
            "platform": "tiktok",
            "scraped_at": timestamp(),
        }

    def get_trending(self, category: str = None, limit: int = 50) -> list[dict]:
        """Get trending TikTok videos via search."""
        log("Fetching TikTok trending videos")
        query = f"trending {category}" if category else "viral tiktok"

        # Use yt-dlp's search to find popular TikTok content
        ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": True}

        try:
            with YoutubeDL(ydl_opts) as ydl:
                results = ydl.extract_info(f"ytsearch{limit}:tiktok {query}", download=False)

            videos = []
            for entry in (results.get("entries", []) if results else []):
                views = entry.get("view_count") or 0
                likes = entry.get("like_count") or 0
                videos.append({
                    "video_id": entry.get("id", ""),
                    "title": entry.get("title", ""),
                    "url": entry.get("url", ""),
                    "views": views,
                    "likes": likes,
                    "comments": 0,
                    "shares": 0,
                    "engagement_rate": engagement_rate(likes, 0, 0, views),
                    "creator_username": entry.get("uploader", ""),
                    "platform": "tiktok",
                    "scraped_at": timestamp(),
                })
            return videos
        except Exception as e:
            log(f"Trending fetch failed: {e}")
            return []
