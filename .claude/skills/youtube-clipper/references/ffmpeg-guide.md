# FFmpeg Usage Guide

FFmpeg is a powerful multimedia processing tool. This document introduces the core commands used in the YouTube Clipper.

## Installation

### macOS
```bash
# Standard version (does not support subtitle burning)
brew install ffmpeg

# Full version (Recommended, supports subtitle burning)
brew install ffmpeg-full
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install ffmpeg libass-dev
```

### Verify Installation
```bash
# Check version
ffmpeg -version

# Check libass support (required for burning subtitles)
ffmpeg -filters 2>&1 | grep subtitles
```

## Common Commands

### 1. Clip Video

```bash
# Precise clipping (starts at 30 seconds, lasts for 60 seconds)
ffmpeg -ss 30 -i input.mp4 -t 60 -c copy output.mp4

# From 01:30:00 to 01:33:15
ffmpeg -ss 01:30:00 -i input.mp4 -to 01:33:15 -c copy output.mp4
```

**Parameters:**
- `-ss`: Start time
- `-i`: Input file
- `-t`: Duration
- `-to`: End time
- `-c copy`: Direct stream copy, no re-encoding (fast and lossless)

### 2. Burn Subtitles

```bash
# Burn SRT subtitles to video
ffmpeg -i input.mp4 \
  -vf "subtitles=subtitle.srt" \
  -c:a copy \
  output.mp4

# Custom subtitle styling
ffmpeg -i input.mp4 \
  -vf "subtitles=subtitle.srt:force_style='FontSize=24,MarginV=30'" \
  -c:a copy \
  output.mp4
```

**Note:**
- Requires libass support
- Paths cannot contain spaces (use a temporary directory to solve)
- Video will be re-encoded (slower than clipping)

### 3. Video Compression

```bash
# Compress using H.264
ffmpeg -i input.mp4 \
  -c:v libx264 \
  -crf 23 \
  -c:a aac \
  output.mp4
```

**CRF Values:**
- 18: High quality, larger file size
- 23: Balanced (Recommended)
- 28: Low quality, smaller file size

### 4. Extract Audio

```bash
# Extract as MP3
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3

# Extract as AAC
ffmpeg -i input.mp4 -vn -c:a copy output.aac
```

### 5. Video Information

```bash
# View detailed video properties
ffmpeg -i input.mp4

# View concise information
ffprobe -v error -show_format -show_streams input.mp4
```

## Subtitles

### Burning Bilingual Subtitles

```bash
# Bilingual subtitles (each subtitle entry contains two lines)
ffmpeg -i input.mp4 \
  -vf "subtitles=bilingual.srt:force_style='FontSize=24,MarginV=30'" \
  -c:a copy \
  output.mp4
```

### Adjusting Subtitle Styles

Available style options:
- `FontSize`: Font size (20-28 recommended)
- `MarginV`: Vertical margin (20-40 recommended)
- `FontName`: Font name
- `PrimaryColour`: Primary color
- `OutlineColour`: Outline color
- `Bold`: Bold (0 or 1)

Example:
```bash
subtitles=subtitle.srt:force_style='FontSize=28,MarginV=40,Bold=1'
```

## Performance Optimization

### Hardware Acceleration

```bash
# macOS (VideoToolbox)
ffmpeg -hwaccel videotoolbox -i input.mp4 ...

# NVIDIA GPU
ffmpeg -hwaccel cuda -i input.mp4 ...
```

### Multi-threading

```bash
# Use 4 threads
ffmpeg -threads 4 -i input.mp4 ...
```

## Frequently Asked Questions

### Q: Subtitle burning fails, error "No such filter: 'subtitles'"

A: Your FFmpeg version lacks libass support. On macOS, you need to install `ffmpeg-full`.

### Q: Subtitle burning fails because paths have spaces

A: Use a temporary directory. Copy the files to a space-free path before processing.

### Q: Video quality dropped

A: Use `-c copy` for direct stream copying, or lower the CRF value (e.g. 18).

### Q: Processing speed is slow

A:
- Use hardware acceleration (`-hwaccel`)
- Use `-c copy` when clipping
- Increase thread count (`-threads`)

## Reference Links

- [FFmpeg Official Documentation](https://ffmpeg.org/documentation.html)
- [FFmpeg Wiki](https://trac.ffmpeg.org/wiki)
- [Subtitles Filter Documentation](https://ffmpeg.org/ffmpeg-filters.html#subtitles)
