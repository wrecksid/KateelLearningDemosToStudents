# 8 — Opinion Quintuple Extractor

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/Browser-AI-Product-Demos/7-opinion-quintuple-extractor/`

An **in-browser Opinion Mining / Aspect-Based Sentiment Analysis (ABSA)** demo. Paste any product or service review and the demo extracts structured **opinion quintuples** entirely on-device using SmolLM2-360M-Instruct — no API key, no server.

---

## What Is an Opinion Quintuple?

Based on Bing Liu's foundational opinion mining framework, every opinion in a text can be represented as a 5-tuple:

```
( oj,  fjk,  soijkl,  hi,  tl )
```

| Symbol | Field | Example |
|--------|-------|---------|
| `oj` | **Object** — the target entity | `iPhone` |
| `fjk` | **Feature** — an attribute of the object | `battery life` |
| `soijkl` | **Sentiment** — the polarity (+, −, neutral) | `negative` |
| `hi` | **Holder** — who expressed the opinion | `reviewer's mother` |
| `tl` | **Time** — when the opinion was expressed | `a few days ago` |

### Example

Input:
> *"I bought an iPhone a few days ago. The touch screen was really cool. The battery life was not long. My mother thought the phone was too expensive."*

Extracted quintuples:

| # | Object | Feature | Sentiment | Holder | Time |
|---|--------|---------|-----------|--------|------|
| 1 | iPhone | touch screen | positive | reviewer | a few days ago |
| 2 | iPhone | battery life | negative | reviewer | a few days ago |
| 3 | iPhone | price | negative | reviewer's mother | a few days ago |

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Model | **SmolLM2-360M-Instruct** (onnx-community, q4 quantised) — ~200 MB |
| Task | Structured JSON extraction via few-shot system prompt |
| Preset reviews | iPhone, Hotel, Laptop, Restaurant — pre-loaded examples |
| Output | Colour-coded quintuple cards (green=positive, red=negative, grey=neutral) |
| JSON export | Copy raw JSON array to clipboard |
| Streaming | Tokens streamed word-by-word; raw model output toggle available |
| Keyboard shortcut | `Ctrl+Enter` / `Cmd+Enter` to trigger extraction |

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
# Open http://localhost:8080/7-opinion-quintuple-extractor/
```

Or double-click **`start_demos.bat`** in the `Browser-AI-Product-Demos` folder.

Requires a **WebGPU-capable browser** (Chrome 113+, Edge 113+). SmolLM2-360M downloads ~200 MB on first run and caches automatically.

---

## Architecture Notes

```
System prompt (few-shot quintuple extraction instructions)
         +
User message ("Extract quintuples from: [review]")
         +
Assistant primer: "["    ← forces JSON array start
         │
         ▼
 text-generation pipeline
 (SmolLM2-360M-Instruct, q4, do_sample=false)
         │
         ▼
 Streamed JSON tokens → accumulated string
         │
         ▼
 Robust JSON parser (3 fallback strategies)
         │
         ▼
 Quintuple cards rendered in UI
```

**Robust parsing strategies** (tried in order):
1. Regex scan for `[...]` blocks → validate as quintuple array
2. Strip markdown fences, parse full text as JSON
3. Append `]` to close uncompleted array, re-parse

---

## Prompt Engineering

The system prompt:
- Defines all 5 fields with examples
- Instructs extraction of ALL opinions (including third-party holders)
- Maps "I/me" → "reviewer" for consistent holder normalisation
- Requires output to start with `[` (assistant primer enforces this)
- Forbids any surrounding text to reduce parse failures

---

## How This Connects to Other Demos

- [`2-customer-support-tagger`](../2-customer-support-tagger/) — sentence-level sentiment (simpler, faster)
- [`5-entity-tagger`](../5-entity-tagger/) — BERT NER to identify objects and holders
- [`1-local-chat-advisor`](../1-local-chat-advisor/) — same SmolLM2 family used for open chat

---

## Student Extensions

1. **Granular sentiment scores**: Change `sentiment` from 3-class to a 1–5 star rating.
2. **Comparative opinions**: Extend the schema with an optional `compared_to` field for sentences like "better than Samsung".
3. **Implicit feature detection**: Identify opinions where the feature is implied (e.g. "It's too heavy" → feature=`weight`).
4. **Aggregation dashboard**: Run the extractor over 50+ reviews, group by feature, and plot average sentiment per feature as a bar chart.
5. **Larger model**: Swap to `Qwen/Qwen2.5-1.5B-Instruct` for better accuracy on complex multi-holder reviews.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
