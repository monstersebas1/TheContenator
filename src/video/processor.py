"""Processor — trim, overlay text, re-encode videos."""


def trim(video_path: str, start: float, end: float, output_path: str = None) -> str:
    """
    Trim a video to a specific time range.

    Args:
        video_path: Path to source video
        start: Start time in seconds
        end: End time in seconds
        output_path: Where to save (defaults to same dir with _trimmed suffix)

    Returns:
        Path to trimmed video
    """
    raise NotImplementedError("trim not yet built")


def add_text_overlay(video_path: str, text: str, position: str = "bottom", output_path: str = None) -> str:
    """
    Add text overlay to a video.

    Args:
        video_path: Path to source video
        text: Text to overlay
        position: Where to place it ("top", "center", "bottom")
        output_path: Where to save

    Returns:
        Path to processed video
    """
    raise NotImplementedError("add_text_overlay not yet built")
