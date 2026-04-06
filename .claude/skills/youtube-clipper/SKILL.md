---
name: youtube-clipper
description: >
  YouTube video intelligent clipping tool. Downloads video and subtitles, uses AI to generate fine-grained chapters (minutes level), and when the user selects a segment, automatically clips the video, translates subtitles to bilingual (English/Target), burns subtitles into the video, and generates a summary copy.
  Use Cases: When users need to clip YouTube videos, generate short video segments, or create bilingual subtitle versions.
  Keywords: video clipping, YouTube, subtitle translation, bilingual subtitles, video download, clip video
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
model: claude-sonnet-4-5-20250514
---

# YouTube Video Intelligent Clipping Tool

> **Installation**: If you're installing this skill from GitHub, please refer to [README.md](README.md#installation) for installation instructions. The recommended method is `npx skills add https://github.com/op7418/Youtube-clipper-skill`.

## Workflow

You will execute the YouTube video clipping task following these 6 phases:

### Phase 1: Environment Check

**Goal**: Ensure all required tools and dependencies are installed

1. Check if yt-dlp is available
   ```bash
   yt-dlp --version
   ```

2. Check FFmpeg version and libass support
   ```bash
   # Priority check for ffmpeg-full (macOS)
   /opt/homebrew/opt/ffmpeg-full/bin/ffmpeg -version

   # Check standard FFmpeg
   ffmpeg -version

   # Verify libass support (required for burning subtitles)
   ffmpeg -filters 2>&1 | grep subtitles
   ```

3. Check Python dependencies
   ```bash
   python3 -c "import yt_dlp; print('✅ yt-dlp available')"
   python3 -c "import pysrt; print('✅ pysrt available')"
   ```

**If environment check fails**:
- yt-dlp not installed: Prompt `brew install yt-dlp` or `pip install yt-dlp`
- FFmpeg missing libass: Prompt to install ffmpeg-full
  ```bash
  brew install ffmpeg-full  # macOS
  ```
- Missing Python dependencies: Prompt `pip install pysrt python-dotenv`

**Note**:
- Standard Homebrew FFmpeg does not include libass and cannot burn subtitles.
- ffmpeg-full path: `/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg` (Apple Silicon)
- You must pass the environment check before continuing.

---

### Phase 2: Download Video

**Goal**: Download YouTube video and English subtitles

1. Ask user for the YouTube URL

2. Call the download_video.py script
   ```bash
   cd ~/.claude/skills/youtube-clipper
   python3 scripts/download_video.py <youtube_url>
   ```

3. The script will:
   - Download video (up to 1080p, mp4 format)
   - Download English subtitles (VTT format, auto-generated subtitles as fallback)
   - Output file paths and video information

4. Display to the user:
   - Video title
   - Video duration
   - File size
   - Download path

**Outputs**:
- Video file: `<id>.mp4` (Named using video ID to avoid special character issues)
- Subtitle file: `<id>.en.vtt`

---

### Phase 3: Analyze Chapters (Core Differentiating Feature)

**Goal**: Use Claude AI to analyze subtitle content and generate fine-grained chapters (2-5 minutes scale)

1. Call analyze_subtitles.py to parse the VTT subtitles
   ```bash
   python3 scripts/analyze_subtitles.py <subtitle_path>
   ```

2. The script outputs structured subtitle data:
   - Full subtitle text (with timestamps)
   - Total duration
   - Subtitle count

3. **You must perform the AI analysis** (This is the most critical step):
   - Read the complete subtitle content
   - Understand the semantics and topic transition points
   - Identify natural conversation switching points
   - Generate chapters at a 2-5 minute granularity (avoid coarse 30-minute splitting)

4. Generate for each chapter:
   - **Title**: Concise topic summary (10-20 words)
   - **Time Range**: Start and end time (Format: MM:SS or HH:MM:SS)
   - **Core Summary**: 1-2 sentences explaining what this segment is about (50-100 words)
   - **Keywords**: 3-5 core concept words

5. **Chapter Generation Principles**:
   - Granularity: 2-5 minutes per chapter (avoid being too short or too long)
   - Completeness: Ensure all video content is covered without omissions
   - Meaningfulness: Each chapter is a relatively independent topic
   - Natural splitting: Cut at topic transition points, do not split mechanically by time

6. Display the chapter list to the user:
   ```
   📊 Analysis complete, generated X chapters:

   1. [00:00 - 03:15] AGI is an exponential curve, not a point in time
      Core: AI model capabilities double every 4-12 months, engineers use Claude to code
      Keywords: AGI, Exponential Growth, Claude Code

   2. [03:15 - 06:30] China's gap in AI
      Core: Chip embargo affects China, DeepSeek benchmark optimization doesn't reflect full power
      Keywords: China, Chip Embargo, DeepSeek

   ... (All chapters)

   ✓ All content covered, no omissions
   ```

---

### Phase 4: User Selection

**Goal**: Let the user select the chapters to clip and processing options

1. Use AskUserQuestion tool to let the user select chapters
   - Provide chapter numbers for user selection
   - Support multiple selections

2. Ask for processing options:
   - Generate bilingual subtitles? (English + Target language)
   - Burn subtitles into video? (Hardcoded subtitles)
   - Generate summary copy?

3. Confirm user choices and display the processing plan

---

### Phase 5: Processing & Clipping (Core Execution Phase)

**Goal**: Execute multiple processing tasks concurrently

For each chapter selected by the user, execute the following steps:

#### 5.1 Clip Video Segment
```bash
python3 scripts/clip_video.py <video_path> <start_time> <end_time> <output_path>
```
- Use FFmpeg for precise clipping
- Maintain original video quality
- Output: `<Chapter_Title>_clip.mp4`

#### 5.2 Extract Subtitle Segment
- Filter subtitles to only include the specific time range
- Adjust timestamps (subtract start time so it starts from 00:00:00)
- Convert to SRT format
- Output: `<Chapter_Title>_original.srt`

#### 5.3 Translate Subtitles (If chosen by user)
```bash
python3 scripts/translate_subtitles.py <subtitle_path>
```
- **Batch translation optimization**: Translate 20 subtitles per batch together (saves 95% API calls)
- Translation strategy:
  - Maintain accuracy of technical terms
  - Conversational tone (suitable for short videos)
  - Concise and fluent (avoid verbosity)
- Output: `<Chapter_Title>_translated.srt`

#### 5.4 Generate Bilingual Subtitle File (If chosen by user)
- Merge English and Target subtitles
- Format: SRT Bilingual (each subtitle contains English and Target language)
- Style: English on top, Target on bottom
- Output: `<Chapter_Title>_bilingual.srt`

#### 5.5 Burn Subtitles Into Video (If chosen by user)
```bash
python3 scripts/burn_subtitles.py <video_path> <subtitle_path> <output_path>
```
- Use ffmpeg-full (with libass support)
- **Use temporary directory to solve path space issues** (Crucial!)
- Subtitle style:
  - Font size: 24
  - Bottom margin: 30
  - Color: White text + Black outline
- Output: `<Chapter_Title>_with_subtitles.mp4`

#### 5.6 Generate Summary Copy (If chosen by user)
```bash
python3 scripts/generate_summary.py <chapter_info>
```
- Based on chapter title, summary and keywords
- Generate social media ready copy
- Includes: Title, Core Points, Platform Versions (Xiaohongshu, Douyin, etc.)
- Output: `<Chapter_Title>_summary.md`

**Progress Display**:
```
🎬 Starting processing chapter 1/3: AGI is an exponential curve...

1/6 Clipping video segment... ✅
2/6 Extracting subtitle segment... ✅
3/6 Translating subtitles... [=====>    ] 50% (26/52)
4/6 Generating bilingual subtitles... ✅
5/6 Burning subtitles to video... ✅
6/6 Generating summary... ✅

✨ Chapter 1 processing complete
```

---

### Phase 6: Output Results

**Goal**: Organize output files and display them to the user

1. Create output directory
   ```
   ./youtube-clips/<Datetime>/
   ```
   The output directory is located in the current working directory.

2. Organize file structure:
   ```
   <Chapter_Title>/
   ├── <Chapter_Title>_clip.mp4              # Original clip (no subtitles)
   ├── <Chapter_Title>_with_subtitles.mp4   # Burned subtitles version
   ├── <Chapter_Title>_bilingual.srt        # Bilingual subtitle file
   └── <Chapter_Title>_summary.md           # Summary copy
   ```

3. Display to user:
   - Output directory path
   - File list (with file sizes)
   - Quick preview commands

   ```
   ✨ Processing complete!

   📁 Output Directory: ./youtube-clips/20260121_143022/

   File List:
     🎬 AGI_Exponential_Curve_with_subtitles.mp4 (14 MB)
     📄 AGI_Exponential_Curve_bilingual.srt (2.3 KB)
     📝 AGI_Exponential_Curve_summary.md (3.2 KB)

   Quick Preview:
   open ./youtube-clips/20260121_143022/AGI_Exponential_Curve_with_subtitles.mp4
   ```

4. Ask if they want to clip other chapters
   - If yes, return to Phase 4 (User Selection)
   - If no, end Skill execution

---

## Technical Details

### 1. FFmpeg Path Space Issue
**Problem**: FFmpeg subtitles filter fails to parse paths containing spaces

**Solution**: burn_subtitles.py uses a temporary directory
- Create a temporary directory without spaces
- Copy files to the temporary directory
- Execute FFmpeg
- Move the output file back to the original destination

### 2. Batch Translation Optimization
**Problem**: Translating subtitle-by-subtitle generates too many API calls

**Solution**: Translate 20 subtitles together per batch
- Saves 95% of API calls
- Increases translation speed
- Maintains contextual translation consistency

### 3. Chapter Analysis Granularity
**Goal**: Generate chapters at a 2-5 minute granularity, avoid 30-minute coarse splitting.

**Method**:
- Understand subtitle semantics to identify topic transitions
- Look for natural conversation switching points
- Ensure each chapter contains a complete discussion
- Do not split mechanically by time

### 4. FFmpeg vs ffmpeg-full
**Difference**:
- Standard FFmpeg: Lacks libass support, cannot burn subtitles
- ffmpeg-full: Includes libass, supports burning subtitles

**Paths**:
- Standard: `/opt/homebrew/bin/ffmpeg`
- ffmpeg-full: `/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg` (Apple Silicon)

---

## Error Handling

### Environment Issues
- Missing tools → Prompt installation command
- FFmpeg missing libass → Recommend ffmpeg-full installation
- Missing Python dependencies → Prompt pip install

### Download Issues
- Invalid URL → Ask user to check URL format
- Missing subtitles → Attempt to fetch automatic subtitles
- Network error → Prompt to retry

### Processing Issues
- FFmpeg execution failed → Display detailed error info
- Translation failed → Retry mechanism (up to 3 times)
- Insufficient disk space → Prompt to clear space

---

## Output File Naming Convention

- Video segment: `<Chapter_Title>_clip.mp4`
- Subtitle file: `<Chapter_Title>_bilingual.srt`
- Burned version: `<Chapter_Title>_with_subtitles.mp4`
- Summary copy: `<Chapter_Title>_summary.md`

**Filename Sanitization**:
- Remove special characters (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`)
- Replace spaces with underscores
- Restrict length (Max 100 characters)

---

## User Experience Focus

1. **Progress Visibility**: Display progress and status for every step
2. **Error Friendliness**: Clear error messages and actionable solutions
3. **Controllability**: Let the user choose which chapters to clip and processing options
4. **High Quality**: Meaningful chapter analysis, accurate and fluent translations
5. **Completeness**: Provide original and processed versions of the output files

---

## Execution Launch

When the user triggers this Skill:
1. Immediately begin Phase 1 (Environment Check)
2. Follow the 6 phases sequentially
3. Automatically move to the next phase after completing the current one
4. Provide clear solutions when encountering problems
5. Output the complete results at the end

Remember: The core value of this Skill lies in its **fine-grained AI chapter analysis** and **seamless technical processing**, allowing users to quickly extract high-quality short video segments from long-form content.
