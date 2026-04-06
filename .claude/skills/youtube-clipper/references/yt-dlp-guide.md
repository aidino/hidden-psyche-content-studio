# yt-dlp Usage Guide

yt-dlp is a powerful YouTube video download tool. This document introduces the core functionalities used in the YouTube Clipper.

## Installation

### macOS
```bash
brew install yt-dlp
```

### Linux
```bash
# Ubuntu/Debian
sudo apt-get install yt-dlp

# Or use pip
pip install yt-dlp
```

### Update
```bash
# Homebrew
brew upgrade yt-dlp

# pip
pip install --upgrade yt-dlp
```

## Basic Usage

### Download Video

```bash
# Download best quality
yt-dlp https://youtube.com/watch?v=VIDEO_ID

# Specify format
yt-dlp -f "best[ext=mp4]" URL

# Limit resolution (max 1080p)
yt-dlp -f "bestvideo[height<=1080]+bestaudio" URL
```

### Download Subtitles

```bash
# Download English subtitles
yt-dlp --write-sub --sub-lang en URL

# Download auto-generated subtitles (fallback if no manual subtitles)
yt-dlp --write-auto-sub --sub-lang en URL

# Download all available subtitles
yt-dlp --write-sub --all-subs URL

# Specify subtitle format (VTT, SRT, etc.)
yt-dlp --write-sub --sub-format vtt URL
```

## Configuration Used in YouTube Clipper

### Full Configuration

```python
ydl_opts = {
    # Video format: max 1080p, prefer mp4
    'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',

    # Output template
    'outtmpl': '%(title)s [%(id)s].%(ext)s',

    # Download subtitles
    'writesubtitles': True,
    'writeautomaticsub': True,  # Auto-generated subtitles as fallback
    'subtitleslangs': ['en'],   # English subtitles
    'subtitlesformat': 'vtt',   # VTT format

    # Don't download thumbnails
    'writethumbnail': False,
}
```

### Format String Explanation

```
bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best
│         │              │        │         │       │                           │
│         │              │        │         │       │                           └─ Final fallback
│         │              │        │         │       └─ Fallback: Best 1080p mp4
│         │              │        │         └─ Best audio (m4a)
│         │              │        └─ Merge
│         │              └─ Prefer mp4 format
│         └─ Max 1080p
└─ Best video quality
```

### Why limit to 1080p?

1. **File Size**: 4K videos can reach 5-10GB
2. **Processing Speed**: FFmpeg processing takes too long
3. **Actual Needs**: Short video platforms are primarily 1080p
4. **Storage Space**: Saves disk space

## Common Commands

### 1. View Video Information

```bash
# Don't download, only display info
yt-dlp --print-json URL

# View available formats
yt-dlp -F URL
```

### 2. Download Playlists

```bash
# Download the whole playlist
yt-dlp PLAYLIST_URL

# Download specific items only (1-5)
yt-dlp --playlist-items 1-5 PLAYLIST_URL

# Don't download playlist, only the current video
yt-dlp --no-playlist URL
```

### 3. Proxy Settings

```bash
# HTTP proxy
yt-dlp --proxy http://proxy:port URL

# SOCKS5 proxy
yt-dlp --proxy socks5://proxy:port URL
```

### 4. Rate Limiting

```bash
# Limit download speed to 50KB/s
yt-dlp --rate-limit 50K URL

# Limit to 4.2MB/s
yt-dlp --rate-limit 4.2M URL
```

### 5. Custom Filenames

```bash
# Use template
yt-dlp -o "%(title)s.%(ext)s" URL

# Include upload date
yt-dlp -o "%(upload_date)s - %(title)s.%(ext)s" URL

# Include channel name
yt-dlp -o "%(channel)s/%(title)s.%(ext)s" URL
```

## Subtitles

### Subtitle Language Codes

Common language codes:
- `en`: English
- `zh-Hans`: Simplified Chinese
- `zh-Hant`: Traditional Chinese
- `ja`: Japanese
- `ko`: Korean
- `es`: Spanish
- `fr`: French
- `de`: German

### View Available Subtitles

```bash
# List all available subtitles
yt-dlp --list-subs URL
```

### Subtitle Formats

```bash
# VTT format (Recommended for compatibility)
yt-dlp --write-sub --sub-format vtt URL

# SRT format
yt-dlp --write-sub --sub-format srt URL

# Multiple formats
yt-dlp --write-sub --sub-format "vtt,srt" URL
```

## Python API Usage

### Basic Example

```python
import yt_dlp

ydl_opts = {
    'format': 'best',
    'outtmpl': '%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://youtube.com/watch?v=VIDEO_ID'])
```

### Getting Video Info

```python
import yt_dlp

ydl_opts = {}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)

    print(f"Title: {info['title']}")
    print(f"Duration: {info['duration']} seconds")
    print(f"Uploader: {info['uploader']}")
```

### Progress Hook

```python
def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d['downloaded_bytes'] / d['total_bytes'] * 100
        print(f"Progress: {percent:.1f}%")
    elif d['status'] == 'finished':
        print("Download complete!")

ydl_opts = {
    'progress_hooks': [progress_hook],
}
```

## Frequently Asked Questions

### Q: Download fails, error "Video unavailable"

A: Possible causes:
- Video has been deleted or is private
- Region restriction (try using a proxy)
- Login required (use the `--cookies` option)

### Q: Subtitle download fails

A: Try:
1. Using `--write-auto-sub` (auto-generated subtitles)
2. using `--list-subs` to view available subtitles
3. Note that some videos simply don't have subtitles

### Q: Download speed is slow

A: Solutions:
- Use a proxy
- Check your network connection
- YouTube might be rate-limiting (wait and retry later)

### Q: Filename contains invalid characters

A: Clean it up using the output template:
```bash
yt-dlp -o "%(title).100s.%(ext)s" URL
# .100s limits the title length to 100 characters
```

### Q: How to download member-only videos?

A: Use browser cookies:
```bash
# Export browser cookies
yt-dlp --cookies-from-browser chrome URL

# Or use a cookies file
yt-dlp --cookies cookies.txt URL
```

## Advanced Usage

### Batch Downloading

```bash
# Read URL list from a file
yt-dlp -a urls.txt

# urls.txt content:
# https://youtube.com/watch?v=VIDEO1
# https://youtube.com/watch?v=VIDEO2
# https://youtube.com/watch?v=VIDEO3
```

### Post-Processing

```bash
# Transform to MP3 after downloading
yt-dlp -x --audio-format mp3 URL

# Embed subtitles after downloading
yt-dlp --embed-subs URL

# Embed thumbnails after downloading
yt-dlp --embed-thumbnail URL
```

### Archive Options

```bash
# Skip already downloaded videos
yt-dlp --download-archive archive.txt PLAYLIST_URL

# archive.txt records the downloaded video IDs
```

## Supported Websites

yt-dlp supports not only YouTube, but also:
- Vimeo
- Twitter
- TikTok
- Bilibili
- And 1000+ other websites

To view the full list:
```bash
yt-dlp --list-extractors
```

## Reference Links

- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp#readme)
- [Format Selection Notes](https://github.com/yt-dlp/yt-dlp#format-selection)
