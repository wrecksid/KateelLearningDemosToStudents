# PM Demo 02 — Feature Prioritization Copilot

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/PM-Product-Demos/2-feature-prioritization-copilot/`

An **in-browser feature prioritization tool** using RICE scoring, MoSCoW classification, Kano hints, AI risk penalties, and strategic scenario weighting. Override machine rankings and record your justification. No AI model required.

---

## What PM Decision Is Being Made?

> Which features to build next quarter, given team capacity, strategic focus, and uncertainty about AI-specific risks.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Pre-loaded features | 8 features across AI, enterprise, UX, and infrastructure categories |
| Scoring formula | RICE = Reach × Impact × Confidence% / Effort — then weighted by scenario |
| Scenario toggle | Growth · Retention · Ops Efficiency · Compliance — reweights the ranking live |
| MoSCoW classification | Derived from percentile rank within current scenario |
| Kano hints | Basic / Performance / Delighter — from feature type |
| AI risk penalty | High uncertainty → 0.75× score; Medium → 0.90×; None → 1.0× |
| Risk penalty | High risk → 0.80×; Medium → 0.92× |
| Override panel | Move features up/down; add justification; see machine rank vs PM rank |
| Trade-off explainer | Click any feature to see full score breakdown |
| Export memo | Markdown summary of ranked sequence + overrides |

---

## Pre-Loaded Feature Set

| # | Feature | Type | AI Uncertainty |
|---|---------|------|---------------|
| 1 | AI-powered search autocomplete | Performance | Medium |
| 2 | Real-time fraud detection (ML) | Basic (compliance) | High |
| 3 | Dark mode | Delighter | None |
| 4 | Bulk CSV export | Performance | None |
| 5 | Recommendation engine v2 | Performance | High |
| 6 | SSO / SAML integration | Basic (enterprise) | None |
| 7 | In-app guided onboarding tour | Performance | None |
| 8 | AI meeting summariser (beta) | Delighter | High |

---

## Scoring Logic

```
RICE     = (Reach × Impact × Confidence%) / Effort
Strategic = (StrategicFit / 10) × scenarioMultiplier
AI Penalty = 0.75 (high) | 0.90 (medium) | 1.00 (none)
Risk Penalty = 0.80 (high) | 0.92 (medium) | 1.00 (low)
Composite = RICE × Strategic × AI Penalty × Risk Penalty
```

Scenario multipliers on strategic weight:
- **Growth**: +40% strategic, +20% reach
- **Retention**: +30% strategic, +30% impact
- **Ops Efficiency**: +0% strategic, +40% effort weight (penalises low-effort less)
- **Compliance**: +50% strategic, +30% confidence

---

## Key Learning Concepts

- **RICE rewards high-reach features** — infrastructure work that unblocks others is systematically undervalued
- **AI uncertainty is a first-class input** — high model uncertainty should reduce confidence, not just risk
- **MoSCoW is relative** — the same feature can be Must in one scenario and Could in another
- **Machine ranking ≠ PM decision** — overrides teach students when judgment matters

---

## PM Reflection Questions

| Prompt | Insight |
|--------|---------|
| **Decision** | What to build next quarter, given constraints and strategic focus |
| **Assumed** | Reach/Impact/Confidence estimates are team inputs — garbage in, garbage out |
| **Risk** | RICE systematically undervalues compliance, security, and infrastructure work |
| **Override** | Regulatory requirements, CEO commitments, and blocker dependencies should override RICE |

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
# Open http://localhost:8080/2-feature-prioritization-copilot/
```

---

## Student Extensions

1. **Import your own backlog**: Add CSV/JSON import so students can paste their own feature ideas.
2. **Dependency graph**: Visualise which features block others and auto-promote unblocked items.
3. **Sprint capacity model**: Add team velocity (story points/sprint) to show which features fit in the next N sprints.
4. **Confidence calibration exercise**: Compare estimated vs actual impact after a feature ships.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
