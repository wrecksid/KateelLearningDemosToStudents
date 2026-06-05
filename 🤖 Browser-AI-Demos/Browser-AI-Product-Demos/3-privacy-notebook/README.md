# 3 — Privacy Notebook

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/Browser-AI-Product-Demos/3-privacy-notebook/`

A **local AI writing assistant** powered by T5-Small that runs entirely in the browser. Three tools — Polish, Summarise, Grammar Fix — transform selected or full notebook text without any data leaving the device. Designed for use cases where content privacy is non-negotiable.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Model | **T5-Small** (text2text-generation) — ~240 MB, cached after first load |
| Polish | Rewrites the text to be clearer and more professional |
| Summarise | Produces a concise summary of longer passages |
| Grammar Fix | Corrects grammar and punctuation errors |
| UI | Split-pane notebook editor; floating tool dock at the bottom of the text area |
| Status bar | Green progress gradient during model download; green-dot ready state |

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
# Open http://localhost:8080/3-privacy-notebook/
```

Requires a **WebGPU-capable browser** (Chrome 113+, Edge 113+). T5-Small downloads ~240 MB on first run and caches automatically.

---

## Architecture Notes

```
User writes text in notebook pane
              │
  Click "Polish" / "Summarise" / "Grammar Fix"
              │
              ▼
  text2text-generation pipeline
  (T5-Small + task prefix)
              │
              ▼
  Output replaces / appends to right pane
```

Each tool wraps the input text in a T5 task prefix (e.g. `"grammar: "`, `"summarize: "`) before calling `pipeline()`. The model returns a transformed version.

---

## Privacy Guarantee

All inference runs in the browser's GPU via WebGPU. No network requests are made after the initial model download. Text never leaves the device.

---

## How This Connects to Other Demos

- [`1-local-chat-advisor`](../1-local-chat-advisor/) — generative chat using a similar privacy-first approach
- [`4-whisper-voice-transcriber`](../4-whisper-voice-transcriber/) — audio-to-text that feeds into this notebook's editor

---

## Student Extensions

1. Add a **Translate** tool using a MarianMT model (e.g. Helsinki-NLP/opus-mt-en-fr).
2. Implement **auto-save** to `localStorage` so notes persist across sessions.
3. Add a **Tone selector** (Formal / Casual / Technical) that changes the polish prompt prefix.
4. Chain Whisper → Privacy Notebook: transcribe voice notes then auto-polish them.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
