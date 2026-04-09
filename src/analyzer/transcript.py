"""Transcript — extract spoken script from any video using Faster-Whisper."""

import os
from faster_whisper import WhisperModel

from core.config import get
from core.utils import DATA_DIR, ensure_data_dirs, log

TRANSCRIPTS_DIR = os.path.join(DATA_DIR, "transcripts")


def _get_model() -> WhisperModel:
    """Load the Whisper model from config."""
    whisper_cfg = get("whisper", {})
    model_size = whisper_cfg.get("model", "base")
    device = whisper_cfg.get("device", "auto")
    compute_type = whisper_cfg.get("compute_type", "int8")

    log(f"Loading Whisper model: {model_size} (device={device}, compute={compute_type})")
    return WhisperModel(model_size, device=device, compute_type=compute_type)


def transcribe(video_path: str, language: str = "en") -> dict:
    """
    Transcribe a downloaded video's audio to text.

    Args:
        video_path: Path to the downloaded video file
        language: Language code for transcription

    Returns:
        Dict with: full_text, segments, language, duration
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    model = _get_model()
    segments_iter, info = model.transcribe(video_path, language=language)

    segments = []
    full_text_parts = []

    for segment in segments_iter:
        seg = {
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip(),
        }
        segments.append(seg)
        full_text_parts.append(segment.text.strip())

    full_text = " ".join(full_text_parts)
    log(f"Transcribed {len(segments)} segments, {len(full_text)} chars")

    return {
        "full_text": full_text,
        "segments": segments,
        "language": info.language,
        "duration": round(info.duration, 2),
    }


def save_transcript(transcript: dict, output_path: str = None, video_id: str = "unknown") -> str:
    """
    Save transcript to a readable text file.

    Args:
        transcript: Output from transcribe()
        output_path: Where to save the .txt file (auto-generated if None)
        video_id: Used for filename if output_path not given

    Returns:
        Path to saved file
    """
    ensure_data_dirs()

    if not output_path:
        output_path = os.path.join(TRANSCRIPTS_DIR, f"{video_id}_transcript.txt")

    lines = []
    lines.append(f"Language: {transcript.get('language', 'unknown')}")
    lines.append(f"Duration: {transcript.get('duration', 0)}s")
    lines.append(f"Segments: {len(transcript.get('segments', []))}")
    lines.append("")
    lines.append("=" * 60)
    lines.append("FULL SCRIPT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(transcript.get("full_text", ""))
    lines.append("")
    lines.append("=" * 60)
    lines.append("TIMESTAMPED SEGMENTS")
    lines.append("=" * 60)
    lines.append("")

    for seg in transcript.get("segments", []):
        start = seg.get("start", 0)
        end = seg.get("end", 0)
        text = seg.get("text", "")
        mins_s, secs_s = divmod(start, 60)
        mins_e, secs_e = divmod(end, 60)
        lines.append(f"[{int(mins_s):02d}:{secs_s:05.2f} -> {int(mins_e):02d}:{secs_e:05.2f}] {text}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    log(f"Transcript saved to: {output_path}")
    return output_path
