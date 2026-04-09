"""Trending — discover trending content by platform and category."""


def get_trending(platform: str = "tiktok", category: str = None, limit: int = 50) -> list[dict]:
    """
    Get currently trending videos on a platform.

    Args:
        platform: Which platform ("tiktok", "youtube", "instagram")
        category: Optional category/niche filter
        limit: Max results

    Returns:
        List of video dicts with stats and creator info
    """
    raise NotImplementedError("trending not yet built")
