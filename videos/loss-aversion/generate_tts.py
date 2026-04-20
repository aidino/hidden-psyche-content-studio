import soundfile as sf
import os
import json
from kokoro_onnx import Kokoro

with open('SCRIPT.md', 'r') as f:
    text = f.read()

# Generate TTS
kokoro = Kokoro(os.path.expanduser("~/.cache/hyperframes/tts/kokoro-v0_19.onnx"), os.path.expanduser("~/.cache/hyperframes/tts/voices.bin"))
samples, sample_rate = kokoro.create(text, voice="af_sky", speed=1.1, lang="en-us")
sf.write("narration.wav", samples, sample_rate)

duration = len(samples) / sample_rate
print(f"Generated {duration:.2f}s of audio")

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

print("Generated dummy transcript.json")
