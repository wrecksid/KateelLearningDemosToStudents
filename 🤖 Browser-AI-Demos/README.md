# 🤖 Browser-AI-Demos

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana

Seven production-quality in-browser AI demos. Every demo runs 100% locally — no server,
no API key, no data ever leaves the device. Models are downloaded once by the browser and
cached; subsequent runs are fully offline.

---

## Why In-Browser AI?

| Traditional Server-Side AI | These Demos |
|---------------------------|-------------|
| Requires a running server | Open `index.html` directly |
| Needs API keys and billing | Zero cost, zero accounts |
| Data leaves the device | 100% private — runs on-device |
| Breaks if internet drops | Works fully offline after first load |
| Hard to share with students | Share a single HTML file |

These demos show students that modern Small Language Models are compact enough to run
entirely in a browser tab using WebGPU — a fundamental shift in how AI applications
can be deployed.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Models | Hugging Face ONNX-quantised checkpoints |
| Inference runtime | **Transformers.js v3** (`@huggingface/transformers@3` via jsDelivr CDN) |
| Language | Vanilla JavaScript ES2022 — no build step, no bundler |
| Styling | Pure CSS3, no framework |
| Audio | Web Audio API + OfflineAudioContext (16 kHz PCM for Whisper) |
| Hardware | WebGPU (Chrome 113+, Edge 113+); fallback to WASM |

---

## Demo Hub

Open **[Browser-AI-Product-Demos/index.html](Browser-AI-Product-Demos/index.html)** for
the full launcher page with cards for all seven demos.

---

## Demos

### Text & Language

| # | Demo | Model | Size | Description |
|---|------|-------|------|-------------|
| 1 | [Local Chat Advisor](Browser-AI-Product-Demos/1-local-chat-advisor/) | SmolLM2-135M-Instruct | ~135 MB | Offline study-buddy chatbot with streaming token output and persistent message history |
| 2 | [Smart Ticket Tagger](Browser-AI-Product-Demos/2-customer-support-tagger/) | DistilBERT + DeBERTa | ~140 MB | Real-time sentiment, urgency scoring, and zero-shot department routing on typed support tickets |
| 3 | [Privacy Notebook](Browser-AI-Product-Demos/3-privacy-notebook/) | T5-Small | ~60 MB | Offline text polish, TL;DR summarisation, and grammar correction — no text ever sent to a server |

### Audio, Vision & Search

| # | Demo | Model | Size | Description |
|---|------|-------|------|-------------|
| 4 | [Whisper Voice Transcriber](Browser-AI-Product-Demos/4-whisper-voice-transcriber/) | Whisper Tiny EN | ~39 MB | Live microphone transcription in 7 languages; 60-bar waveform visualiser; 16 kHz PCM resampling pipeline |
| 5 | [Named Entity Tagger](Browser-AI-Product-Demos/5-entity-tagger/) | BERT-NER | ~110 MB | Inline span highlighting of PER / ORG / LOC / MISC entities with colour-coded entity chips |
| 6 | [Semantic Search Engine](Browser-AI-Product-Demos/6-semantic-search/) | all-MiniLM-L6-v2 | ~23 MB | Cosine-similarity search over 10 pre-loaded documents; add your own; keyword comparison toggle |

### Interactive Game

| # | Demo | Model | Size | Description |
|---|------|-------|------|-------------|
| 7 | [SYNAPSE — Semantic Word Game](Browser-AI-Product-Demos/semantic-game/) | mxbai-embed-xsmall-v1 | ~25 MB | Wordle-style word game driven by semantic similarity (0–100% gauge, temperature labels, daily word rotation, share grid) |

---

## Running the Demos

1. Clone the repository (or download a ZIP).
2. Open any `index.html` file directly in **Chrome 113+** or **Edge 113+**.
3. On first load the model downloads (sizes listed above) and is cached by the browser.
4. All subsequent runs are fully offline.

> **No `npm install`, no `python app.py`, no Docker.** Double-click the HTML file.

Verify WebGPU is enabled: navigate to `chrome://gpu` and look for **WebGPU: Enabled**.
If unavailable the demos fall back to WASM automatically.

---

## Architecture Notes

- **Model download tracking** — each demo shows a live download progress bar with
  per-file speed metrics using the Transformers.js `progress_callback` API.
- **Cosine similarity** — implemented as a pure JS formula (`dot / (|a| · |b|)`) with
  no external library, demonstrating that embedding arithmetic needs no ML framework.
- **Whisper audio pipeline** — `MediaRecorder` → `AudioContext.decodeAudioData` →
  `OfflineAudioContext` resampled to 16 kHz mono PCM → passed to the ASR pipeline.
- **Zero-shot routing** — the ticket tagger uses `Xenova/nli-deberta-v3-small` with
  natural-language category labels, requiring no labelled training data.
- **Daily word rotation** — SYNAPSE selects its hidden word via
  `WORDS[Math.floor(Date.now() / 86_400_000) % WORDS.length]` so every player gets
  the same word each day without a server.

---

## Original Specification

The original design spec that drove this section is preserved at the top of this file's
git history. The implemented demos fully satisfy the spec and extend it with four
additional demos (Whisper, NER, Semantic Search, SYNAPSE) beyond the original three.

---

## Attribution Reminder

If you use any of these demos in a course, workshop, or project, the three mandatory
requirements in [ATTRIBUTION.md](../ATTRIBUTION.md) apply:

1. **Credit Professor Vinaya Sathyanarayana** in every presentation, handout, and published resource.
2. **Star the repository** at https://github.com/VinayaSharada/KateelLearningDemosToStudents
3. **Email vinallcontact@gmail.com** with a usage notification.
