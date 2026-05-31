# PM Demo 05 — AI Launch Gate

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/PM-Product-Demos/5-ai-launch-gate/`

An **in-browser launch review simulator** where a PM reviews evidence across 8 dimensions, hears role-based objections, then makes a launch decision that is scored for quality and explained. No AI model required.

---

## What PM Decision Is Being Made?

> Launch now, limited beta, human-reviewed rollout, or delay — for an AI product with known evidence gaps, blocking issues, and cross-functional concerns.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Scenarios | 5 product scenarios with different evidence profiles |
| Evidence dimensions | 8 tabs per scenario: model quality, red team, fairness, privacy, incident readiness, human fallback, legal/compliance, unit economics |
| Traffic-light readiness | Each dimension scored 0–100 with 🟢/🟡/🔴 |
| Blocking issues | Displayed prominently before the decision panel |
| Role-based objections | Legal, Data Science, Engineering, Customer Experience — auto-generated from evidence |
| Decision buttons | Launch Now · Limited Beta · Human-Reviewed Rollout · Delay |
| Decision scoring | Quality score 0–100 with headline and consequences |
| Ideal decision reveal | Shows recommended decision + rationale after the user decides |

---

## Scenarios

| Scenario | Key Issue | Ideal Decision |
|----------|-----------|---------------|
| **Support Copilot** | AI disclosure to customers not published | Limited Beta |
| **Lending Assistant** | Disparate impact detected, ECOA review incomplete | Delay |
| **AI Hiring Screener** | Gender bias confirmed, Title VII review not started | Delay |
| **Recommendation Engine** | No blocking issues — strong evidence package | Launch Now |
| **Healthcare Intake Assistant** | HIPAA risk assessment incomplete, FDA SaMD pending | Human-Reviewed Rollout |

---

## Evidence Dimensions

| Dimension | What It Covers |
|-----------|---------------|
| **Model Quality** | Test accuracy, hallucination rate, validation coverage |
| **Red Team** | Adversarial testing, jailbreak vectors, output safety |
| **Bias & Fairness** | Disparate impact, demographic parity, audit status |
| **Privacy** | Data handling, PII exposure, regulatory compliance |
| **Incident Readiness** | Kill switch, rollback, on-call, runbook |
| **Human Fallback** | Coverage %, override mechanism, appeal path |
| **Legal & Compliance** | Regulatory review, disclosure obligations, certifications |
| **Unit Economics** | Cost per decision, ROI projection, cost to serve |

---

## Decision Quality Scoring

The tool scores each decision based on the evidence profile:

- **90–100**: Optimal decision, well-supported by evidence
- **70–89**: Defensible, minor trade-offs accepted
- **40–69**: Acceptable with significant caveats
- **0–39**: Poor decision — blocking issues ignored or evidence misread

Key insight: **the same model accuracy score can justify different decisions** depending on the use case risk profile. 78% accuracy on a support copilot ≠ 78% accuracy on a lending system.

---

## Role-Based Objections (Auto-Generated)

Objections are generated dynamically from the evidence scores — not hard-coded strings. Legal raises legal score concerns; DS raises model quality gaps; Engineering raises incident readiness; CX raises fairness and customer trust.

---

## Key Learning Concepts

- **Blocking issues are binary** — a 23% disparate impact gap is not "a risk to mitigate"; it's a hard stop
- **Good overall score ≠ ready to launch** — one red dimension can veto ten green ones
- **"Human reviewed" is not a universal fix** — anchoring on biased AI scores, humans can perpetuate the disparity
- **Governance is product work** — launch gates have clear owners, timelines, and consequences

---

## PM Reflection Questions

| Prompt | Insight |
|--------|---------|
| **Decision** | Launch / beta / human-reviewed / delay — a cross-functional governance call |
| **Assumed** | Evidence scores are synthetic; real gates require actual audit reports |
| **Risk** | Ship pressure can rationalise around blocking issues. The tool shows what a block looks like |
| **Override** | A PM accepts lower overall readiness if one blocker has a clear resolution path and timeline |

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
# Open http://localhost:8080/5-ai-launch-gate/
```

---

## Student Extensions

1. **Add a sixth scenario**: Autonomous vehicle routing assistant, fraud detection for small-business lending, or AI-powered medical imaging triage.
2. **Stakeholder negotiation mode**: Allow students to "negotiate" with each role — raising their evidence score by committing to specific mitigations.
3. **Post-launch incident simulator**: After launching, reveal a random incident from a probability distribution based on the evidence gaps at launch.
4. **Regulatory jurisdiction selector**: Overlay EU AI Act / US EO / NIST RMF requirements on top of the evidence gaps.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
