# PM Demo 04 — Pricing & Unit Economics Explorer

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/PM-Product-Demos/4-pricing-unit-economics/`

An **in-browser unit economics simulator** showing how inference cost, MAU, prompts-per-user, and pricing model interact to drive gross margin. Includes cohort analysis, margin collapse detection, and scenario comparison. No AI model required.

---

## What PM Decision Is Being Made?

> How to price an AI product — and at what scale, usage pattern, or pricing model does the gross margin become unsustainable?

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Product type presets | SaaS Copilot · API Product · Recommendation Engine · Document AI Workflow |
| Pricing models | Subscription · Usage-Based · Freemium · Hybrid · Enterprise License |
| Input sliders | MAU, prompts/user, tokens/prompt, model cost, infra, support, pricing |
| KPI cards | Revenue, COGS, Gross Profit, Gross Margin (circular gauge) |
| COGS breakdown | Stacked bar: LLM cost % vs Infra % vs Support % |
| Cohort table | Light (20% usage) / Medium (100%) / Heavy (400%) — cost to serve + margin % |
| Margin collapse alert | Red banner when heavy users go margin-negative |
| Sensitivity analysis | "What if model cost doubles?" / "10× MAU" / "50% more free users" |
| Scenario compare | Snapshot A vs B side-by-side |

---

## Revenue & COGS Formulas

```
Monthly Revenue (Subscription)  = paying_users × subscription_price
Total Token Volume               = MAU × prompts_per_user × tokens_per_prompt
LLM Cost                        = (token_volume / 1000) × model_cost_per_1k
Infra Cost                      = MAU × infra_cost_per_mau
Support Cost                    = MAU × support_cost_per_mau
Total COGS                      = LLM + Infra + Support
Gross Profit                    = Revenue − COGS
Gross Margin                    = Gross Profit / Revenue × 100%
```

Cohort cost multipliers:
- **Light users**: 0.2× average token volume
- **Medium users**: 1.0× average (= definition of average)
- **Heavy users**: 4.0× average (real power users often reach 10–50×)

---

## Key Learning Concepts

- **LLM cost scales with usage, revenue doesn't** (in subscription models) — this is the fundamental tension
- **Heavy users destroy unit economics** — the 4× multiplier is conservative; real usage distributions are fat-tailed
- **Freemium works until the free tier scales** — increasing free-tier % on thin margins is a margin compression trap
- **Usage-based pricing aligns cost and revenue** — but introduces revenue unpredictability and sales complexity

---

## Product Type Presets

| Type | MAU | Prompts/User | Tokens/Prompt | Model Cost/1k |
|------|-----|-------------|--------------|--------------|
| SaaS Copilot | 5,000 | 200 | 3,000 | $0.008 |
| API Product | 2,000 | 1,000 | 5,000 | $0.004 |
| Recommendation Engine | 50,000 | 50 | 500 | $0.002 |
| Document AI Workflow | 500 | 100 | 10,000 | $0.012 |

---

## Margin Collapse Warning Triggers

| Condition | Warning |
|-----------|---------|
| Heavy-user margin < 0% | 🔴 "Margin Collapse Risk — heavy users cost more than they pay" |
| Heavy-user margin 0–20% | 🟡 "Heavy-user margin is thin — consider usage caps" |
| Free-tier > 50% + margin < 40% | 🟡 "Freemium structure is margin-compressing" |
| Usage-based + high token volume | "Revenue ceiling risk — consider hybrid pricing" |

---

## PM Reflection Questions

| Prompt | Insight |
|--------|---------|
| **Decision** | How to price an AI product without destroying margin at scale |
| **Assumed** | Costs are fixed-rate per token; real costs vary by model, provider, batching |
| **Risk** | Heavy-user multiplier is 4×; real power users can be 20–50× average |
| **Override** | Validate heavy-user behavior from actual usage logs before setting tier limits |

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
# Open http://localhost:8080/4-pricing-unit-economics/
```

---

## Student Extensions

1. **Usage distribution model**: Replace the 3-cohort table with a full histogram of usage distribution (e.g., log-normal) to show margin at each percentile.
2. **Churn model**: Add monthly churn rate and show how LTV vs COGS changes over 12 months.
3. **Competitor pricing overlay**: Add a competitor's published pricing and show what margin they would run at your cost structure.
4. **Token optimisation lever**: Add a "prompt compression" slider (0–80%) to show how engineering investment in shorter prompts affects COGS.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
