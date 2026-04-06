#!/usr/bin/env python3
"""
Analyze subtitles and generate chapters
Parse VTT subtitle files, prepare data for Claude AI analysis
"""

import sys
import re
import json
from pathlib import Path
from typing import List, Dict

from utils import (
    time_to_seconds,
    seconds_to_time,
    get_video_duration_display
)


def parse_vtt(vtt_path: str) -> List[Dict]:
    """
    Parse VTT subtitle file

    Args:
        vtt_path: VTT file path

    Returns:
        List[Dict]: List of subtitles, each containing {start, end, text}

    Example:
        [
            {'start': 0.0, 'end': 3.5, 'text': 'Hello world'},
            {'start': 3.5, 'end': 7.2, 'text': 'This is a test'},
            ...
        ]
    """
    vtt_path = Path(vtt_path)

    if not vtt_path.exists():
        raise FileNotFoundError(f"Subtitle file not found: {vtt_path}")

    print(f"📊 Parsing subtitle file: {vtt_path.name}")

    subtitles = []

    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove WEBVTT header and style information
    content = re.sub(r'^WEBVTT.*?\n\n', '', content, flags=re.DOTALL)
    content = re.sub(r'STYLE.*?-->', '', content, flags=re.DOTALL)

    # Split subtitle blocks
    blocks = content.strip().split('\n\n')

    for block in blocks:
        lines = block.strip().split('\n')

        if len(lines) < 2:
            continue

        # Find timestamp line
        timestamp_line = None
        text_lines = []

        for line in lines:
            # Match timestamp format: 00:00:00.000 --> 00:00:03.000
            if '-->' in line:
                timestamp_line = line
            elif line and not line.isdigit():  # Skip sequence numbers
                text_lines.append(line)

        if not timestamp_line or not text_lines:
            continue

        # Parse timestamps
        try:
            # Remove potential position info (e.g. align:start position:0%)
            timestamp_line = re.sub(r'align:.*|position:.*', '', timestamp_line).strip()

            times = timestamp_line.split('-->')
            start_str = times[0].strip()
            end_str = times[1].strip()

            start = time_to_seconds(start_str)
            end = time_to_seconds(end_str)

            # Join text lines
            text = ' '.join(text_lines)

            # Clean HTML tags (if any)
            text = re.sub(r'<[^>]+>', '', text)

            # Clean special characters
            text = text.strip()

            if text:
                subtitles.append({
                    'start': start,
                    'end': end,
                    'text': text
                })

        except Exception as e:
            # Skip unparseable subtitle blocks
            continue

    print(f"   Found {len(subtitles)} subtitles")

    if subtitles:
        total_duration = subtitles[-1]['end']
        print(f"   Total duration: {get_video_duration_display(total_duration)}")

    return subtitles


def prepare_analysis_data(subtitles: List[Dict], target_chapter_duration: int = 180) -> Dict:
    """
    Prepare data for Claude AI analysis

    Args:
        subtitles: List of subtitles
        target_chapter_duration: Target chapter duration (seconds), default 180 seconds (3 minutes)

    Returns:
        Dict: {
            'subtitle_text': Full subtitle text with timestamps,
            'total_duration': Total duration,
            'subtitle_count': Subtitle count,
            'target_chapter_duration': Target chapter duration,
            'estimated_chapters': Estimated number of chapters
        }
    """
    if not subtitles:
        raise ValueError("No subtitles to analyze")

    print(f"\n📝 Preparing analysis data...")

    # Combine subtitles into full text with timestamps
    full_text_lines = []

    for sub in subtitles:
        time_str = seconds_to_time(sub['start'], include_hours=True, use_comma=False)
        full_text_lines.append(f"[{time_str}] {sub['text']}")

    full_text = '\n'.join(full_text_lines)

    total_duration = subtitles[-1]['end']
    estimated_chapters = max(1, int(total_duration / target_chapter_duration))

    print(f"   Total duration: {get_video_duration_display(total_duration)}")
    print(f"   Subtitle count: {len(subtitles)}")
    print(f"   Target chapter duration: {target_chapter_duration} seconds ({target_chapter_duration // 60} minutes)")
    print(f"   Estimated chapters: {estimated_chapters}")

    return {
        'subtitle_text': full_text,
        'total_duration': total_duration,
        'subtitle_count': len(subtitles),
        'target_chapter_duration': target_chapter_duration,
        'estimated_chapters': estimated_chapters,
        'subtitles_raw': subtitles  # Keep original data for later use
    }


def save_analysis_data(data: Dict, output_path: str):
    """
    Save analysis data to JSON file

    Args:
        data: Analysis data
        output_path: Output file path
    """
    output_path = Path(output_path)

    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save as JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Analysis data saved: {output_path}")


def main():
    """Command line entry point"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_subtitles.py <vtt_file> [target_duration] [output_json]")
        print("\nArguments:")
        print("  vtt_file         - VTT subtitle file path")
        print("  target_duration  - Target chapter duration (seconds), default 180")
        print("  output_json      - Output JSON file path (optional)")
        print("\nExample:")
        print("  python analyze_subtitles.py video.en.vtt")
        print("  python analyze_subtitles.py video.en.vtt 240")
        print("  python analyze_subtitles.py video.en.vtt 240 analysis.json")
        sys.exit(1)

    vtt_file = sys.argv[1]
    target_duration = int(sys.argv[2]) if len(sys.argv) > 2 else 180
    output_json = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        # Parse subtitles
        subtitles = parse_vtt(vtt_file)

        if not subtitles:
            print("❌ No valid subtitles found")
            sys.exit(1)

        # Prepare analysis data
        analysis_data = prepare_analysis_data(subtitles, target_duration)

        # Output subtitle text (for Claude analysis)
        print("\n" + "="*60)
        print("Subtitle Text (preview of first 50 lines):")
        print("="*60)
        lines = analysis_data['subtitle_text'].split('\n')
        preview_lines = lines[:50]
        print('\n'.join(preview_lines))
        if len(lines) > 50:
            print(f"\n... (and {len(lines) - 50} more lines)")

        # Save to file (if specified)
        if output_json:
            save_analysis_data(analysis_data, output_json)

        # Output summary info
        print("\n" + "="*60)
        print("Analysis Summary:")
        print("="*60)
        print(json.dumps({
            'total_duration': analysis_data['total_duration'],
            'total_duration_display': get_video_duration_display(analysis_data['total_duration']),
            'subtitle_count': analysis_data['subtitle_count'],
            'target_chapter_duration': analysis_data['target_chapter_duration'],
            'estimated_chapters': analysis_data['estimated_chapters']
        }, indent=2, ensure_ascii=False))

        print("\n💡 Tip: You can now use Claude AI to analyze the above subtitle text and generate detailed chapters")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
