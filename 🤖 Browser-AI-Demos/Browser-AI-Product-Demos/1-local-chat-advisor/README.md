# 1 — Local Chat Advisor

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/Browser-AI-Product-Demos/1-local-chat-advisor/`

A fully **private, zero-server chat interface** that runs a small language model entirely inside the browser using WebGPU and the Transformers.js pipeline. No API keys, no data leaves the device.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Model | **SmolLM2-135M-Instruct** (HuggingFace) — quantised to ~100 MB, streamed from CDN on first load |
| Inference | `text-generation` pipeline with `TextStreamer` — tokens appear word-by-word as they are generated |
| UI | Dark chat bubble layout; user messages right-aligned, assistant responses left-aligned |
| Status bar | Animated amber dot while loading, green on ready; progress track shows download % |
| Context | Full conversation history fed back to the model on each turn |

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Complete single-file demo — HTML + CSS + JavaScript |

---

## How to Run

Open directly in a **WebGPU-capable browser** (Chrome 113+, Edge 113+):

```bash
# From repo root — just open the file:
start "🤖 Browser-AI-Demos/Browser-AI-Product-Demos/1-local-chat-advisor/index.html"
```

Or serve locally (recommended for sub-resource isolation):

```bash
cd "🤖 Browser-AI-Demos/Browser-AI-Product-Demos"
python -m http.server 8080
# Open http://localhost:8080/1-local-chat-advisor/
```

**First load:** model downloads ~100 MB from Hugging Face CDN and caches in the browser's `Cache API`. Subsequent loads are instant.

---

## Architecture Notes

```
User types message
        │
        ▼
 conversation[] array ──► model.generate(messages, { streamer })
        │
        ▼
 TextStreamer.on('text') ──► append tokens to assistant bubble in real time
```

The `progress_callback` from the Transformers.js `pipeline()` constructor drives the status bar percentage display.

---

## How This Connects to Other Demos

- [`2-customer-support-tagger`](../2-customer-support-tagger/) — classification instead of generation
- [`3-privacy-notebook`](../3-privacy-notebook/) — T5-based text editing in the same privacy-first pattern
- All demos in this collection share the same **no-server, WebGPU** philosophy

---

## Student Extensions

1. Swap the model ID to `Phi-3-mini-4k-instruct` and compare response quality vs speed.
2. Add a **system prompt** input so the model can be primed as a financial advisor, tutor, or code reviewer.
3. Implement a **Clear conversation** button that resets the history array.
4. Add **token count** display to show how context window fills up over a long chat.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
