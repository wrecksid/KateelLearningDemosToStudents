# Network Anomaly Detection

**Section:** `DomainUseCaseDemos/CyberSecurity/`
**Author:** Professor Vinaya Sathyanarayana

Detect network-based attacks by analysing synthetic NetFlow-style traffic records.
Four attack scenarios are embedded in the data; four complementary detectors find them.

---

## What This Demo Does

| Detector | Attack Targeted | Method |
|----------|----------------|--------|
| Isolation Forest | General anomalies | Unsupervised ML on 6 flow features |
| Z-score (bytes_out) | Data exfiltration | Statistical outlier — z > 4 |
| Port-scan rule | Reconnaissance | Unique dst_ports per src_ip in 10-min window > 20 |
| Beaconing detection | C2 communication | Inter-arrival coefficient of variation < 0.05 |

---

## Embedded Attack Scenarios

| Label | Description | Attacker IP |
|-------|-------------|-------------|
| `exfiltration` | 45 large uploads (400 KB–2 MB) to C2 between 01:00–02:30 | `192.0.2.15` |
| `port_scan` | 200-port TCP SYN sweep of an internal host at 14:xx | `198.51.100.99` |
| `beaconing` | 96 heartbeat connections every 300 s ± 5 s all day | `203.0.113.77` |
| `ddos` | 500-packet UDP flood burst from internal host at 21:xx | internal |

All attacker IPs use RFC 5737 non-routable ranges — safe for classroom use.

---

## Files

| File | Purpose |
|------|---------|
| `syndata.py` | Generates `data/network_flows.csv` (~5,800 flows) |
| `network_anomaly_detection.py` | Runs all four detectors, prints summary, saves dashboard |
| `requirements.txt` | Python dependencies |
| `data/` | Generated CSV (created by syndata.py) |
| `reports/` | Dashboard PNG (created by the detector script) |

---

## Setup & Run

```bash
cd DomainUseCaseDemos/CyberSecurity/NetworkAnomalyDetection
pip install -r requirements.txt
python syndata.py
python network_anomaly_detection.py
```

Expected output: detection summary table + `reports/network_anomaly_dashboard.png`

---

## Dashboard Panels

1. Hourly flow volume stacked by attack type
2. Bytes-out distribution (log scale) — exfiltration visible as right tail
3. Isolation Forest score histogram — flagged vs normal
4. Port-scan: unique dst_ports per src_ip per 10-min window
5. Beaconing: inter-arrival coefficient of variation per (src, dst) pair
6. Summary bar: flows flagged by each detector

---

## Student Extensions

1. Add a **lateral movement** scenario (internal-to-internal on unusual ports) and extend the detectors.
2. Replace the Z-score detector with an **hourly per-IP baseline** to reduce false positives.
3. Add a **GeoIP lookup** stub that flags connections to RFC 5737 ranges as external attacker IPs.
4. Tune the Isolation Forest `contamination` parameter and observe the precision/recall trade-off.
5. Combine all four detector flags into a **composite risk score** and rank hosts by risk.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../ATTRIBUTION.md)
for mandatory credit, star, and usage notification requirements.
