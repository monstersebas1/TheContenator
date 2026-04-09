"""Video Stats — full statistics breakdown for any video."""

from core.utils import log, engagement_rate
from video.metadata import get_metadata


def analyze_video(video_url: str) -> dict:
    """
    Analyze a video and return full statistics using yt-dlp metadata extraction.

    Args:
        video_url: URL of the video to analyze

    Returns:
        Dict with all available stats and metadata
    """
    log(f"Analyzing video: {video_url}")
    meta = get_metadata(video_url)

    views = meta.get("view_count", 0) or 0
    likes = meta.get("like_count", 0) or 0
    comments = meta.get("comment_count", 0) or 0

    meta["engagement_rate"] = engagement_rate(likes, comments, 0, views)

    return meta
