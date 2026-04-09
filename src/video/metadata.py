"""Metadata — extract video metadata from any platform without downloading."""

from yt_dlp import YoutubeDL

from core.utils import log


def get_metadata(url: str) -> dict:
    """
    Extract metadata from a video URL without downloading the video.

    Args:
        url: Video URL (YouTube, TikTok, Instagram, etc.)

    Returns:
        Dict with: title, description, duration, uploader, upload_date,
        view_count, like_count, comment_count, thumbnail, tags, platform
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)

    return {
        "title": info.get("title"),
        "description": info.get("description"),
        "duration": info.get("duration"),
        "uploader": info.get("uploader"),
        "uploader_id": info.get("uploader_id"),
        "upload_date": info.get("upload_date"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "comment_count": info.get("comment_count"),
        "thumbnail": info.get("thumbnail"),
        "tags": info.get("tags", []),
        "categories": info.get("categories", []),
        "platform": info.get("extractor", "").lower(),
        "video_id": info.get("id"),
        "url": url,
        "filesize": info.get("filesize_approx") or info.get("filesize"),
        "resolution": f"{info.get('width', '?')}x{info.get('height', '?')}",
    }
