# Hidden Psyche — Content Studio

Claude Code project for the [Hidden Psyche](https://www.youtube.com/@hidden-psyche-5p) YouTube channel.
Automatically generate full video content packages using community marketing skills + custom YouTube skills.

---

## Quick Start

### Prerequisites

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
2. Clone this repo:
   ```bash
   git clone https://github.com/aidino/hidden-psyche-content-studio.git
   cd hidden-psyche-content-studio
   ```
3. Clone the marketing-skill community pack into this repo:
   ```bash
   git clone https://github.com/alirezarezvani/claude-skills.git
   # The marketing-skill folder will be at ./claude-skills/marketing-skill/
   ```
4. Launch Claude Code:
   ```bash
   claude
   ```

---

## Project Structure

```
hidden-psyche-content-studio/
├── CLAUDE.md                          # Agent instructions (auto-read by Claude Code)
├── README.md                          # This file
├── channel-context/
│   └── CHANNEL.md                     # Brand voice, audience, content pillars
├── skills/
│   └── youtube-content/
│       └── SKILL.md                   # Custom skill: full YouTube content package
├── output/                            # Generated content goes here
│   └── .gitkeep
└── claude-skills/                     # Community marketing skills (git cloned)
    └── marketing-skill/               # 43 marketing sub-skills
```

---

## How to Generate a Full Video Package

### Method 1 — Quick Command (Recommended)

In Claude Code, type:

```
create video package for topic: people who avoid conflict
```

then

```
write out to files in output folder with prefix mmdd_video_
```

Claude will automatically:
1. Load channel context from `channel-context/CHANNEL.md`
2. Load the custom YouTube skill from `.claude/skills/youtube-content/SKILL.md`
3. Output all 5 content pieces below

---

### What You Get (5 Outputs)

#### 1. Video Script
Full script with hook, intro, body sections, and outro.
Structured for ~7 minutes (medium length) by default.

Example structure:
```
[HOOK — 0:00–0:30]
Have you ever noticed how some people go completely silent when they're upset instead of talking it out?

[INTRO — 0:30–1:00]
Today we're looking at the psychology behind conflict avoidance...

[SECTION 1 — The Fawn Response]
...
```

---

#### 2. Clickable Title — "The Psychology of..." Formula

Claude generates **3 title variants** using the channel formula:

```
A) The Psychology of People Who Avoid Conflict  
B) The Psychology of Never Wanting to Argue  ⭐ (recommended)
C) The Psychology of People Who Keep the Peace
```

The ⭐ recommended option is optimized for CTR and search volume.

---

#### 3. SEO Description (YouTube-ready)

Humanized plain text, no markdown, 150–200 words.

Example output:
```
Some people will do almost anything to avoid an argument. They'll change the subject, apologize when they're not wrong, or simply go quiet. But why? And what does it cost them in the long run?

In this video we look at why conflict avoidance runs so deep for certain people — from childhood conditioning to the fawn trauma response. You'll understand how people-pleasing connects to anxiety, why silence feels safer than honesty, and the psychological patterns that keep conflict avoiders stuck in relationships that drain them.

We cover concepts like the fawn response, passive communication styles, and the link between low self-worth and boundary difficulties.

If any of this sounds familiar, leave a comment below — I'd love to hear your experience.

Hidden Psyche explores psychology in everyday life — subscribe for new videos every week.
```

---

#### 4. SEO Tags (comma-separated)

Example output:
```
psychology, conflict avoidance, hidden psyche, why people avoid conflict, fawn response, people pleasing psychology, conflict avoider personality, avoiding arguments, psychology of peace keeping, social anxiety, attachment styles, people pleaser, conflict avoidance in relationships, psychology explained, human behavior
```

Copy and paste directly into the YouTube tags field.

---

#### 5. Thumbnail Prompt

Ready-to-use prompt for image generation tools (Midjourney, DALL-E, Ideogram).

Example output:
```
Create a YouTube thumbnail in 16:9 ratio.
Video title: The Psychology of People Who Avoid Conflict
Style: White background, stickman character illustration.
Layout: Left half contains 2 lines of text.
Line 1: "Psychology of" — black text on white background, large bold font.
Line 2: "People Who Avoid Conflict" — white text on red background, slightly smaller font than Line 1.
Right half: A stickman illustration of a person backing away with hands raised in a "peace" gesture while another stickman approaches pointing a finger.
Overall feel: Clean, minimal, instantly readable at small thumbnail size.
```

Paste this into Midjourney (`/imagine`), Ideogram, or DALL-E 3.

---

## Using Individual Skills

You can also call specific skills for targeted tasks:

### Generate only a title
```
Using .claude/skills/youtube-content/SKILL.md, generate only the title variants for topic: overthinking before sleep
```

### Humanize existing text
```
Using claude-skills/marketing-skill/content-humanizer/SKILL.md, humanize this description: [paste your text]
```

### Generate a content calendar
```
Using claude-skills/marketing-skill/content-strategy/SKILL.md, create a 4-week content calendar for a psychology YouTube channel focused on dark psychology and personality types
```

### Write an SEO-optimized script
```
Using claude-skills/marketing-skill/content-production/SKILL.md and channel-context/CHANNEL.md, write a 7-minute script about the psychology of quiet people
```

---

## Skill Reference Table

| Task | Skill Location | Command Example |
|------|---------------|----------------|
| Full video package | `.claude/skills/youtube-content/SKILL.md` | `create video package for topic: X` |
| Script writing | `claude-skills/marketing-skill/content-production/SKILL.md` | `write script for topic: X` |
| Humanize description | `claude-skills/marketing-skill/content-humanizer/SKILL.md` | `humanize this text: [text]` |
| SEO optimization | `claude-skills/marketing-skill/ai-seo/SKILL.md` | `optimize SEO for: [title]` |
| Content calendar | `claude-skills/marketing-skill/content-strategy/SKILL.md` | `create 4-week calendar for psychology channel` |
| Video strategy | `claude-skills/marketing-skill/video-content-strategist/SKILL.md` | `analyze video strategy for psychology niche` |
| Social media posts | `claude-skills/marketing-skill/social-content/SKILL.md` | `create Shorts description for: [title]` |
| Psychology hooks | `claude-skills/marketing-skill/marketing-psychology/SKILL.md` | `generate psychological hooks for topic: X` |

---

## Saving Output

Ask Claude to save generated content:

```
create video package for topic: people who overthink everything, then save the output to output/overthinking.md
```

---

## Tips

- **Always provide a specific topic** — the more specific, the better the output. "quiet people" → OK. "people who go quiet when they're emotionally overwhelmed" → much better.
- **Review the 3 title variants** before picking. The ⭐ recommendation is a starting point, not a final answer.
- **Thumbnail prompt works best** with Ideogram (free) or Midjourney v6.
- **Humanizer skill** is your best friend for descriptions — run any AI-generated description through it before publishing.
- **Update CHANNEL.md** as your channel evolves — new content pillars, new audience data, new upload cadence.

---

## Adding New Custom Skills

1. Create a new folder under `.claude/skills/`:
   ```bash
   mkdir -p .claude/skills/shorts-repurpose
   touch .claude/skills/shorts-repurpose/SKILL.md
   ```
2. Write your skill instructions in `SKILL.md` (follow the format in `.claude/skills/youtube-content/SKILL.md`)
3. Add the new skill to the routing table in `CLAUDE.md`

---

## License

Custom skills in `.claude/skills/` are authored for this project.  
Community skills from `claude-skills/marketing-skill/` are from [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).
