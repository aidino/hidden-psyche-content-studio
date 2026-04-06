#!/usr/bin/env python3
"""
Clip video segments
Use FFmpeg for precise video clipping, maintaining original quality
"""

import sys
import shutil
import subprocess
from pathlib import Path
from typing import Union

from utils import (
    time_to_seconds,
    seconds_to_time,
    format_file_size,
    get_video_duration_display
)


def clip_video(
    video_path: str,
    start_time: Union[str, float],
    end_time: Union[str, float],
    output_path: str,
    ffmpeg_path: str = None
) -> str:
    """
    Clip video segment

    Args:
        video_path: Input video path
        start_time: Start time (seconds or time string, e.g. "00:01:30")
        end_time: End time (seconds or time string)
        output_path: Output video path
        ffmpeg_path: FFmpeg executable path (optional)

    Returns:
        str: Output video path

    Raises:
        FileNotFoundError: Input file does not exist
        RuntimeError: FFmpeg execution failed
    """
    video_path = Path(video_path)
    output_path = Path(output_path)

    # Validate input file
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Convert time to seconds
    if isinstance(start_time, str):
        start_seconds = time_to_seconds(start_time)
    else:
        start_seconds = float(start_time)

    if isinstance(end_time, str):
        end_seconds = time_to_seconds(end_time)
    else:
        end_seconds = float(end_time)

    # Validate time range
    if start_seconds >= end_seconds:
        raise ValueError(f"Start time ({start_seconds}s) must be before end time ({end_seconds}s)")

    duration = end_seconds - start_seconds

    # Detect FFmpeg
    if ffmpeg_path is None:
        ffmpeg_path = shutil.which('ffmpeg')
        if not ffmpeg_path:
            raise RuntimeError("FFmpeg not found. Please install FFmpeg.")

    print(f"\n✂️  Clipping video segment...")
    print(f"   Input: {video_path.name}")
    print(f"   Start time: {seconds_to_time(start_seconds)} ({start_seconds}s)")
    print(f"   End time: {seconds_to_time(end_seconds)} ({end_seconds}s)")
    print(f"   Segment duration: {get_video_duration_display(duration)}")
    print(f"   Output: {output_path.name}")

    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build FFmpeg command
    # Use -ss and -t for precise clipping
    # -c copy: Copy stream directly, no re-encoding (fast and lossless)
    cmd = [
        ffmpeg_path,
        '-ss', str(start_seconds),  # Start time
        '-i', str(video_path),       # Input file
        '-t', str(duration),         # Duration
        '-c', 'copy',                # Copy directly, no re-encoding
        '-y',                        # Overwrite output file
        str(output_path)
    ]

    print(f"   Executing FFmpeg...")

    # Execute FFmpeg
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"\n❌ FFmpeg execution failed:")
        print(result.stderr)
        raise RuntimeError(f"FFmpeg failed with return code {result.returncode}")

    # Validate output file
    if not output_path.exists():
        raise RuntimeError("Output file not created")

    # Get file size
    output_size = output_path.stat().st_size
    print(f"✅ Clipping complete")
    print(f"   Output file: {output_path}")
    print(f"   File size: {format_file_size(output_size)}")

    return str(output_path)


def extract_subtitle_segment(
    subtitles: list,
    start_time: float,
    end_time: float,
    adjust_timestamps: bool = True
) -> list:
    """
    Extract subtitles for a specific time segment from full subtitles

    Args:
        subtitles: Full subtitle list (each item contains {start, end, text})
        start_time: Start time (seconds)
        end_time: End time (seconds)
        adjust_timestamps: Whether to adjust timestamps (subtract start time)

    Returns:
        list: Extracted subtitle list
    """
    segment_subtitles = []

    for sub in subtitles:
        # Subtitle within time range
        if sub['start'] >= start_time and sub['end'] <= end_time:
            if adjust_timestamps:
                # Adjust timestamps (relative to segment start time)
                adjusted_sub = {
                    'start': sub['start'] - start_time,
                    'end': sub['end'] - start_time,
                    'text': sub['text']
                }
                segment_subtitles.append(adjusted_sub)
            else:
                segment_subtitles.append(sub.copy())

        # Subtitle crosses time range boundary (partial overlap)
        elif sub['start'] < end_time and sub['end'] > start_time:
            if adjust_timestamps:
                adjusted_sub = {
                    'start': max(0, sub['start'] - start_time),
                    'end': min(end_time - start_time, sub['end'] - start_time),
                    'text': sub['text']
                }
                segment_subtitles.append(adjusted_sub)
            else:
                segment_subtitles.append(sub.copy())

    return segment_subtitles


def save_subtitles_as_srt(subtitles: list, output_path: str):
    """
    Save subtitles in SRT format

    Args:
        subtitles: Subtitle list
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        for i, sub in enumerate(subtitles, 1):
            # SRT sequence number
            f.write(f"{i}\n")

            # SRT timestamps (use comma for milliseconds)
            start_time = seconds_to_time(sub['start'], include_hours=True, use_comma=True)
            end_time = seconds_to_time(sub['end'], include_hours=True, use_comma=True)
            f.write(f"{start_time} --> {end_time}\n")

            # Subtitle text
            f.write(f"{sub['text']}\n")

            # Blank line separator
            f.write("\n")

    print(f"✅ Subtitles saved: {output_path}")


def main():
    """Command line entry point"""
    if len(sys.argv) < 5:
        print("Usage: python clip_video.py <video> <start_time> <end_time> <output>")
        print("\nArguments:")
        print("  video      - Input video file path")
        print("  start_time - Start time (seconds or time string, e.g. 00:01:30)")
        print("  end_time   - End time (seconds or time string)")
        print("  output     - Output video file path")
        print("\nExample:")
        print("  python clip_video.py input.mp4 0 195 output.mp4")
        print("  python clip_video.py input.mp4 00:00:00 00:03:15 output.mp4")
        print("  python clip_video.py input.mp4 01:30:00 01:33:15 output.mp4")
        sys.exit(1)

    video_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    output_path = sys.argv[4]

    try:
        result_path = clip_video(video_path, start_time, end_time, output_path)
        print(f"\n✨ Done! Output file: {result_path}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
