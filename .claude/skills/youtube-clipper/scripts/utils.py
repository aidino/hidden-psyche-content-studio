#!/usr/bin/env python3
"""
Common utility functions
Provides time format conversion, filename sanitization, path handling, etc.
"""

import re
import os
from pathlib import Path
from datetime import datetime


def time_to_seconds(time_str: str) -> float:
    """
    Convert time string to seconds

    Supported formats:
    - HH:MM:SS.mmm
    - MM:SS.mmm
    - SS.mmm

    Args:
        time_str: Time string

    Returns:
        float: Seconds

    Examples:
        >>> time_to_seconds("01:23:45.678")
        5025.678
        >>> time_to_seconds("23:45.678")
        1425.678
        >>> time_to_seconds("45.678")
        45.678
    """
    # Remove spaces
    time_str = time_str.strip()

    # Split time parts
    parts = time_str.split(':')

    if len(parts) == 3:
        # HH:MM:SS.mmm
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    elif len(parts) == 2:
        # MM:SS.mmm
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    else:
        # SS.mmm
        return float(parts[0])


def seconds_to_time(seconds: float, include_hours: bool = True, use_comma: bool = False) -> str:
    """
    Convert seconds to time string

    Args:
        seconds: Seconds
        include_hours: Whether to include hours (even if 0)
        use_comma: Use comma to separate milliseconds (required for SRT format)

    Returns:
        str: Time string

    Examples:
        >>> seconds_to_time(5025.678)
        '01:23:45.678'
        >>> seconds_to_time(1425.678, include_hours=False)
        '23:45.678'
        >>> seconds_to_time(5025.678, use_comma=True)
        '01:23:45,678'
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60

    separator = ',' if use_comma else '.'

    if include_hours or hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', separator)
    else:
        return f"{minutes:02d}:{secs:06.3f}".replace('.', separator)


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """
    Sanitize filename by removing illegal characters

    Args:
        filename: Original filename
        max_length: Maximum length

    Returns:
        str: Sanitized filename

    Examples:
        >>> sanitize_filename("Hello: World?")
        'Hello_World'
        >>> sanitize_filename("AGI is not a point in time, it's an exponential curve")
        'AGI_is_not_a_point_in_time_its_an_exponential_curve'
    """
    # Remove or replace illegal characters
    # Common illegal characters for Windows/Mac/Linux
    illegal_chars = r'[<>:"/\\|?*]'
    filename = re.sub(illegal_chars, '_', filename)

    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')

    # Replace spaces with underscores
    filename = filename.replace(' ', '_')

    # Remove consecutive underscores
    filename = re.sub(r'_+', '_', filename)

    # Limit length
    if len(filename) > max_length:
        # Keep extension
        name, ext = os.path.splitext(filename)
        if ext:
            max_name_length = max_length - len(ext)
            filename = name[:max_name_length] + ext
        else:
            filename = filename[:max_length]

    return filename


def create_output_dir(base_dir: str = None) -> Path:
    """
    Create output directory (with timestamp)

    Args:
        base_dir: Base directory, defaults to youtube-clips under current working directory

    Returns:
        Path: Output directory path

    Examples:
        >>> create_output_dir()
        PosixPath('/path/to/current/dir/youtube-clips/20260121_143022')
    """
    if base_dir is None:
        base_dir = Path.cwd() / "youtube-clips"
    else:
        base_dir = Path(base_dir)

    # Create subdirectory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = base_dir / timestamp

    # Create directory
    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir


def format_file_size(size_bytes: int) -> str:
    """
    Format file size to human-readable format

    Args:
        size_bytes: File size (bytes)

    Returns:
        str: Formatted size

    Examples:
        >>> format_file_size(1024)
        '1.0 KB'
        >>> format_file_size(1536)
        '1.5 KB'
        >>> format_file_size(1048576)
        '1.0 MB'
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def parse_time_range(time_range: str) -> tuple:
    """
    Parse time range string

    Args:
        time_range: Time range string, e.g. "00:00 - 03:15" or "00:00-03:15"

    Returns:
        tuple: (start_seconds, end_seconds)

    Examples:
        >>> parse_time_range("00:00 - 03:15")
        (0.0, 195.0)
        >>> parse_time_range("01:30:00-01:33:15")
        (5400.0, 5595.0)
    """
    # Remove spaces and split
    parts = time_range.replace(' ', '').split('-')
    if len(parts) != 2:
        raise ValueError(f"Invalid time range format: {time_range}")

    start_time = time_to_seconds(parts[0])
    end_time = time_to_seconds(parts[1])

    if start_time >= end_time:
        raise ValueError(f"Start time must be before end time: {time_range}")

    return start_time, end_time


def adjust_subtitle_time(time_seconds: float, offset: float) -> float:
    """
    Adjust subtitle timestamp (used for subtitles after clipping)

    Args:
        time_seconds: Original time (seconds)
        offset: Offset (seconds), usually the clip start time

    Returns:
        float: Adjusted time

    Examples:
        >>> adjust_subtitle_time(125.5, 120.0)
        5.5
    """
    adjusted = time_seconds - offset
    return max(0.0, adjusted)  # Ensure non-negative


def get_video_duration_display(seconds: float) -> str:
    """
    Get display format for video duration

    Args:
        seconds: Duration (seconds)

    Returns:
        str: Formatted duration

    Examples:
        >>> get_video_duration_display(125.5)
        '02:05'
        >>> get_video_duration_display(3725.5)
        '1:02:05'
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def validate_url(url: str) -> bool:
    """
    Validate YouTube URL format

    Args:
        url: YouTube URL

    Returns:
        bool: Is valid

    Examples:
        >>> validate_url("https://youtube.com/watch?v=Ckt1cj0xjRM")
        True
        >>> validate_url("https://youtu.be/Ckt1cj0xjRM")
        True
        >>> validate_url("invalid_url")
        False
    """
    # Supported YouTube URL formats
    patterns = [
        r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'https?://(?:www\.)?youtu\.be/[\w-]+',
        r'https?://(?:www\.)?youtube\.com/embed/[\w-]+',
    ]

    return any(re.match(pattern, url) for pattern in patterns)


def ensure_directory(path: Path) -> Path:
    """
    Ensure directory exists, create if not present

    Args:
        path: Directory path

    Returns:
        Path: Directory path
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


if __name__ == "__main__":
    # Test code
    print("Testing utils.py...")

    # Test time conversion
    assert time_to_seconds("01:23:45.678") == 5025.678
    assert time_to_seconds("23:45.678") == 1425.678
    assert time_to_seconds("45.678") == 45.678

    # Test filename sanitization
    assert sanitize_filename("Hello: World?") == "Hello_World"
    assert sanitize_filename("AGI is not a point in time, it's an exponential curve") == "AGI_is_not_a_point_in_time_its_an_exponential_curve"

    # Test time range parsing
    assert parse_time_range("00:00 - 03:15") == (0.0, 195.0)
    assert parse_time_range("01:30:00-01:33:15") == (5400.0, 5595.0)

    # Test URL validation
    assert validate_url("https://youtube.com/watch?v=Ckt1cj0xjRM") == True
    assert validate_url("https://youtu.be/Ckt1cj0xjRM") == True
    assert validate_url("invalid_url") == False

    print("✅ All tests passed!")
