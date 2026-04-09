"""Account Browser — list and sort videos from any creator account."""


def browse_account(username: str, platform: str = "tiktok", sort_by: str = "most_views") -> list[dict]:
    """
    Fetch all videos from an account and sort them.

    Sort options: most_views, most_comments, most_likes, most_shares,
                  highest_engagement, newest, oldest, trending

    Args:
        username: Creator's username/handle
        platform: Platform to query
        sort_by: Sort order for results

    Returns:
        List of video dicts with: title, url, views, likes, comments, shares,
        engagement_rate, posted_date, duration, thumbnail_url
    """
    raise NotImplementedError("account_browser not yet built")
