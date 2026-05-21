# 2 — Customer Support Smart Ticket Tagger

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/Browser-AI-Product-Demos/2-customer-support-tagger/`

Demonstrates **dual-model NLP inference in the browser**: sentiment analysis with DistilBERT-SST-2 combined with zero-shot intent routing using DeBERTa-NLI. As an agent types a support ticket, the UI tags it in real time — no server call, no latency from a remote API.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Sentiment model | **DistilBERT-SST-2** — binary positive/negative sentiment score on the ticket text |
| Intent routing | **DeBERTa-v3-base-mnli** — zero-shot classification against custom intent labels (Billing, Technical, Cancellation, Complaint, General Inquiry, etc.) |
| Debounce | 300 ms after last keystroke before inference fires — prevents excessive GPU usage while typing |
| Output | Colour-coded intent badge + sentiment bar updated live below the textarea |
| Status bar | Per-model download progress for both pipelines shown sequentially |

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
# Open http://localhost:8080/2-customer-support-tagger/
```

Requires a **WebGPU-capable browser** (Chrome 113+, Edge 113+). Both models download on first run (~130 MB combined) and cache in the browser.

---

## Architecture Notes

```
Textarea input ──► 300ms debounce
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
   sentiment pipeline           zero-shot pipeline
   (DistilBERT-SST-2)     (DeBERTa NLI + intent labels)
          │                           │
          ▼                           ▼
   sentiment bar                intent badge
```

Both pipelines are loaded in sequence at startup. The debounce ensures only one inference pair fires per burst of typing.

---

## How This Connects to Other Demos

- [`1-local-chat-advisor`](../1-local-chat-advisor/) — generative model, same WebGPU runtime
- [`5-entity-tagger`](../5-entity-tagger/) — NER instead of classification, same architecture pattern
- [`DomainUseCaseDemos/Banking/Marketing001`](../../../DomainUseCaseDemos/Banking/Marketing001/) — server-side NLP for support triage

---

## Student Extensions

1. Add a third label set for **priority** (Low / Medium / High / Urgent) using a second zero-shot call.
2. Build a **ticket queue table** below the input that accumulates all tagged tickets in the session.
3. Replace the intent labels with your own business vocabulary (e.g. Insurance: Claim / Policy / Payment).
4. Add **confidence threshold** control — show "Uncertain" if top label < 60%.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
