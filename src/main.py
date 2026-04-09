"""TheContenator — CLI Entry Point"""

import sys
import os

# Add src/ to path so modules can import each other
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prettytable import PrettyTable

from core.constants import APP_NAME, APP_VERSION, PLATFORMS, SORT_OPTIONS
from core.utils import format_number, log, ensure_data_dirs
from storage.db import init_db


# ─── Helpers ──────────────────────────────────────────────

def pick_platform() -> str | None:
    """Prompt user to select a platform."""
    print()
    for i, p in enumerate(PLATFORMS, 1):
        print(f"    [{i}] {p.capitalize()}")
    print()
    choice = input("    Platform: ").strip()
    try:
        return PLATFORMS[int(choice) - 1]
    except (ValueError, IndexError):
        print("    Invalid choice.")
        return None


def display_accounts(accounts: list[dict]):
    """Pretty-print a list of accounts."""
    if not accounts:
        print("\n    No accounts found.")
        return
    table = PrettyTable()
    table.field_names = ["#", "Username", "Followers", "Videos", "Platform"]
    table.align["Username"] = "l"
    table.align["Followers"] = "r"
    table.align["Videos"] = "r"
    for i, a in enumerate(accounts, 1):
        table.add_row([
            i,
            a.get("username", "?"),
            format_number(a.get("followers", 0)),
            a.get("total_videos", "?"),
            a.get("platform", "?"),
        ])
    print()
    print(table)


def display_videos(videos: list[dict]):
    """Pretty-print a list of videos."""
    if not videos:
        print("\n    No videos found.")
        return
    table = PrettyTable()
    table.field_names = ["#", "Title", "Views", "Likes", "Comments", "Eng%"]
    table.align["Title"] = "l"
    table.align["Views"] = "r"
    table.align["Likes"] = "r"
    table.align["Comments"] = "r"
    table.align["Eng%"] = "r"
    table.max_width["Title"] = 40
    for i, v in enumerate(videos, 1):
        table.add_row([
            i,
            (v.get("title", "?") or "?")[:40],
            format_number(v.get("views", 0)),
            format_number(v.get("likes", 0)),
            format_number(v.get("comments", 0)),
            f"{v.get('engagement_rate', 0):.1f}%",
        ])
    print()
    print(table)
    return videos


def display_video_details(details: dict):
    """Pretty-print full video details."""
    print()
    print("    " + "=" * 50)
    print(f"    {details.get('title', 'Untitled')}")
    print("    " + "=" * 50)
    fields = [
        ("Platform", details.get("platform", "?")),
        ("Creator", details.get("creator_username", details.get("uploader", "?"))),
        ("Views", format_number(details.get("views", details.get("view_count", 0)) or 0)),
        ("Likes", format_number(details.get("likes", details.get("like_count", 0)) or 0)),
        ("Comments", format_number(details.get("comments", details.get("comment_count", 0)) or 0)),
        ("Shares", format_number(details.get("shares", 0) or 0)),
        ("Engagement", f"{details.get('engagement_rate', 0):.1f}%"),
        ("Duration", f"{details.get('duration', 0)}s"),
        ("Posted", details.get("posted_date", details.get("upload_date", "?"))),
        ("Hashtags", ", ".join(details.get("hashtags", details.get("tags", [])) or [])),
        ("Resolution", details.get("resolution", "?")),
    ]
    for label, value in fields:
        if value and value != "?" and value != "0" and value != "0s":
            print(f"    {label:>12}: {value}")
    print()


# ─── Discovery Menu ──────────────────────────────────────

def discovery_menu():
    """Discovery submenu."""
    print("\n    --- Discover ---")
    print("    [1] Search niche — find top creators")
    print("    [2] Browse account — see all videos")
    print("    [3] Trending — what's hot right now")
    print("    [0] Back")
    print()
    return input("    Select: ").strip()


def handle_discovery():
    """Handle discovery submenu actions."""
    while True:
        choice = discovery_menu()

        if choice == "1":
            platform = pick_platform()
            if not platform:
                continue
            keyword = input("    Niche keyword: ").strip()
            if not keyword:
                continue
            try:
                from discovery.niche_search import search_niche
                results = search_niche(keyword, platform=platform)
                display_accounts(results)
            except Exception as e:
                print(f"\n    Error: {e}")

        elif choice == "2":
            platform = pick_platform()
            if not platform:
                continue
            username = input("    Username: ").strip().lstrip("@")
            if not username:
                continue
            print(f"\n    Sort options: {', '.join(SORT_OPTIONS)}")
            sort_by = input("    Sort by [most_views]: ").strip() or "most_views"
            try:
                from discovery.account_browser import browse_account
                videos = browse_account(username, platform=platform, sort_by=sort_by)
                displayed = display_videos(videos)
                if displayed:
                    video_actions(displayed, platform)
            except Exception as e:
                print(f"\n    Error: {e}")

        elif choice == "3":
            platform = pick_platform()
            if not platform:
                continue
            category = input("    Category (optional): ").strip() or None
            try:
                from discovery.trending import get_trending
                videos = get_trending(platform=platform, category=category)
                displayed = display_videos(videos)
                if displayed:
                    video_actions(displayed, platform)
            except Exception as e:
                print(f"\n    Error: {e}")

        elif choice == "0":
            break


# ─── Video Actions (after listing) ───────────────────────

def video_actions(videos: list[dict], platform: str):
    """After displaying a video list, let the user act on them."""
    while True:
        print()
        print("    [#] Enter video number for details")
        print("    [d #] Download video #")
        print("    [t #] Transcribe video #")
        print("    [0] Back")
        print()
        action = input("    Action: ").strip().lower()

        if action == "0":
            break

        parts = action.split()
        cmd = parts[0] if parts else ""
        num = parts[1] if len(parts) > 1 else parts[0] if parts else ""

        try:
            idx = int(num if cmd in ("d", "t") else cmd) - 1
            if idx < 0 or idx >= len(videos):
                print("    Invalid number.")
                continue
            video = videos[idx]
        except ValueError:
            print("    Invalid input.")
            continue

        if cmd == "d":
            # Download
            url = video.get("url", "")
            if not url:
                print("    No URL available.")
                continue
            try:
                from video.downloader import download
                print(f"\n    Downloading: {video.get('title', url)[:50]}...")
                path = download(url)
                print(f"    Saved to: {path}")
            except Exception as e:
                print(f"    Download failed: {e}")

        elif cmd == "t":
            # Transcribe (download first, then transcribe)
            url = video.get("url", "")
            if not url:
                print("    No URL available.")
                continue
            try:
                from video.downloader import download
                from analyzer.transcript import transcribe, save_transcript
                print(f"\n    Downloading for transcription...")
                path = download(url)
                print(f"    Transcribing...")
                result = transcribe(path)
                vid_id = video.get("video_id", "unknown")
                txt_path = save_transcript(result, video_id=vid_id)
                print(f"\n    --- Script ---")
                print(f"    {result['full_text'][:500]}")
                if len(result['full_text']) > 500:
                    print(f"    ... ({len(result['full_text'])} chars total)")
                print(f"\n    Full transcript saved: {txt_path}")
            except Exception as e:
                print(f"    Transcription failed: {e}")

        else:
            # Show details
            url = video.get("url", "")
            if url:
                try:
                    from analyzer.video_stats import analyze_video
                    details = analyze_video(url)
                    display_video_details(details)
                except Exception as e:
                    print(f"    Error getting details: {e}")
            else:
                display_video_details(video)


# ─── Analyze Menu ────────────────────────────────────────

def handle_analyze():
    """Handle analyzer submenu."""
    print("\n    --- Analyze ---")
    print("    [1] Video stats — analyze any video URL")
    print("    [2] Transcribe — extract script from video URL")
    print("    [0] Back")
    print()
    choice = input("    Select: ").strip()

    if choice == "1":
        url = input("    Video URL: ").strip()
        if not url:
            return
        try:
            from analyzer.video_stats import analyze_video
            details = analyze_video(url)
            display_video_details(details)
        except Exception as e:
            print(f"\n    Error: {e}")

    elif choice == "2":
        url = input("    Video URL: ").strip()
        if not url:
            return
        try:
            from video.downloader import download
            from analyzer.transcript import transcribe, save_transcript
            print("\n    Downloading...")
            path = download(url)
            print("    Transcribing...")
            result = transcribe(path)
            txt_path = save_transcript(result)
            print(f"\n    --- Script ---")
            print(f"    {result['full_text'][:1000]}")
            if len(result['full_text']) > 1000:
                print(f"    ... ({len(result['full_text'])} chars total)")
            print(f"\n    Full transcript saved: {txt_path}")
        except Exception as e:
            print(f"\n    Error: {e}")


# ─── Download Menu ───────────────────────────────────────

def handle_download():
    """Handle download submenu."""
    print("\n    --- Download ---")
    print("    [1] Single video")
    print("    [2] Batch download (paste URLs)")
    print("    [0] Back")
    print()
    choice = input("    Select: ").strip()

    if choice == "1":
        url = input("    Video URL: ").strip()
        if not url:
            return
        print(f"    Quality options: best, 720p, 480p, audio_only")
        quality = input("    Quality [best]: ").strip() or "best"
        try:
            from video.downloader import download
            print("\n    Downloading...")
            path = download(url, quality=quality)
            print(f"    Saved to: {path}")
        except Exception as e:
            print(f"\n    Error: {e}")

    elif choice == "2":
        print("    Paste URLs (one per line, empty line to finish):")
        urls = []
        while True:
            line = input("    ").strip()
            if not line:
                break
            urls.append(line)
        if not urls:
            return
        try:
            from video.downloader import batch_download
            print(f"\n    Downloading {len(urls)} videos...")
            paths = batch_download(urls)
            for i, p in enumerate(paths):
                status = p if p else "FAILED"
                print(f"    [{i+1}] {status}")
        except Exception as e:
            print(f"\n    Error: {e}")


# ─── Main ────────────────────────────────────────────────

def main_menu():
    """Display the main interactive menu."""
    print()
    print("  " + "=" * 50)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print("  Creator Research & Content Intelligence")
    print("  " + "=" * 50)
    print()
    print("  [1] Discover  — Search niches & find top creators")
    print("  [2] Analyze   — Video stats & script extraction")
    print("  [3] Download  — Grab videos from any platform")
    print("  [0] Exit")
    print()
    return input("  Select: ").strip()


def run():
    """Main application loop."""
    ensure_data_dirs()
    init_db()

    while True:
        choice = main_menu()

        if choice == "1":
            handle_discovery()
        elif choice == "2":
            handle_analyze()
        elif choice == "3":
            handle_download()
        elif choice == "0":
            print("\n  Goodbye.\n")
            sys.exit(0)
        else:
            print("\n  Invalid option.")


if __name__ == "__main__":
    run()
