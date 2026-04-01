---
name: "youtube-content"
description: "Full YouTube content package generator for the Hidden Psyche psychology channel. Given a topic, outputs all 5 production-ready assets: video script, clickable title (3 variants using 'The Psychology of...' formula), SEO description (plain text, humanized, no markdown), SEO tags (comma-separated), and thumbnail prompt (stickman style). Triggers: 'create video package', 'generate content for topic', 'write script for', 'make thumbnail prompt', 'generate YouTube SEO'. NOT for general blog writing (use content-production). NOT for social captions only (use social-content)."
license: MIT
metadata:
  version: 1.1.0
  author: Dino (aidino)
  category: youtube, content-creation
  channel: Hidden Psyche
  updated: 2026-04-01
---

# YouTube Content Skill — Hidden Psyche

## Purpose

Generate a complete YouTube content package for the Hidden Psyche channel given a topic.
Outputs: Script, Title, SEO Description, SEO Tags, Thumbnail Prompt.

---

## Inputs Required

```
topic: [string] — e.g., "people who hate small talk"
```

Optional:
```
tone: [educational | dark | philosophical]  (default: educational)
script_length: [short=3min | medium=7min | long=12min]  (default: medium)
```

---

## Output Format

Always output all 5 sections in this exact order:

### 1. VIDEO SCRIPT
### 2. CLICKABLE TITLE
### 3. SEO DESCRIPTION
### 4. SEO TAGS
### 5. THUMBNAIL PROMPT

---

## Section Rules

### 1. VIDEO SCRIPT

Structure:
```
[HOOK — 0:00–0:30]
Open with a provocative question or surprising fact related to the topic.
Example: "Have you ever noticed how some people seem physically uncomfortable during small talk?"

[INTRO — 0:30–1:00]
Briefly frame what psychology says about this topic.
Tease 3 key insights the viewer will learn.

[BODY — 1:00–end]
Divide into 3–5 clearly labeled sections.
Each section: insight name → explanation → real-world example → psychological backing

[OUTRO — last 60 seconds]
Summarize insights in 3 bullet points.
Call to action: "If this resonated with you, subscribe for more psychology explained simply."
```

Tone guidelines:
- Use second-person ("you") to create intimacy
- Short paragraphs, max 3 sentences per paragraph
- Avoid academic citations mid-script; save for description
- Use pauses: mark them as [PAUSE]

---

### 2. CLICKABLE TITLE

Formula: `The Psychology of [Topic]`

Rules:
- MUST use the formula above — no exceptions for Hidden Psyche
- 40–60 characters ideal
- Capitalize each main word
- The topic phrase must be specific enough to feel personal
- Generate 3 title variants, label them A / B / C
- Mark the recommended one with ⭐

Examples:
- The Psychology of People Who Hate Small Talk
- The Psychology of Always Feeling Behind in Life
- The Psychology of People Who Go Silent When Hurt

---

### 3. SEO DESCRIPTION

Rules:
- **NO markdown formatting** (no **, no ##, no bullet dashes)
- **Must sound human** — conversational, not keyword-stuffed
- Length: 150–200 words
- Structure (plain prose only):
  - Line 1–2: Hook sentence that mirrors the video's opening question
  - Lines 3–6: What the viewer will learn (written as natural sentences)
  - Lines 7–9: Brief note on the psychological concepts covered
  - Line 10: Soft CTA (subscribe, leave a comment)
  - Line 11–12: Channel description sentence
- Include 3–5 natural keyword phrases woven into the prose
- End with: "Hidden Psyche explores psychology in everyday life — subscribe for new videos every week."

---

### 4. SEO TAGS

Rules:
- 15–20 tags total
- Each tag separated by a comma
- Mix of: broad terms + specific phrases + channel brand terms
- Include: "psychology", "hidden psyche", and topic-specific tags
- No hashtags, no # symbol
- All lowercase

Format:
```
tag1, tag2, tag3, tag4, ...
```

---

### 5. THUMBNAIL PROMPT

Always use this exact template, filling in the bracketed variables:

```
Create a YouTube thumbnail in 16:9 ratio.
Video title: [FULL TITLE HERE]
Style: White background, stickman character illustration.
Layout: Left half contains 2 lines of text.
Line 1: "Psychology of" — black text on white background, large bold font.
Line 2: "[TOPIC SUBJECT]" — white text on red background, slightly smaller font than Line 1.
Right half: A stickman illustration depicting [BRIEF SCENE DESCRIPTION RELATED TO TOPIC].
Overall feel: Clean, minimal, instantly readable at small thumbnail size.
```

Fill in:
- `[FULL TITLE HERE]` — the recommended title from Section 2
- `[TOPIC SUBJECT]` — the subject part after "Psychology of" (e.g., "People Who Hate Small Talk")
- `[BRIEF SCENE DESCRIPTION]` — 1 sentence describing what the stickman is doing to represent the topic

---

## Example Output

For topic: `people who hate small talk`

**TITLE (recommended ⭐):** The Psychology of People Who Hate Small Talk

**THUMBNAIL PROMPT:**
```
Create a YouTube thumbnail in 16:9 ratio.
Video title: The Psychology of People Who Hate Small Talk
Style: White background, stickman character illustration.
Layout: Left half contains 2 lines of text.
Line 1: "Psychology of" — black text on white background, large bold font.
Line 2: "People Who Hate Small Talk" — white text on red background, slightly smaller font than Line 1.
Right half: A stickman illustration of a person standing alone at a party, arms crossed, while other stickmen chat in groups nearby.
Overall feel: Clean, minimal, instantly readable at small thumbnail size.
```

---

## Related Skills

- **content-production**: Use for long-form blog/article writing outside of YouTube scripts.
- **content-humanizer**: Run SEO description through this if it still sounds AI-generated.
- **marketing-psychology**: Use to generate additional psychological hooks and persuasion angles for the script.
- **social-content**: Use to repurpose the video script into Shorts descriptions or Instagram captions.
