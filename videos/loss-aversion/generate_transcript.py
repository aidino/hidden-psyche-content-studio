import json
import soundfile as sf
import os

with open('SCRIPT.md', 'r') as f:
    text = f.read()

# Read the duration
audio_info = sf.info('narration.wav')
duration = audio_info.duration

# Generate Transcript (uniform distribution)
words = text.split()
transcript = []
time_per_word = duration / len(words)
current_time = 0.0

for word in words:
    clean_word = "".join(c for c in word if c.isalnum() or c in "'-!?.,")
    if not clean_word:
        clean_word = word
    transcript.append({
        "text": clean_word,
        "start": current_time,
        "end": current_time + time_per_word
    })
    current_time += time_per_word

with open("transcript.json", "w") as f:
    json.dump(transcript, f, indent=2)

print(f"Generated transcript.json for {duration:.2f}s of audio, {len(words)} words.")
