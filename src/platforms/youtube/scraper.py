"""YouTube Scraper — uses yt-dlp for channels, shorts, search, and stats."""

from yt_dlp import YoutubeDL

from core.utils import log, engagement_rate, timestamp
from platforms.base import BaseScraper


class YouTubeScraper(BaseScraper):
    """YouTube platform scraper using yt-dlp as the backend."""

    @property
    def platform_name(self) -> str:
        return "youtube"

    def _get_channel_stats(self, channel_url: str) -> dict:
        """Fetch a channel page to get subscriber count and video count."""
        ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": True, "playlistend": 1}
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(channel_url, download=False)
            return {
                "followers": info.get("channel_follower_count") or 0,
                "total_videos": info.get("playlist_count") or len(info.get("entries", [])),
                "display_name": info.get("channel") or info.get("uploader", ""),
                "bio": (info.get("description") or "")[:200],
            }
        except Exception:
            return {"followers": 0, "total_videos": 0, "display_name": "", "bio": ""}

    def search_creators(self, keyword: str, limit: int = 20) -> list[dict]:
        """Search YouTube for channels/creators by keyword, then fetch their stats."""
        log(f"Searching YouTube creators for: {keyword}")
        ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": "in_playlist"}

        with YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch{limit * 3}:{keyword}", download=False)

        # Deduplicate by channel
        seen = {}
        for entry in results.get("entries", []):
            channel_id = entry.get("channel_id")
            if not channel_id or channel_id in seen:
                continue
            seen[channel_id] = {
                "username": entry.get("uploader_id", channel_id),
                "display_name": entry.get("uploader", ""),
                "channel_id": channel_id,
                "profile_url": f"https://www.youtube.com/channel/{channel_id}",
                "platform": "youtube",
                "scraped_at": timestamp(),
            }
            if len(seen) >= limit:
                break

        # Fetch real stats for each channel
        creators = list(seen.values())
        log(f"Found {len(creators)} channels, fetching stats...")
        for creator in creators:
            channel_url = f"https://www.youtube.com/channel/{creator['channel_id']}/videos"
            stats = self._get_channel_stats(channel_url)
            creator["followers"] = stats["followers"]
            creator["total_videos"] = stats["total_videos"]
            if stats["display_name"]:
                creator["display_name"] = stats["display_name"]
            creator["bio"] = stats.get("bio", "")

        return creators

    def get_account_videos(self, username: str, limit: int = 50) -> list[dict]:
        """Get videos from a YouTube channel."""
        log(f"Fetching videos for YouTube channel: {username}")

        if username.startswith("http"):
            channel_url = username
        elif username.startswith("@"):
            channel_url = f"https://www.youtube.com/{username}/videos"
        elif username.startswith("UC"):
            channel_url = f"https://www.youtube.com/channel/{username}/videos"
        else:
            channel_url = f"https://www.youtube.com/@{username}/videos"

        ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": "in_playlist"}

        with YoutubeDL(ydl_opts) as ydl:
            channel_info = ydl.extract_info(channel_url, download=False)

        results = []
        entries = channel_info.get("entries", [])
        for entry in entries[:limit]:
            results.append({
                "video_id": entry.get("id", ""),
                "title": entry.get("title", ""),
                "url": entry.get("url", f"https://www.youtube.com/watch?v={entry.get('id', '')}"),
                "views": entry.get("view_count") or 0,
                "duration": entry.get("duration") or 0,
                "posted_date": entry.get("upload_date", ""),
                "creator_username": username,
                "platform": "youtube",
                "scraped_at": timestamp(),
            })

        return results

    def get_video_details(self, video_url: str) -> dict:
        """Get full details for a single YouTube video."""
        log(f"Getting YouTube video details: {video_url}")
        ydl_opts = {"quiet": True, "no_warnings": True}

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            info = ydl.sanitize_info(info)

        views = info.get("view_count") or 0
        likes = info.get("like_count") or 0
        comments = info.get("comment_count") or 0

        return {
            "video_id": info.get("id", ""),
            "title": info.get("title", ""),
            "description": info.get("description", ""),
            "url": video_url,
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": 0,
            "engagement_rate": engagement_rate(likes, comments, 0, views),
            "duration": info.get("duration") or 0,
            "posted_date": info.get("upload_date", ""),
            "creator_username": info.get("uploader", ""),
            "channel_id": info.get("channel_id", ""),
            "thumbnail_url": info.get("thumbnail", ""),
            "tags": info.get("tags") or [],
            "categories": info.get("categories") or [],
            "resolution": f"{info.get('width', '?')}x{info.get('height', '?')}",
            "platform": "youtube",
            "scraped_at": timestamp(),
        }

    def get_trending(self, category: str = None, limit: int = 50) -> list[dict]:
        """Get trending YouTube videos (via search for 'trending' + category)."""
        log("Fetching YouTube trending videos")
        query = f"trending {category}" if category else "trending"
        ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": "in_playlist"}

        with YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)

        videos = []
        for entry in results.get("entries", []):
            videos.append({
                "video_id": entry.get("id", ""),
                "title": entry.get("title", ""),
                "url": entry.get("url", f"https://www.youtube.com/watch?v={entry.get('id', '')}"),
                "views": entry.get("view_count") or 0,
                "duration": entry.get("duration") or 0,
                "creator_username": entry.get("uploader", ""),
                "platform": "youtube",
                "scraped_at": timestamp(),
            })

        return videos
