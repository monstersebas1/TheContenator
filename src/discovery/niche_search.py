"""Niche Search — find top creators in any niche across platforms."""


def search_niche(keyword: str, platform: str = "tiktok", limit: int = 20) -> list[dict]:
    """
    Search a niche keyword and return top accounts ranked by engagement.

    Args:
        keyword: Niche to search (e.g. "fitness", "cooking", "gaming")
        platform: Which platform to search ("tiktok", "youtube", "instagram")
        limit: Max number of accounts to return

    Returns:
        List of account dicts with: username, followers, avg_views, engagement_rate, profile_url
    """
    raise NotImplementedError("niche_search not yet built")
