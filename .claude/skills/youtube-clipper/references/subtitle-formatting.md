# Subtitle Formatting Guide

This document introduces the subtitle formats used in YouTube Clipper and how to convert between them.

## Supported Formats

### 1. VTT (WebVTT)

WebVTT is the standard subtitle format for web video.

#### Format Example

```vtt
WEBVTT

1
00:00:00.000 --> 00:00:03.500
This is the first subtitle

2
00:00:03.500 --> 00:00:07.000
This is the second subtitle
```

#### Characteristics
- The header must be `WEBVTT`
- Timestamps use a period (`.`) to separate milliseconds
- Supports styling and positioning information
- The default subtitle format for YouTube

#### Full Example

```vtt
WEBVTT

STYLE
::cue {
  background-color: rgba(0,0,0,0.8);
  color: white;
}

1
00:00:00.000 --> 00:00:03.500 align:start position:0%
<v Speaker>This is the first subtitle</v>

NOTE This is a comment

2
00:00:03.500 --> 00:00:07.000
This is the second subtitle
with multiple lines
```

---

### 2. SRT (SubRip)

SRT is the most commonly used subtitle format, offering excellent compatibility.

#### Format Example

```srt
1
00:00:00,000 --> 00:00:03,500
This is the first subtitle

2
00:00:03,500 --> 00:00:07,000
This is the second subtitle
```

#### Characteristics
- No header
- Timestamps use a comma (`,`) to separate milliseconds
- Does not support styling natively (but FFmpeg can override)
- Best compatibility across players

#### Multiline Text

```srt
1
00:00:00,000 --> 00:00:03,500
This is the first line
This is the second line
This is the third line

2
00:00:03,500 --> 00:00:07,000
Single line subtitle
```

---

## VTT vs SRT Comparison

| Feature | VTT | SRT |
|---------|-----|-----|
| Header | Required (`WEBVTT`) | None |
| Millisecond Separator | Period (`.`) | Comma (`,`) |
| Style Support | Yes | No |
| Position Control | Yes | No |
| Comment Support | Yes | No |
| Compatibility | Web | Universal |

---

## Format Conversion

### VTT → SRT

#### Python Implementation

```python
import re

def vtt_to_srt(vtt_content):
    # 1. Remove WEBVTT header
    srt_content = re.sub(r'^WEBVTT.*?\n\n', '', vtt_content, flags=re.DOTALL)

    # 2. Remove style information
    srt_content = re.sub(r'STYLE.*?\n\n', '', srt_content, flags=re.DOTALL)

    # 3. Remove NOTEs
    srt_content = re.sub(r'NOTE.*?\n\n', '', srt_content, flags=re.DOTALL)

    # 4. Convert timestamp separator: . → ,
    srt_content = re.sub(
        r'(\d{2}:\d{2}:\d{2})\.(\d{3})',
        r'\1,\2',
        srt_content
    )

    # 5. Remove position information
    srt_content = re.sub(
        r'(-->.*?)\s+(align|position|line|size):.*',
        r'\1',
        srt_content
    )

    # 6. Remove speaker tags <v Speaker>
    srt_content = re.sub(r'<v [^>]+>', '', srt_content)
    srt_content = re.sub(r'</v>', '', srt_content)

    return srt_content
```

#### Command Line Tools

```bash
# Using ffmpeg
ffmpeg -i input.vtt output.srt

# Using sed
sed 's/\./,/3' input.vtt > output.srt  # Simple conversion (incomplete)
```

### SRT → VTT

#### Python Implementation

```python
def srt_to_vtt(srt_content):
    # 1. Add WEBVTT header
    vtt_content = "WEBVTT\n\n" + srt_content

    # 2. Convert timestamp separator: , → .
    vtt_content = re.sub(
        r'(\d{2}:\d{2}:\d{2}),(\d{3})',
        r'\1.\2',
        vtt_content
    )

    return vtt_content
```

---

## Bilingual Subtitles

### SRT Format

Bilingual subtitles use multiline text in SRT:

```srt
1
00:00:00,000 --> 00:00:03,500
This is English subtitle
这是中文字幕

2
00:00:03,500 --> 00:00:07,000
Another English line
另一行中文
```

### Styling Recommendations

Styles when burning into a video:

```bash
ffmpeg -i video.mp4 \
  -vf "subtitles=bilingual.srt:force_style='FontSize=24,MarginV=30'" \
  output.mp4
```

Recommended parameters:
- `FontSize=24`: Suitable for 1080p videos
- `MarginV=30`: Bottom margin of 30 pixels
- English on top, Target Language on bottom

---

## Timestamp Formats

### Full Format

```
HH:MM:SS.mmm --> HH:MM:SS.mmm
```

- `HH`: Hours (00-99)
- `MM`: Minutes (00-59)
- `SS`: Seconds (00-59)
- `mmm`: Milliseconds (000-999)

### Examples

```
00:00:00.000  # 0 seconds
00:00:03.500  # 3.5 seconds
00:01:30.250  # 1 minute 30.25 seconds
01:23:45.678  # 1 hour 23 minutes 45.678 seconds
```

### Caveats

1. The hours portion is occasionally optional, but highly recommended for compatibility.
2. VTT uses period (`.`), SRT uses comma (`,`).
3. Milliseconds must be exactly 3 digits (zero-padded if necessary).

---

## Time Adjustment

### Scenario: Adjusting Subtitles After Video Clipping

After clipping the video segment from 02:00-02:10, subtitle timestamps need to be adjusted:

#### Original Subtitles

```srt
1
00:02:00,000 --> 00:02:03,500
First subtitle

2
00:02:03,500 --> 00:02:07,000
Second subtitle
```

#### Adjusted Subtitles

```srt
1
00:00:00,000 --> 00:00:03,500
First subtitle

2
00:00:03,500 --> 00:00:07,000
Second subtitle
```

#### Python Implementation

```python
def adjust_subtitle_time(subtitles, offset_seconds):
    """
    Adjust subtitle timestamp

    Args:
        subtitles: List of subtitles
        offset_seconds: Offset amount in seconds (i.e. clip start time)

    Returns:
        List of adjusted subtitles
    """
    adjusted = []

    for sub in subtitles:
        adjusted_sub = {
            'start': max(0, sub['start'] - offset_seconds),
            'end': max(0, sub['end'] - offset_seconds),
            'text': sub['text']
        }

        # Keep subtitles that end after 0
        if adjusted_sub['end'] > 0:
            adjusted.append(adjusted_sub)

    return adjusted
```

---

## Subtitle Encoding

### Recommended Encoding

**UTF-8** (Without BOM)

### Check Encoding

```bash
file -i subtitle.srt
# Output: subtitle.srt: text/plain; charset=utf-8
```

### Convert Encoding

```bash
# GBK → UTF-8
iconv -f GBK -t UTF-8 input.srt > output.srt

# Remove BOM
sed -i '1s/^\xEF\xBB\xBF//' subtitle.srt
```

---

## Subtitle Validation

### Check List

1. **Timestamp Format**: Does it comply with specifications?
2. **Time Sequence**: Start time < End time?
3. **Overlap Detection**: Do adjacent subtitles overlap?
4. **Encoding Check**: Is it UTF-8?
5. **Blank Lines**: Are there blank lines separating subtitle blocks?

### Python Validation Script

```python
def validate_srt(srt_path):
    errors = []

    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split subtitle blocks
    blocks = content.strip().split('\n\n')

    prev_end_time = 0

    for i, block in enumerate(blocks):
        lines = block.split('\n')

        if len(lines) < 3:
            errors.append(f"Block {i+1}: Invalid format (< 3 lines)")
            continue

        # Check sequence
        try:
            seq = int(lines[0])
            if seq != i + 1:
                errors.append(f"Block {i+1}: Invalid sequence number ({seq})")
        except ValueError:
            errors.append(f"Block {i+1}: Invalid sequence number")

        # Check timestamp
        timestamp_pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})'
        match = re.match(timestamp_pattern, lines[1])

        if not match:
            errors.append(f"Block {i+1}: Invalid timestamp format")
            continue

        start_str, end_str = match.groups()
        start_time = time_to_seconds(start_str)
        end_time = time_to_seconds(end_str)

        # Check time logic
        if start_time >= end_time:
            errors.append(f"Block {i+1}: Start time >= End time")

        if start_time < prev_end_time:
            errors.append(f"Block {i+1}: Overlaps with previous subtitle")

        prev_end_time = end_time

    return errors
```

---

## Frequently Asked Questions

### Q: FFmpeg fails to read subtitles, prompting encoding errors

A: Ensure the subtitle is UTF-8 encoded, without a BOM:
```bash
iconv -f GBK -t UTF-8 input.srt > output.srt
sed -i '1s/^\xEF\xBB\xBF//' output.srt
```

### Q: Subtitles display as garbled characters

A: Check your encoding:
```bash
file -i subtitle.srt
# If not UTF-8, convert the encoding
```

### Q: VTT subtitles do not display in certain media players

A: Try converting them to SRT format for better compatibility.

### Q: Characters in bilingual subtitles are too crowded

A: Increase the font size and margins:
```bash
subtitles=sub.srt:force_style='FontSize=28,MarginV=40'
```

---

## Reference Links

- [WebVTT Specification](https://www.w3.org/TR/webvtt1/)
- [SRT Format Description](https://en.wikipedia.org/wiki/SubRip)
- [FFmpeg Subtitles Filter](https://ffmpeg.org/ffmpeg-filters.html#subtitles)
