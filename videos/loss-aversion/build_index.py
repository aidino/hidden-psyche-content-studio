import json
import os

with open('transcript.json', 'r') as f:
    transcript = json.load(f)

# Group words (3 words per group)
groups = []
current_group = []
for i, word in enumerate(transcript):
    current_group.append(word)
    if len(current_group) >= 3 or i == len(transcript) - 1:
        groups.append({
            "text": " ".join([w["text"] for w in current_group]),
            "start": current_group[0]["start"],
            "end": current_group[-1]["end"],
            "words": current_group
        })
        current_group = []

# Generate group divs and animation script
html_groups = ""
gsap_logic = ""
total_duration = transcript[-1]["end"] + 1

# Generate background logic
bg_logic = ""
bg_1_start = 0.0
bg_1_end = groups[5]["start"]
bg_2_start = groups[5]["start"]
bg_2_end = groups[11]["start"]
bg_3_start = groups[11]["start"]
bg_3_end = groups[20]["start"]
bg_4_start = groups[20]["start"]
bg_4_end = total_duration

bg_logic += f'      tl.to("#bg-1", {{ opacity: 0.4, duration: 1 }}, {bg_1_start:.2f});\n'
bg_logic += f'      tl.to("#bg-1", {{ opacity: 0, duration: 1 }}, {bg_1_end - 1:.2f});\n'

bg_logic += f'      tl.to("#bg-2", {{ opacity: 0.4, duration: 1 }}, {bg_2_start:.2f});\n'
bg_logic += f'      tl.to("#bg-2", {{ opacity: 0, duration: 1 }}, {bg_2_end - 1:.2f});\n'

bg_logic += f'      tl.to("#bg-3", {{ opacity: 0.4, duration: 1 }}, {bg_3_start:.2f});\n'
bg_logic += f'      tl.to("#bg-3", {{ opacity: 0, duration: 1 }}, {bg_3_end - 1:.2f});\n'

bg_logic += f'      tl.to("#bg-4", {{ opacity: 0.4, duration: 1 }}, {bg_4_start:.2f});\n'
bg_logic += f'      tl.to("#bg-4", {{ opacity: 0, duration: 1 }}, {bg_4_end - 1:.2f});\n'

for i, group in enumerate(groups):
    # Determine highlight words
    html_groups += f'    <div id="cg-{i}" class="caption-group" style="visibility: hidden; position: absolute; width: 100%; text-align: center; top: 50%; transform: translateY(-50%);">\n'
    for j, word in enumerate(group["words"]):
        text = word["text"]
        color_class = ""
        lower = text.lower()
        if any(bad in lower for bad in ["losing", "worse", "threats", "defeat", "bias", "failing"]):
            color_class = "accent-loss"
        elif any(good in lower for good in ["finding", "rewards", "smarter", "free"]):
            color_class = "accent-gain"
        
        html_groups += f'      <span id="cg-{i}-w-{j}" class="word {color_class}" style="display: inline-block;">{text}</span>\n'
    html_groups += f'    </div>\n'

    # GSAP logic for this group
    gsap_logic += f'    // Group {i}\n'
    gsap_logic += f'    tl.set("#cg-{i}", {{ visibility: "visible" }}, {group["start"]:.2f});\n'
    # Base group entrance
    gsap_logic += f'    tl.from("#cg-{i}", {{ scale: 0.8, opacity: 0, duration: 0.2, ease: "back.out(1.5)" }}, {group["start"]:.2f});\n'
    
    # Word pop and color logic
    for j, word in enumerate(group["words"]):
        # Pop each word slightly on its start time
        gsap_logic += f'    tl.to("#cg-{i}-w-{j}", {{ scale: 1.15, duration: 0.1, yoyo: true, repeat: 1 }}, {word["start"]:.2f});\n'

    # Exit
    # Wait, the rule is NO exit animation before a transition, EXCEPT for captions which need hard kill to avoid overlap.
    gsap_logic += f'    tl.to("#cg-{i}", {{ scale: 1.1, opacity: 0, duration: 0.15, ease: "power2.in" }}, {group["end"] - 0.15:.2f});\n'
    gsap_logic += f'    tl.set("#cg-{i}", {{ opacity: 0, visibility: "hidden" }}, {group["end"]:.2f});\n\n'

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@700;900&display=swap');
    
    body, html {{
      margin: 0;
      padding: 0;
      background: #111111;
      width: 100%;
      height: 100%;
      overflow: hidden;
    }}
    
    .scene-content {{
      width: 1080px;
      height: 1920px;
      position: relative;
    }}

    .bg-layer {{
      position: absolute;
      top: 0;
      left: 0;
      width: 1080px;
      height: 1920px;
      object-fit: cover;
      opacity: 0;
      z-index: 0;
    }}


    .caption-group {{
      font-family: 'Outfit', sans-serif;
      font-weight: 900;
      font-size: 110px;
      color: #FFFFFF;
      text-transform: uppercase;
      line-height: 1.1;
      text-shadow: 0 4px 20px rgba(0,0,0,0.8);
      padding: 0 80px;
      box-sizing: border-box;
      z-index: 10;
    }}

    .word {{
      margin: 0 10px;
    }}

    .accent-loss {{
      color: #FF3366;
    }}

    .accent-gain {{
      color: #00E5FF;
    }}
  </style>
</head>
<body>
  <!-- Root composition -->
  <div data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{total_duration:.2f}">
    <div class="scene-content">
      <img id="bg-1" class="bg-layer" src="bg-1.png">
      <img id="bg-2" class="bg-layer" src="bg-2.png">
      <img id="bg-3" class="bg-layer" src="bg-3.png">
      <img id="bg-4" class="bg-layer" src="bg-4.png">
{html_groups}
    </div>
    
    <audio
      id="narration"
      data-start="0"
      data-duration="{total_duration:.2f}"
      data-track-index="1"
      src="narration.wav"
      data-volume="1"
    ></audio>

    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      
{bg_logic}
{gsap_logic}
      
      window.__timelines["main"] = tl;
    </script>
  </div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_template)

print("Generated index.html with timeline.")
