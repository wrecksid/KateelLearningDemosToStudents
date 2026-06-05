# PM Demo 01 — Experimentation & Metrics Simulator

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/PM-Product-Demos/1-experimentation-metrics-simulator/`

An **in-browser metrics simulator** showing how confidence thresholds, review policies, and cost assumptions drive precision, recall, review queue size, and business KPIs — all updating in real time. No AI model required.

---

## What PM Decision Is Being Made?

> Setting the confidence threshold that balances automation rate, human review burden, and business cost — for a given use case and operational capacity.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Use cases | Fraud Detection · Support Ticket Routing · Recommendation Relevance · AI Response Approval |
| Controls | Confidence threshold, traffic allocation, review capacity, FP/FN cost |
| Confusion matrix | Live 2×2 matrix with TP/FP/FN/TN counts and % of total |
| Metric cards | Precision, Recall, F1, Review Queue — traffic-light coloured |
| Business impact | Daily cost, cost/1k decisions, use-case-specific KPI proxy |
| Explanation | Auto-generated 2-sentence contextual explanation of current state |
| Scenario compare | Save Snapshot A and B → side-by-side diff table |
| Presets | Conservative / Balanced / Aggressive |

---

## Use Cases and KPI Proxies

| Use Case | Population | True Events | KPI Proxy |
|----------|-----------|-------------|-----------|
| Fraud Detection | 1,000 txn/day | 50 frauds | Fraud Loss Avoided ($) |
| Support Routing | 5,000 tickets/day | 2,000 routable | SLA Hit Rate (%) |
| Recommendation | 100k impressions/day | 15k relevant | Conversion Lift (%) |
| AI Response Approval | 10k responses/day | 8k safe | Approval Rate with Risk |

---

## Key Learning Concepts

- **Precision vs Recall trade-off**: Lowering the threshold improves recall but increases FP volume
- **Review queue saturation**: A threshold that produces more items than the team can review is not operationally viable, even if metrics look good
- **Business cost asymmetry**: FP cost ≠ FN cost — the right threshold depends on which error is more expensive
- **Offline vs online gap**: Test-set curves are modelled here; real deployments show drift and distribution shift

---

## PM Reflection Questions

| Prompt | Insight |
|--------|---------|
| **Decision** | Threshold setting at launch, and again after each model update |
| **Assumed** | Curve shapes are synthetic; real ROC curves are model- and dataset-specific |
| **Risk** | Review queue costs (agent time, tooling, burnout) are not modelled |
| **Override** | A PM might accept higher FN rate short-term to protect reviewer capacity during team scaling |

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
# Open http://localhost:8080/1-experimentation-metrics-simulator/
```

---

## Student Extensions

1. Add a **time series view**: simulate drift in the model's curve over 12 weeks and show how threshold needs to be re-tuned.
2. Add a **cost-optimal threshold finder**: compute the minimum-cost threshold automatically and show it as a reference line.
3. Add a **staffing calculator**: given queue size and handle time, compute the team headcount needed.
4. Add a **fifth use case**: content moderation, medical diagnosis, or loan default prediction.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
