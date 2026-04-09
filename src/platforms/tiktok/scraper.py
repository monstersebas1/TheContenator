"""TikTok Scraper — uses TikTok-Api for accounts, videos, and stats."""

import asyncio

from TikTokApi import TikTokApi

from core.config import config_get
from core.utils import log, engagement_rate, timestamp
from platforms.base import BaseScraper


class TikTokScraper(BaseScraper):
    """TikTok platform scraper using the unofficial TikTok-Api."""

    @property
    def platform_name(self) -> str:
        return "tiktok"

    def _get_ms_tokens(self) -> list[str]:
        token = (config_get("tiktok", {}) or {}).get("ms_token", "")
        return [token] if token else []

    def _run(self, coro):
        """Run an async coroutine synchronously."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(asyncio.run, coro).result()
        return asyncio.run(coro)

    async def _search_creators_async(self, keyword: str, limit: int) -> list[dict]:
        results = []
        async with TikTokApi() as api:
            await api.create_sessions(
                num_sessions=1,
                ms_tokens=self._get_ms_tokens(),
                headless=True,
            )
            async for user in api.search.users(keyword, count=limit):
                user_info = user.as_dict if hasattr(user, "as_dict") else {}
                stats = user_info.get("stats", {})
                results.append({
                    "username": getattr(user, "username", ""),
                    "display_name": user_info.get("nickname", ""),
                    "followers": stats.get("followerCount", 0),
                    "following": stats.get("followingCount", 0),
                    "total_videos": stats.get("videoCount", 0),
                    "likes": stats.get("heartCount", 0),
                    "bio": user_info.get("signature", ""),
                    "profile_url": f"https://www.tiktok.com/@{getattr(user, 'username', '')}",
                    "platform": "tiktok",
                    "scraped_at": timestamp(),
                })
        return results

    def search_creators(self, keyword: str, limit: int = 20) -> list[dict]:
        log(f"Searching TikTok creators for: {keyword}")
        return self._run(self._search_creators_async(keyword, limit))

    async def _get_account_videos_async(self, username: str, limit: int) -> list[dict]:
        results = []
        async with TikTokApi() as api:
            await api.create_sessions(
                num_sessions=1,
                ms_tokens=self._get_ms_tokens(),
                headless=True,
            )
            user = api.user(username=username)
            async for video in user.videos(count=limit):
                vdict = video.as_dict if hasattr(video, "as_dict") else {}
                stats = vdict.get("stats", {})
                views = stats.get("playCount", 0)
                likes = stats.get("diggCount", 0)
                comments = stats.get("commentCount", 0)
                shares = stats.get("shareCount", 0)
                results.append({
                    "video_id": getattr(video, "id", ""),
                    "title": vdict.get("desc", ""),
                    "url": f"https://www.tiktok.com/@{username}/video/{getattr(video, 'id', '')}",
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "engagement_rate": engagement_rate(likes, comments, shares, views),
                    "duration": vdict.get("video", {}).get("duration", 0),
                    "posted_date": vdict.get("createTime", ""),
                    "thumbnail_url": vdict.get("video", {}).get("cover", ""),
                    "hashtags": [t.get("hashtagName", "") for t in vdict.get("textExtra", []) if t.get("hashtagName")],
                    "platform": "tiktok",
                    "creator_username": username,
                    "scraped_at": timestamp(),
                })
        return results

    def get_account_videos(self, username: str, limit: int = 50) -> list[dict]:
        log(f"Fetching videos for TikTok user: @{username}")
        return self._run(self._get_account_videos_async(username, limit))

    async def _get_video_details_async(self, video_url: str) -> dict:
        async with TikTokApi() as api:
            await api.create_sessions(
                num_sessions=1,
                ms_tokens=self._get_ms_tokens(),
                headless=True,
            )
            video_id = video_url.split("/video/")[-1].split("?")[0] if "/video/" in video_url else video_url
            video = api.video(id=video_id)
            info = await video.info()
            stats = info.get("stats", info.get("statsV2", {}))
            author = info.get("author", {})
            views = stats.get("playCount") or 0
            likes = stats.get("diggCount") or 0
            comments = stats.get("commentCount") or 0
            shares = stats.get("shareCount") or 0
            return {
                "video_id": video_id,
                "title": info.get("desc", ""),
                "url": video_url,
                "views": views,
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "saves": stats.get("collectCount") or 0,
                "engagement_rate": engagement_rate(likes, comments, shares, views),
                "duration": info.get("video", {}).get("duration") or 0,
                "posted_date": info.get("createTime", ""),
                "creator_username": author.get("uniqueId", ""),
                "creator_display_name": author.get("nickname", ""),
                "thumbnail_url": info.get("video", {}).get("cover", ""),
                "hashtags": [t.get("hashtagName", "") for t in info.get("textExtra", []) if t.get("hashtagName")],
                "music": info.get("music", {}).get("title", ""),
                "platform": "tiktok",
                "scraped_at": timestamp(),
            }

    def get_video_details(self, video_url: str) -> dict:
        log(f"Getting TikTok video details: {video_url}")
        return self._run(self._get_video_details_async(video_url))

    async def _get_trending_async(self, limit: int) -> list[dict]:
        results = []
        async with TikTokApi() as api:
            await api.create_sessions(
                num_sessions=1,
                ms_tokens=self._get_ms_tokens(),
                headless=True,
            )
            async for video in api.trending.videos(count=limit):
                vdict = video.as_dict if hasattr(video, "as_dict") else {}
                stats = vdict.get("stats", {})
                author = vdict.get("author", {})
                views = stats.get("playCount", 0)
                likes = stats.get("diggCount", 0)
                comments = stats.get("commentCount", 0)
                shares = stats.get("shareCount", 0)
                results.append({
                    "video_id": getattr(video, "id", ""),
                    "title": vdict.get("desc", ""),
                    "url": f"https://www.tiktok.com/@{author.get('uniqueId', '')}/video/{getattr(video, 'id', '')}",
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "engagement_rate": engagement_rate(likes, comments, shares, views),
                    "creator_username": author.get("uniqueId", ""),
                    "platform": "tiktok",
                    "scraped_at": timestamp(),
                })
        return results

    def get_trending(self, category: str = None, limit: int = 50) -> list[dict]:
        log("Fetching TikTok trending videos")
        return self._run(self._get_trending_async(limit))
