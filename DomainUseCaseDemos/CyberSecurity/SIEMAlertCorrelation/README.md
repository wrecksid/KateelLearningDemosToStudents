# SIEM Alert Correlation

**Section:** `DomainUseCaseDemos/CyberSecurity/`
**Author:** Professor Vinaya Sathyanarayana

Reduce alert fatigue and reconstruct attack campaigns from raw SIEM events.
Seven days of synthetic alerts (1,400+ total) contain three embedded attack campaigns.

---

## What This Demo Does

Real SOC analysts receive thousands of alerts per day — most are noise. This demo
shows the core techniques used to separate signal from noise:

| Technique | Purpose |
|-----------|---------|
| Source-IP reputation scoring | Flag IPs appearing across multiple MITRE tactic categories |
| 1-hour burst detection | Identify alert floods from a single source |
| Deduplication | Collapse repeated identical rule firings within 10-min windows |
| Kill-chain reconstruction | Map detected alerts to MITRE ATT&CK tactic sequences |
| Severity aggregation | Roll up individual alerts to campaign-level risk |

---

## Embedded Attack Campaigns

| ID | Campaign | MITRE Tactics |
|----|----------|---------------|
| C1 | Phishing → Credential Theft → Lateral Movement → Exfiltration | Initial Access → Credential Access → Lateral Movement → Collection → Exfiltration |
| C2 | SSH Brute Force → Successful Login → Persistence → Crypto-Miner | Credential Access → Initial Access → Persistence → Impact |
| C3 | SQLi → Web Shell → C2 Beacon → Data Staged | Initial Access → Execution → Command and Control → Collection → Exfiltration |

---

## Files

| File | Purpose |
|------|---------|
| `syndata.py` | Generates `data/siem_alerts.csv` (~1,470 alerts over 7 days) |
| `siem_correlation.py` | Runs all five correlation techniques; prints campaign summary; saves dashboard |
| `requirements.txt` | Python dependencies |
| `data/` | Generated CSV |
| `reports/` | Dashboard PNG |

---

## Setup & Run

```bash
cd DomainUseCaseDemos/CyberSecurity/SIEMAlertCorrelation
pip install -r requirements.txt
python syndata.py
python siem_correlation.py
```

---

## Dashboard Panels

1. Hourly alert volume stacked by severity
2. Severity distribution pie chart (after deduplication)
3. Source IP reputation — tactic spread bar chart
4. Alert burst detection — top source IPs per 1-hour window
5. Kill-chain coverage heatmap — tactic × campaign matrix
6. Alert volume by category (authentication / network / endpoint / application)

---

## Student Extensions

1. Implement **graph-based correlation**: build a bipartite graph of src_ip → affected_host and find connected components that span multiple alert categories.
2. Add a **MITRE ATT&CK stage counter** and flag campaigns that have progressed past "Lateral Movement".
3. Experiment with different deduplication windows (5 min, 30 min, 60 min) and measure false-negative rate against the embedded campaigns.
4. Add a **fourth campaign** in `syndata.py` — supply chain / software update poisoning — and extend the kill-chain reconstruction to detect it.
5. Replace the rule-based burst detector with an **LSTM** trained on alert sequences.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../ATTRIBUTION.md)
for mandatory credit, star, and usage notification requirements.
