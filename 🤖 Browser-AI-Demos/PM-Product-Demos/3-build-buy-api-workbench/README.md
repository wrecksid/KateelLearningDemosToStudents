# PM Demo 03 — Build vs Buy vs API Decision Workbench

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/PM-Product-Demos/3-build-buy-api-workbench/`

An **in-browser sourcing decision tool** that scores Build / Buy / API / Partner options across 8 constraint dimensions. Includes a quadrant map, risk register, and auto-generated recommendation memo. No AI model required.

---

## What PM Decision Is Being Made?

> Should we build this AI capability in-house, buy a platform, use an external API, or partner — given our constraints on time, budget, privacy, talent, and scale?

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Capability presets | 6 preset capabilities with pre-filled constraints |
| Constraint sliders | 8 sliders: TTM, budget, privacy, customisation, talent, scale, reliability, lock-in |
| Scoring | Weighted formula per option, normalised to 0–100 |
| Option cards | Score bar, "best when" bullets, dynamic red-flag warnings |
| Quadrant map | SVG Control vs Speed map, winner highlighted with pulsing ring |
| Recommendation memo | Rules-based auto-generated rationale + due diligence questions |
| Risk register | 5-dimension × 4-option table with 🟢/🟡/🔴 indicators |
| Export | Copy memo as Markdown |

---

## Capability Presets

| Capability | Pre-filled Bias |
|-----------|----------------|
| Text Summarization | API-friendly (commodity, low privacy, fast TTM) |
| Fraud Detection | Build-leaning (high privacy, custom data, reliability-critical) |
| Recommendation Engine | Build or Buy (differentiating, scale-heavy, latency-sensitive) |
| Internal Copilot | Build-leaning (privacy-critical, org-knowledge requirement) |
| Speech-to-Text | API-friendly (commodity, volume-driven, quality threshold) |
| Document AI / OCR | Buy or Partner (workflow-specific, compliance-driven) |

---

## Scoring Logic

Each option's score is computed as a signed weighted sum of slider values, normalised across the 4 options:

| Option | Boosted by | Penalised by |
|--------|------------|-------------|
| **Build** | Talent, customisation, privacy, lock-in concern, budget | Tight TTM |
| **Buy** | Reliability, budget, scale, speed | Privacy concern, lock-in worry |
| **API** | Speed, scale, budget | Privacy sensitivity, lock-in, customisation need |
| **Partner** | Customisation, reliability | Budget constraints, lock-in concern |

---

## Red Flags Triggered

| Condition | Warning |
|-----------|---------|
| Privacy ≥ 8 + API | External API may violate compliance requirements |
| Talent ≤ 3 + Build | In-house build will likely miss timelines |
| TTM ≥ 8 + Build | In-house build rarely ships in weeks |
| Scale ≥ 9 + API | API cost may exceed build cost at extreme scale |
| Lock-in ≥ 8 + API | Single-vendor API dependency risk |
| Budget ≤ 2 + Buy | Enterprise platform licenses may be unaffordable |

---

## Key Learning Concepts

- **No universally right answer** — the same capability (summarisation) can be API-right for one company and Build-right for another
- **Privacy reframes everything** — highly sensitive data changes the scoring fundamentally
- **Talent gaps have a half-life** — today's "no ML talent" may not be true in 12 months
- **Lock-in is a long-term tax** — cheap to ignore short-term, expensive to fix later

---

## PM Reflection Questions

| Prompt | Insight |
|--------|---------|
| **Decision** | Build / Buy / API / Partner for a specific AI capability |
| **Assumed** | Slider inputs are self-assessed; real decisions need vendor POCs and build estimates |
| **Risk** | Constraints treated as independent; real decisions have complex interdependencies |
| **Override** | A PM might choose API despite privacy concerns if a DPA + private deployment option exists |

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Complete single-file demo |

---

## How to Run

```bash
cd "🤖 Browser-AI-Demos/PM-Product-Demos"
python -m http.server 8080
# Open http://localhost:8080/3-build-buy-api-workbench/
```

---

## Student Extensions

1. **Add "Fine-tune" as a fifth option** — sits between API and Build in the control/speed space.
2. **Vendor comparison sub-module**: After selecting Buy or API, show a comparison matrix of 3 fictitious vendors.
3. **Time-phased strategy**: Model a path that starts with API and transitions to Build as talent grows and volume scales.
4. **Cost projection**: Add a 3-year TCO calculator comparing options.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
