"""Downloader — download videos from any platform using yt-dlp."""


def download(url: str, output_dir: str = None, quality: str = "best") -> str:
    """
    Download a video from any supported platform.

    Args:
        url: Video URL (TikTok, YouTube, Instagram, etc.)
        output_dir: Where to save (defaults to data/downloads/)
        quality: Video quality ("best", "720p", "480p", "audio_only")

    Returns:
        Path to downloaded file
    """
    raise NotImplementedError("downloader not yet built")


def batch_download(urls: list[str], output_dir: str = None) -> list[str]:
    """
    Download multiple videos.

    Args:
        urls: List of video URLs
        output_dir: Where to save

    Returns:
        List of paths to downloaded files
    """
    raise NotImplementedError("batch_download not yet built")
