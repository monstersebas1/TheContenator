"""Comparator — side-by-side comparison of accounts or videos."""


def compare_accounts(usernames: list[str], platform: str = "tiktok") -> dict:
    """
    Compare multiple accounts side-by-side.

    Args:
        usernames: List of usernames to compare
        platform: Platform to query

    Returns:
        Dict with comparison table: followers, avg_views, engagement_rate,
        posting_frequency, top_video, niche/category
    """
    raise NotImplementedError("compare_accounts not yet built")


def compare_videos(video_urls: list[str]) -> dict:
    """
    Compare multiple videos side-by-side.

    Args:
        video_urls: List of video URLs to compare

    Returns:
        Dict with comparison: views, likes, comments, engagement_rate,
        duration, hashtags, posted_date
    """
    raise NotImplementedError("compare_videos not yet built")
