# PM Product Demos

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/PM-Product-Demos/`

Five **in-browser PM decision tools** that simulate real product management decisions — threshold tuning, feature prioritisation, build-vs-buy, pricing, and launch governance. No backend, no AI model required. Pure JavaScript running entirely in the browser.

---

## Demos

| # | Demo | Key Decision | Sessions |
|---|------|-------------|---------|
| 01 | [Experimentation & Metrics Simulator](1-experimentation-metrics-simulator/) | Confidence threshold × business cost trade-off | 10, 11, 12 |
| 02 | [Feature Prioritization Copilot](2-feature-prioritization-copilot/) | What to build next given RICE, MoSCoW, and strategic fit | 03, 04 |
| 03 | [Build vs Buy vs API Decision Workbench](3-build-buy-api-workbench/) | AI sourcing — in-house vs API vs platform vs partner | 03, 04, 13 |
| 04 | [Pricing & Unit Economics Explorer](4-pricing-unit-economics/) | How to price an AI product without destroying margin | 11, 13, 15 |
| 05 | [AI Launch Gate](5-ai-launch-gate/) | Launch now / limited beta / human-reviewed / delay | 11, 12, 15 |

---

## How to Run

```bash
cd "🤖 Browser-AI-Demos/PM-Product-Demos"
python -m http.server 8080
# Open http://localhost:8080/
```

Or double-click **`start_demos.bat`** in this folder.

Works in any modern browser — Chrome, Edge, Firefox. No WebGPU required.

---

## Common Design Rules

Every demo includes four built-in PM reflection prompts (collapsible):

| Prompt | Purpose |
|--------|---------|
| **What PM decision is being made?** | Names the exact decision the tool supports |
| **What data is assumed?** | Surfaces synthetic/hardcoded inputs students shouldn't over-generalise |
| **What can go wrong if you trust this too much?** | Teaches model limitations |
| **What would a strong PM override here?** | Teaches judgment beyond the tool |

All demos:
- Run from `index.html` — single file, no build step
- No backend or server-side logic
- Work with hardcoded scenario data in first version
- Include a `file://` protocol warning that directs students to use HTTP

---

## Demo Anchor Slides

For course decks, use one named "Demo Anchor" slide per session referencing these demos:

- **Session 10:** `Demo Anchor: Experimentation & Metrics Simulator`
- **Session 03/04:** `Demo Anchor: Feature Prioritization Copilot`
- **Session 13:** `Demo Anchor: Build vs Buy vs API Decision Workbench · Pricing & Unit Economics Explorer`
- **Session 12:** `Demo Anchor: AI Launch Gate`

---

## Attribution

If you use these demos in a course or project, see [ATTRIBUTION.md](../../../ATTRIBUTION.md).
