#!/usr/bin/env python3
"""
Merge English and Chinese subtitles into a bilingual SRT file
"""

import sys
import re

def parse_srt_file(file_path):
    """Parse SRT file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split subtitle blocks
    blocks = content.strip().split('\n\n')
    subtitles = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            index = lines[0]
            time = lines[1]
            text = '\n'.join(lines[2:])
            subtitles.append({
                'index': index,
                'time': time,
                'text': text
            })

    return subtitles

def merge_bilingual_subtitles(english_file, chinese_file, output_file):
    """Merge English and localized subtitles"""
    print(f"📝 Merging bilingual subtitles...")
    print(f"   English subtitles: {english_file}")
    print(f"   Target subtitles: {chinese_file}")

    # Parse both subtitle files
    english_subs = parse_srt_file(english_file)
    chinese_subs = parse_srt_file(chinese_file)

    if len(english_subs) != len(chinese_subs):
        print(f"⚠️  Warning: English subtitles ({len(english_subs)} lines) and target subtitles ({len(chinese_subs)} lines) count mismatch")

    # Merge subtitles
    bilingual_subs = []
    for i in range(min(len(english_subs), len(chinese_subs))):
        bilingual_subs.append({
            'index': english_subs[i]['index'],
            'time': english_subs[i]['time'],
            'text': f"{english_subs[i]['text']}\n{chinese_subs[i]['text']}"
        })

    # Write bilingual subtitle file
    with open(output_file, 'w', encoding='utf-8') as f:
        for sub in bilingual_subs:
            f.write(f"{sub['index']}\n")
            f.write(f"{sub['time']}\n")
            f.write(f"{sub['text']}\n")
            f.write("\n")

    print(f"✅ Bilingual subtitles generated")
    print(f"   Output file: {output_file}")
    print(f"   Subtitle count: {len(bilingual_subs)}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python merge_bilingual_subtitles.py <english_srt> <translated_srt> <output_srt>")
        sys.exit(1)

    english_file = sys.argv[1]
    chinese_file = sys.argv[2]
    output_file = sys.argv[3]

    merge_bilingual_subtitles(english_file, chinese_file, output_file)
