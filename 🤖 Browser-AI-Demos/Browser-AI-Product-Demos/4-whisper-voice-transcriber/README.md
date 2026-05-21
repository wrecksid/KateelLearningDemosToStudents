# 4 — Whisper Voice Transcriber

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/Browser-AI-Product-Demos/4-whisper-voice-transcriber/`

A **real-time speech-to-text demo** using OpenAI Whisper Tiny (English) running entirely in the browser via WebGPU and Transformers.js. Records microphone audio, displays a live 60-bar waveform visualiser, and transcribes the recording locally — no cloud API, no data upload.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Model | **openai/whisper-tiny.en** (~150 MB) — automatic-speech-recognition pipeline |
| Audio capture | `MediaRecorder` API; 16 kHz PCM pipeline from raw audio chunks |
| Waveform | 60-bar animated amplitude display updated at ~30 fps during recording |
| Languages | Primarily English; model also handles 7 further languages with reduced accuracy |
| Output | Transcript text appears below the recorder card after processing |
| Status bar | Pink/purple progress gradient during model download |

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Complete single-file demo — HTML + CSS + JavaScript |

---

## How to Run

```bash
cd "🤖 Browser-AI-Demos/Browser-AI-Product-Demos"
python -m http.server 8080
# Open http://localhost:8080/4-whisper-voice-transcriber/
```

**Browser requirements:**
- Chrome 113+ or Edge 113+ (WebGPU)
- Microphone permission granted when prompted

Model downloads ~150 MB on first run and caches in the browser's `Cache API`.

---

## Architecture Notes

```
Microphone ──► MediaRecorder (WebAudio API)
                    │
                    ▼
           Raw audio chunks (Float32Array)
                    │
                    ▼
           Resample to 16 kHz PCM
                    │
                    ▼
   automatic-speech-recognition pipeline
          (whisper-tiny.en)
                    │
                    ▼
           Transcript text shown in UI
```

The 60-bar waveform reads `AnalyserNode.getByteFrequencyData()` on each animation frame and maps it to CSS `height` on the bar elements.

---

## How This Connects to Other Demos

- [`3-privacy-notebook`](../3-privacy-notebook/) — transcribed text can be pasted into the notebook for polishing
- [`1-local-chat-advisor`](../1-local-chat-advisor/) — voice-to-chat pipeline possible by chaining both demos

---

## Student Extensions

1. Switch to `whisper-small` for better multilingual accuracy (adds ~250 MB download).
2. Add **real-time streaming transcription** using `chunk_length_s` parameter for long recordings.
3. Wire the transcript output directly into the Privacy Notebook editor — build a voice-to-polished-note pipeline.
4. Add **language detection** using the Whisper `language` token to auto-detect the spoken language.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
