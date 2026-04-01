# Hidden Psyche — Claude Code Agent Instructions

## Channel Identity

- **Channel**: [Hidden Psyche](https://www.youtube.com/@hidden-psyche-5p)
- **Niche**: Psychology, human behavior, dark psychology, social dynamics
- **Style**: Educational, thought-provoking, accessible to general audience
- **Visual Identity**: Stickman illustrations, white background, clean minimalist design
- **Title Formula**: `The Psychology of ...`

---

## How to Use This Project

### Skill Loading Order (ALWAYS follow this)

1. **Read `channel-context/CHANNEL.md`** first — it has brand voice, audience persona, and content pillars
2. **Read `marketing-skill/marketing-ops/SKILL.md`** to route to the right marketing sub-skill
3. **Load ONE specialist skill** from `skills/` or from `marketing-skill/` as needed

> ❌ Never bulk-load all skill files  
> ❌ Never skip channel-context  
> ✅ Always load only what the task requires

---

## Skill Map

### From `marketing-skill/` (Community)

| Task | Skill to Load |
|------|---------------|
| Content strategy & planning | `marketing-skill/content-strategy/SKILL.md` |
| Write/edit script | `marketing-skill/content-production/SKILL.md` |
| Humanize AI-written text | `marketing-skill/content-humanizer/SKILL.md` |
| SEO optimization | `marketing-skill/ai-seo/SKILL.md` |
| Social media (Shorts, IG) | `marketing-skill/social-content/SKILL.md` |
| Video strategy | `marketing-skill/video-content-strategist/SKILL.md` |
| Marketing psychology hooks | `marketing-skill/marketing-psychology/SKILL.md` |

### From `skills/` (Custom — this project)

| Task | Skill to Load |
|------|---------------|
| Full YouTube content package | `.claude/skills/youtube-content/SKILL.md` |
| Thumbnail prompt generation | `.claude/skills/youtube-content/SKILL.md` |
| Title generation (Psychology formula) | `.claude/skills/youtube-content/SKILL.md` |
| SEO description (humanized, no markdown) | `.claude/skills/youtube-content/SKILL.md` |
| SEO tags (comma-separated) | `.claude/skills/youtube-content/SKILL.md` |

---

## Core Workflow: One Video Package

When the user provides a **topic**, execute in this order:

```
1. Load channel-context/CHANNEL.md
2. Load .claude/skills/youtube-content/SKILL.md
3. Generate: Script → Title → Description → Tags → Thumbnail Prompt
4. Output each section clearly labeled
```

**Quick command the user can type:**
```
create video package for topic: [TOPIC]
```

---

## Anti-Patterns

❌ Don't use markdown formatting in YouTube descriptions  
❌ Don't make descriptions sound robotic or keyword-stuffed  
❌ Don't use clickbait titles unrelated to content  
❌ Don't skip the thumbnail prompt — it's part of every package  
❌ Don't bulk-load all skills at once  
