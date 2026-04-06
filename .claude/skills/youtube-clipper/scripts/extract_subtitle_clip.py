#!/usr/bin/env python3
"""
Extract subtitle clip and convert to SRT format
"""

import sys
import re
from datetime import timedelta

def parse_vtt_time(time_str):
    """Parse VTT time format to seconds"""
    parts = time_str.strip().split(':')
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes = int(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    return 0

def format_srt_time(seconds):
    """Format to SRT time"""
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    secs = int(td.total_seconds() % 60)
    millis = int((td.total_seconds() % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def extract_subtitle_clip(vtt_file, start_time, end_time, output_file):
    """Extract subtitle clip"""
    # Parse time
    start_seconds = parse_vtt_time(start_time)
    end_seconds = parse_vtt_time(end_time)

    print(f"📝 Extracting subtitle clip...")
    print(f"   Input: {vtt_file}")
    print(f"   Time range: {start_time} - {end_time}")
    print(f"   Time range (seconds): {start_seconds:.1f}s - {end_seconds:.1f}s")

    # Read VTT file
    with open(vtt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse subtitles
    subtitles = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Find timestamp line
        if '-->' in line:
            # Parse timestamps
            time_parts = line.split('-->')
            sub_start_str = time_parts[0].strip().split()[0]
            sub_end_str = time_parts[1].strip().split()[0]

            sub_start = parse_vtt_time(sub_start_str)
            sub_end = parse_vtt_time(sub_end_str)

            # Check if within target time range
            if sub_start >= start_seconds and sub_end <= end_seconds:
                # Collect subtitle text
                i += 1
                text_lines = []
                while i < len(lines) and lines[i].strip() != '':
                    text_lines.append(lines[i].strip())
                    i += 1

                text = ' '.join(text_lines)

                # Adjust timestamps (subtract start time)
                adjusted_start = sub_start - start_seconds
                adjusted_end = sub_end - start_seconds

                subtitles.append({
                    'start': adjusted_start,
                    'end': adjusted_end,
                    'text': text
                })

        i += 1

    print(f"   Found {len(subtitles)} subtitles")

    # Write in SRT format
    with open(output_file, 'w', encoding='utf-8') as f:
        for idx, sub in enumerate(subtitles, 1):
            f.write(f"{idx}\n")
            f.write(f"{format_srt_time(sub['start'])} --> {format_srt_time(sub['end'])}\n")
            f.write(f"{sub['text']}\n")
            f.write("\n")

    print(f"✅ Subtitle extraction complete")
    print(f"   Output file: {output_file}")
    print(f"   Subtitle count: {len(subtitles)}")

    return subtitles

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python extract_subtitle_clip.py <vtt_file> <start_time> <end_time> <output_file>")
        print("Example: python extract_subtitle_clip.py input.vtt 00:05:47 00:09:19 output.srt")
        sys.exit(1)

    vtt_file = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    output_file = sys.argv[4]

    extract_subtitle_clip(vtt_file, start_time, end_time, output_file)
