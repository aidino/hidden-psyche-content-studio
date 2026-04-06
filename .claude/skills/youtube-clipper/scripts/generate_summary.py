#!/usr/bin/env python3
"""
Generate summary copy
Generate social media ready copy based on chapter information
"""

import sys
import json
from pathlib import Path
from typing import Dict


def generate_summary(
    chapter_info: Dict,
    output_path: str = None
) -> str:
    """
    Generate summary copy

    Note: This function needs to be called within the Claude Code Skill environment
    Claude will automatically handle the copy generation logic

    Args:
        chapter_info: Chapter info, contains:
            - title: Chapter title
            - time_range: Time range
            - summary: Core summary
            - keywords: List of keywords
        output_path: Output file path (optional)

    Returns:
        str: Generated copy
    """
    print(f"\n📝 Generating summary copy...")
    print(f"   Chapter: {chapter_info.get('title', 'Unknown')}")

    # Output chapter info (for Claude analysis)
    print("\n" + "="*60)
    print("Chapter Information (JSON format):")
    print("="*60)
    print(json.dumps(chapter_info, indent=2, ensure_ascii=False))

    print("\n" + "="*60)
    print("Copy Generation Requirements:")
    print("="*60)
    print("""
Please generate social media ready copy based on the above chapter information.

Copy requirements:
1. Catchy title (10-20 words)
2. Core points (3-5 bullet points, 1-2 sentences each)
3. Adapted for platforms:
   - Xiaohongshu (Little Red Book): conversational, uses emojis, under 1000 words
   - Douyin (TikTok): concise, highlights catchy phrases, under 300 words
   - WeChat Official Account: detailed, clear structure, no word limit

Output format (Markdown):

# [Title]

## Core Points

1. Point 1
2. Point 2
3. Point 3

## Platform Versions

### Xiaohongshu Version (1000 words)
[Copy content]

### Douyin Version (300 words)
[Copy content]

### WeChat Official Account Version
[Copy content]

## Tags

#Tag1 #Tag2 #Tag3
""")

    # Generate base copy (placeholder)
    summary_template = f"""# {chapter_info.get('title', 'Unnamed Chapter')}

## Chapter Information

- Time range: {chapter_info.get('time_range', 'N/A')}
- Core summary: {chapter_info.get('summary', 'N/A')}
- Keywords: {', '.join(chapter_info.get('keywords', []))}

## Core Points

[Pending generation - Claude will automatically fill this during Skill execution]

## Platform Versions

### Xiaohongshu Version

[Pending generation]

### Douyin Version

[Pending generation]

### WeChat Official Account Version

[Pending generation]

## Tags

{' '.join(['#' + kw for kw in chapter_info.get('keywords', [])])}

---

Generated at: {chapter_info.get('generated_at', 'N/A')}
"""

    # Save to file (if specified)
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary_template)

        print(f"✅ Copy saved: {output_path}")

    return summary_template


def load_chapter_info(json_path: str) -> Dict:
    """
    Load chapter information from JSON file

    Args:
        json_path: JSON file path

    Returns:
        Dict: Chapter information
    """
    json_path = Path(json_path)
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    print(f"📂 Loading chapter info: {json_path.name}")

    with open(json_path, 'r', encoding='utf-8') as f:
        chapter_info = json.load(f)

    return chapter_info


def create_chapter_info(
    title: str,
    time_range: str,
    summary: str,
    keywords: list
) -> Dict:
    """
    Create chapter information dictionary

    Args:
        title: Chapter title
        time_range: Time range (e.g., "00:00 - 03:15")
        summary: Core summary
        keywords: List of keywords

    Returns:
        Dict: Chapter information
    """
    from datetime import datetime

    return {
        'title': title,
        'time_range': time_range,
        'summary': summary,
        'keywords': keywords,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def main():
    """Command line entry point"""
    if len(sys.argv) < 2:
        print("Usage: python generate_summary.py <chapter_info_json> [output_file]")
        print("   or: python generate_summary.py --create <title> <time_range> <summary> <keywords> [output_file]")
        print("\nArguments:")
        print("  chapter_info_json - Chapter info JSON file path")
        print("  output_file       - Output file path (optional, default is summary.md)")
        print("\nCreate mode arguments:")
        print("  --create    - Create mode")
        print("  title       - Chapter title")
        print("  time_range  - Time range (e.g., '00:00 - 03:15')")
        print("  summary     - Core summary")
        print("  keywords    - Keywords (comma separated)")
        print("\nExample:")
        print("  python generate_summary.py chapter.json")
        print("  python generate_summary.py chapter.json summary.md")
        print("  python generate_summary.py --create 'AGI Exponential Curve' '00:00-03:15' 'Core summary' 'AGI,Exponential Growth,Claude' summary.md")
        sys.exit(1)

    try:
        if sys.argv[1] == '--create':
            # Create mode
            if len(sys.argv) < 6:
                print("❌ Create mode requires: title, time_range, summary, keywords")
                sys.exit(1)

            title = sys.argv[2]
            time_range = sys.argv[3]
            summary = sys.argv[4]
            keywords = sys.argv[5].split(',')
            output_file = sys.argv[6] if len(sys.argv) > 6 else 'summary.md'

            chapter_info = create_chapter_info(title, time_range, summary, keywords)

        else:
            # JSON mode
            json_file = sys.argv[1]
            output_file = sys.argv[2] if len(sys.argv) > 2 else 'summary.md'

            chapter_info = load_chapter_info(json_file)

        # Generate copy
        summary = generate_summary(chapter_info, output_file)

        print("\n" + "="*60)
        print("Generated Copy Preview:")
        print("="*60)
        print(summary)

        print("\n⚠️  Note: This script needs to be run within Claude Code Skill")
        print("   Claude will automatically generate detailed copy content")
        print("   Currently only outputting template")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
