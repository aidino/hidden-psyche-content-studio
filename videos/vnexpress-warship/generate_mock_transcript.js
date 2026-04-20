const fs = require('fs');
const text = fs.readFileSync('narration.txt', 'utf8');
const words = text.replace(/[\n\r]+/g, ' ').split(/\s+/).filter(w => w.trim().length > 0);
const duration = 83.832;
const timePerWord = duration / words.length;

const transcript = words.map((w, i) => {
  return {
    text: w,
    start: Number((i * timePerWord).toFixed(2)),
    end: Number(((i + 1) * timePerWord).toFixed(2))
  };
});

fs.writeFileSync('transcript.json', JSON.stringify(transcript, null, 2));
console.log('Created transcript.json with ' + words.length + ' words.');
