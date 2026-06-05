# 5 — Named Entity Tagger

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/Browser-AI-Product-Demos/5-entity-tagger/`

A **browser-side NER (Named Entity Recognition) demo** that highlights persons, organisations, locations, and miscellaneous entities in any text you type or paste — in real time, using BERT-NER running locally via WebGPU and Transformers.js.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Model | **dslim/bert-base-NER** (token-classification pipeline) — ~420 MB |
| Entity types | **PER** (persons), **ORG** (organisations), **LOC** (locations), **MISC** (miscellaneous) |
| Highlighting | Each entity type gets a distinct colour-coded inline span with a label tooltip |
| Input | Editable text area; inference fires automatically after a short pause in typing |
| Status bar | Cyan/indigo progress gradient during model download |

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
# Open http://localhost:8080/5-entity-tagger/
```

Requires a **WebGPU-capable browser** (Chrome 113+, Edge 113+). BERT-NER downloads ~420 MB on first run and caches in the browser.

---

## Architecture Notes

```
User types / pastes text
          │
   short debounce (~400ms)
          │
          ▼
 token-classification pipeline
    (bert-base-NER)
          │
          ▼
 Token predictions grouped into word-level entities
          │
          ▼
 Annotated HTML spans injected into result pane
```

The pipeline returns per-token predictions (B-PER, I-PER, B-ORG, etc.). The demo groups consecutive tokens with the same entity into single spans using the B- / I- prefix convention.

---

## Colour Coding

| Entity | Colour |
|--------|--------|
| PER — Person | Indigo |
| ORG — Organisation | Cyan |
| LOC — Location | Emerald |
| MISC — Miscellaneous | Amber |

---

## How This Connects to Other Demos

- [`2-customer-support-tagger`](../2-customer-support-tagger/) — text classification, same Transformers.js pipeline pattern
- [`6-semantic-search`](../6-semantic-search/) — combine NER extraction with semantic search over results

---

## Student Extensions

1. Add a **filter panel** so users can toggle which entity types are highlighted.
2. Feed NER output into a **knowledge graph** — PER linked to ORG linked to LOC.
3. Test with financial news: does the model correctly tag company names vs. person names?
4. Try `Jean-Baptiste/roberta-large-ner-english` for better accuracy (larger model, more download time).

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
