"""Downloader — download videos from any platform using yt-dlp."""

import os
from yt_dlp import YoutubeDL

from core.utils import DATA_DIR, ensure_data_dirs, log

DOWNLOADS_DIR = os.path.join(DATA_DIR, "downloads")

# Quality presets mapped to yt-dlp format strings
QUALITY_MAP = {
    "best": "bestvideo+bestaudio/best",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "audio_only": "bestaudio/best",
}


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
    ensure_data_dirs()
    output_dir = output_dir or DOWNLOADS_DIR
    fmt = QUALITY_MAP.get(quality, quality)

    outtmpl = os.path.join(output_dir, "%(extractor)s_%(uploader)s_%(id)s.%(ext)s")

    ydl_opts = {
        "format": fmt,
        "merge_output_format": "mp4",
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        # prepare_filename returns the final post-merge path
        final_path = ydl.prepare_filename(info)
        # If merge happened, extension might differ — force .mp4
        base, _ = os.path.splitext(final_path)
        mp4_path = base + ".mp4"
        if os.path.exists(mp4_path):
            final_path = mp4_path

    log(f"Download complete: {os.path.basename(final_path)}")
    return final_path


def batch_download(urls: list[str], output_dir: str = None, quality: str = "best") -> list[str]:
    """
    Download multiple videos.

    Args:
        urls: List of video URLs
        output_dir: Where to save
        quality: Video quality

    Returns:
        List of paths to downloaded files
    """
    results = []
    for url in urls:
        try:
            path = download(url, output_dir=output_dir, quality=quality)
            results.append(path)
        except Exception as e:
            log(f"Failed to download {url}: {e}")
            results.append(None)
    return results
