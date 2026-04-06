#!/usr/bin/env python3
"""
Burn subtitles into video
Handles FFmpeg libass support and path space issues
"""

import sys
import os
import shutil
import subprocess
import tempfile
import platform
from pathlib import Path
from typing import Dict, Optional

from utils import format_file_size


def detect_ffmpeg_variant() -> Dict:
    """
    Detect FFmpeg version and libass support

    Returns:
        Dict: {
            'type': 'full' | 'standard' | 'none',
            'path': FFmpeg executable path,
            'has_libass': Whether libass is supported
        }
    """
    print("🔍 Detecting FFmpeg environment...")

    # Priority check for ffmpeg-full (macOS)
    if platform.system() == 'Darwin':
        # Apple Silicon
        full_path_arm = '/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg'
        # Intel
        full_path_intel = '/usr/local/opt/ffmpeg-full/bin/ffmpeg'

        for full_path in [full_path_arm, full_path_intel]:
            if Path(full_path).exists():
                has_libass = check_libass_support(full_path)
                print(f"   Found ffmpeg-full: {full_path}")
                print(f"   libass support: {'✅ Yes' if has_libass else '❌ No'}")
                return {
                    'type': 'full',
                    'path': full_path,
                    'has_libass': has_libass
                }

    # Check standard FFmpeg
    standard_path = shutil.which('ffmpeg')
    if standard_path:
        has_libass = check_libass_support(standard_path)
        variant_type = 'full' if has_libass else 'standard'
        print(f"   Found FFmpeg: {standard_path}")
        print(f"   Type: {variant_type}")
        print(f"   libass support: {'✅ Yes' if has_libass else '❌ No'}")
        return {
            'type': variant_type,
            'path': standard_path,
            'has_libass': has_libass
        }

    # FFmpeg not found
    print("   ❌ FFmpeg not found")
    return {
        'type': 'none',
        'path': None,
        'has_libass': False
    }


def check_libass_support(ffmpeg_path: str) -> bool:
    """
    Check if FFmpeg supports libass (required for burning subtitles)

    Args:
        ffmpeg_path: FFmpeg executable path

    Returns:
        bool: Whether libass is supported
    """
    try:
        # Check if subtitles filter is available
        result = subprocess.run(
            [ffmpeg_path, '-filters'],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Search for subtitles filter
        return 'subtitles' in result.stdout.lower()

    except Exception:
        return False


def install_ffmpeg_full_guide():
    """
    Show guide to install ffmpeg-full
    """
    print("\n" + "="*60)
    print("⚠️  ffmpeg-full needs to be installed to burn subtitles")
    print("="*60)

    if platform.system() == 'Darwin':
        print("\nmacOS installation:")
        print("  brew install ffmpeg-full")
        print("\nAfter installation, FFmpeg paths:")
        print("  /opt/homebrew/opt/ffmpeg-full/bin/ffmpeg  (Apple Silicon)")
        print("  /usr/local/opt/ffmpeg-full/bin/ffmpeg     (Intel)")
    else:
        print("\nOther systems:")
        print("  Please compile FFmpeg from source, ensuring libass support is included")
        print("  Reference: https://trac.ffmpeg.org/wiki/CompilationGuide")

    print("\nVerify installation:")
    print("  ffmpeg -filters 2>&1 | grep subtitles")
    print("="*60)


def burn_subtitles(
    video_path: str,
    subtitle_path: str,
    output_path: str,
    ffmpeg_path: str = None,
    font_size: int = 24,
    margin_v: int = 30
) -> str:
    """
    Burn subtitles into video (uses temporary directory to solve path space issues)

    Args:
        video_path: Input video path
        subtitle_path: Subtitle file path (SRT format)
        output_path: Output video path
        ffmpeg_path: FFmpeg executable path (optional)
        font_size: Font size, default 24
        margin_v: Bottom margin, default 30

    Returns:
        str: Output video path

    Raises:
        FileNotFoundError: Input file doesn't exist
        RuntimeError: FFmpeg execution failed
    """
    video_path = Path(video_path)
    subtitle_path = Path(subtitle_path)
    output_path = Path(output_path)

    # Validate input file
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not subtitle_path.exists():
        raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")

    # Detect FFmpeg
    if ffmpeg_path is None:
        ffmpeg_info = detect_ffmpeg_variant()

        if ffmpeg_info['type'] == 'none':
            install_ffmpeg_full_guide()
            raise RuntimeError("FFmpeg not found")

        if not ffmpeg_info['has_libass']:
            install_ffmpeg_full_guide()
            raise RuntimeError("FFmpeg does not support libass (subtitles filter)")

        ffmpeg_path = ffmpeg_info['path']

    print(f"\n🎬 Burning subtitles into video...")
    print(f"   Video: {video_path.name}")
    print(f"   Subtitle: {subtitle_path.name}")
    print(f"   Output: {output_path.name}")
    print(f"   FFmpeg: {ffmpeg_path}")

    # Create temporary directory (solves path space issue)
    temp_dir = tempfile.mkdtemp(prefix='youtube_clipper_')
    print(f"   Using temporary directory: {temp_dir}")

    try:
        # Copy files to temporary directory (path without spaces)
        temp_video = os.path.join(temp_dir, 'video.mp4')
        temp_subtitle = os.path.join(temp_dir, 'subtitle.srt')
        temp_output = os.path.join(temp_dir, 'output.mp4')

        print(f"   Copying files to temporary directory...")
        shutil.copy(video_path, temp_video)
        shutil.copy(subtitle_path, temp_subtitle)

        # Build FFmpeg command
        # Burn subtitles using subtitles filter
        subtitle_filter = f"subtitles={temp_subtitle}:force_style='FontSize={font_size},MarginV={margin_v}'"

        cmd = [
            ffmpeg_path,
            '-i', temp_video,
            '-vf', subtitle_filter,
            '-c:a', 'copy',  # Copy audio directly, no re-encoding
            '-y',  # Overwrite output file
            temp_output
        ]

        print(f"   Executing FFmpeg...")
        print(f"   Command: {' '.join(cmd)}")

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
        if not Path(temp_output).exists():
            raise RuntimeError("Output file not created")

        # Move output file to target location
        print(f"   Moving output file...")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(temp_output, output_path)

        # Get file size
        output_size = output_path.stat().st_size
        print(f"✅ Subtitle burning complete")
        print(f"   Output file: {output_path}")
        print(f"   File size: {format_file_size(output_size)}")

        return str(output_path)

    finally:
        # Clean temporary directory
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"   Cleaning temporary directory")
        except Exception:
            pass


def main():
    """Command line entry point"""
    if len(sys.argv) < 4:
        print("Usage: python burn_subtitles.py <video> <subtitle> <output> [font_size] [margin_v]")
        print("\nArguments:")
        print("  video      - Input video file path")
        print("  subtitle   - Subtitle file path (SRT format)")
        print("  output     - Output video file path")
        print("  font_size  - Font size, default 24")
        print("  margin_v   - Bottom margin, default 30")
        print("\nExample:")
        print("  python burn_subtitles.py input.mp4 subtitle.srt output.mp4")
        print("  python burn_subtitles.py input.mp4 subtitle.srt output.mp4 28 40")
        sys.exit(1)

    video_path = sys.argv[1]
    subtitle_path = sys.argv[2]
    output_path = sys.argv[3]
    font_size = int(sys.argv[4]) if len(sys.argv) > 4 else 24
    margin_v = int(sys.argv[5]) if len(sys.argv) > 5 else 30

    try:
        result_path = burn_subtitles(
            video_path,
            subtitle_path,
            output_path,
            font_size=font_size,
            margin_v=margin_v
        )

        print(f"\n✨ Done! Output file: {result_path}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
