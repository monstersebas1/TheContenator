"""Metadata — extract and read video metadata without downloading."""


def get_metadata(url: str) -> dict:
    """
    Extract metadata from a video URL without downloading the video.

    Args:
        url: Video URL

    Returns:
        Dict with: title, description, duration, resolution, filesize,
        uploader, upload_date, view_count, like_count, comment_count
    """
    raise NotImplementedError("metadata not yet built")
