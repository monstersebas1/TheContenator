"""Transcript — extract spoken script from any video using Faster-Whisper."""


def transcribe(video_path: str, language: str = "en") -> dict:
    """
    Transcribe a downloaded video's audio to text.

    Args:
        video_path: Path to the downloaded video file
        language: Language code for transcription

    Returns:
        Dict with: full_text, segments (list of {start, end, text}), language, duration
    """
    raise NotImplementedError("transcript not yet built")


def save_transcript(transcript: dict, output_path: str) -> str:
    """
    Save transcript to a readable text file.

    Args:
        transcript: Output from transcribe()
        output_path: Where to save the .txt file

    Returns:
        Path to saved file
    """
    raise NotImplementedError("save_transcript not yet built")
