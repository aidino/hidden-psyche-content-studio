#!/usr/bin/env python3
"""
Download YouTube video and subtitles
Uses yt-dlp to download video (up to 1080p) and English subtitles
"""

import sys
import json
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("❌ Error: yt-dlp not installed")
    print("Please install: pip install yt-dlp")
    sys.exit(1)

from utils import (
    validate_url,
    sanitize_filename,
    format_file_size,
    get_video_duration_display,
    ensure_directory
)


def download_video(url: str, output_dir: str = None) -> dict:
    """
    Download YouTube video and subtitles

    Args:
        url: YouTube URL
        output_dir: Output directory, defaults to current directory

    Returns:
        dict: {
            'video_path': Video file path,
            'subtitle_path': Subtitle file path,
            'title': Video title,
            'duration': Video duration (seconds),
            'file_size': File size (bytes)
        }

    Raises:
        ValueError: Invalid URL
        Exception: Download failed
    """
    # Validate URL
    if not validate_url(url):
        raise ValueError(f"Invalid YouTube URL: {url}")

    # Set output directory
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)

    output_dir = ensure_directory(output_dir)

    print(f"🎬 Starting video download...")
    print(f"   URL: {url}")
    print(f"   Output directory: {output_dir}")

    # Configure yt-dlp options
    ydl_opts = {
        # Video format: max 1080p, prefer mp4
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',

        # Output template: include video ID (avoids special character issues)
        'outtmpl': str(output_dir / '%(id)s.%(ext)s'),

        # Download subtitles
        'writesubtitles': True,
        'writeautomaticsub': True,  # Automatic subtitles as fallback
        'subtitleslangs': ['en'],   # English subtitles
        'subtitlesformat': 'vtt',   # VTT format

        # Do not download thumbnails
        'writethumbnail': False,

        # Quiet mode (reduce output)
        'quiet': False,
        'no_warnings': False,

        # Progress hooks
        'progress_hooks': [_progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info
            print("\n📊 Fetching video information...")
            info = ydl.extract_info(url, download=False)

            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            video_id = info.get('id', 'unknown')

            print(f"   Title: {title}")
            print(f"   Duration: {get_video_duration_display(duration)}")
            print(f"   Video ID: {video_id}")

            # Download video
            print(f"\n📥 Starting download...")
            info = ydl.extract_info(url, download=True)

            # Get downloaded file path
            video_filename = ydl.prepare_filename(info)
            video_path = Path(video_filename)

            # Find subtitle file
            subtitle_path = None
            subtitle_exts = ['.en.vtt', '.vtt']
            for ext in subtitle_exts:
                potential_sub = video_path.with_suffix(ext)
                # Handle subtitle files with language codes
                if not potential_sub.exists():
                    # Process <filename>.en.vtt format
                    stem = video_path.stem
                    potential_sub = video_path.parent / f"{stem}.en.vtt"

                if potential_sub.exists():
                    subtitle_path = potential_sub
                    break

            # Get file size
            file_size = video_path.stat().st_size if video_path.exists() else 0

            # Verify download result
            if not video_path.exists():
                raise Exception("Video file not found after download")

            print(f"\n✅ Video download complete: {video_path.name}")
            print(f"   Size: {format_file_size(file_size)}")

            if subtitle_path and subtitle_path.exists():
                print(f"✅ Subtitle download complete: {subtitle_path.name}")
            else:
                print(f"⚠️  English subtitles not found")
                print(f"   Tip: Some videos might not have subtitles or require auto-generated ones")

            return {
                'video_path': str(video_path),
                'subtitle_path': str(subtitle_path) if subtitle_path else None,
                'title': title,
                'duration': duration,
                'file_size': file_size,
                'video_id': video_id
            }

    except Exception as e:
        print(f"\n❌ Download failed: {str(e)}")
        raise


def _progress_hook(d):
    """Download progress callback"""
    if d['status'] == 'downloading':
        # Display download progress
        if 'downloaded_bytes' in d and 'total_bytes' in d and d['total_bytes']:
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            downloaded = format_file_size(d['downloaded_bytes'])
            total = format_file_size(d['total_bytes'])
            speed = d.get('speed', 0)
            speed_str = format_file_size(speed) + '/s' if speed else 'N/A'

            # Use \r to overwrite progress bar
            bar_length = 30
            filled = int(bar_length * percent / 100)
            bar = '█' * filled + '░' * (bar_length - filled)

            print(f"\r   [{bar}] {percent:.1f}% - {downloaded}/{total} - {speed_str}", end='', flush=True)
        elif 'downloaded_bytes' in d:
            # When missing total size, only show downloaded
            downloaded = format_file_size(d['downloaded_bytes'])
            speed = d.get('speed', 0)
            speed_str = format_file_size(speed) + '/s' if speed else 'N/A'
            print(f"\r   Downloading... {downloaded} - {speed_str}", end='', flush=True)

    elif d['status'] == 'finished':
        print()  # Newline


def main():
    """Command line entry point"""
    if len(sys.argv) < 2:
        print("Usage: python download_video.py <youtube_url> [output_dir]")
        print("\nExample:")
        print("  python download_video.py https://youtube.com/watch?v=Ckt1cj0xjRM")
        print("  python download_video.py https://youtube.com/watch?v=Ckt1cj0xjRM ~/Downloads")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = download_video(url, output_dir)

        # Output JSON result (for other scripts to use)
        print("\n" + "="*60)
        print("Download Result (JSON):")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
