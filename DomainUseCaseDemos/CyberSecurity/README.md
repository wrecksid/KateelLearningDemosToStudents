# CyberSecurity Demos

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `DomainUseCaseDemos/CyberSecurity/`

Six hands-on cybersecurity demos covering threat detection, log analysis, user
behaviour analytics, alert correlation, and malware classification. All demos use
synthetic data in realistic formats — no real infrastructure, API keys, or sensitive
data required.

---

## Demos

| # | Folder | Topic | Key Techniques | Difficulty |
|---|--------|-------|----------------|-----------|
| 1 | [ServerLogIntrusion](ServerLogIntrusion/) | Intrusion detection from server logs | Regex, sliding-window rate analysis, Apache/SSH/iptables log parsing | Intermediate |
| 2 | [NetworkAnomalyDetection](NetworkAnomalyDetection/) | NetFlow anomaly detection | Isolation Forest, Z-score, port-scan rule, beaconing CV | Intermediate |
| 3 | [PhishingURLClassifier](PhishingURLClassifier/) | URL phishing classification | Logistic Regression, Random Forest, Gradient Boosting on URL features | Beginner–Intermediate |
| 4 | [InsiderThreatUBA](InsiderThreatUBA/) | Insider threat user behaviour analytics | Per-user baselines, Z-score risk scoring, Isolation Forest | Intermediate |
| 5 | [SIEMAlertCorrelation](SIEMAlertCorrelation/) | SIEM alert correlation & noise reduction | IP reputation, burst detection, deduplication, kill-chain reconstruction | Intermediate–Advanced |
| 6 | [MalwareStaticAnalysis](MalwareStaticAnalysis/) | PE static feature malware classification | Random Forest, PCA, ROC one-vs-rest, 5 malware families | Intermediate |

---

## Demo Summaries

### 1. Server Log Intrusion Detection
Parse Apache access logs, Linux SSH auth logs, and iptables firewall logs to detect
7 attack types. All attacker IPs use RFC 5737 non-routable ranges. Maps detections
to MITRE ATT&CK tactics.
**Run:** `python intrusion_detection.py`

### 2. Network Anomaly Detection
Detect data exfiltration, port scans, C2 beaconing, and DDoS participation in
synthetic NetFlow-style traffic (~5,800 flows). Four complementary detectors with
a 2×3 matplotlib dashboard.
**Run:** `python syndata.py && python network_anomaly_detection.py`

### 3. Phishing URL Classifier
Classify URLs as benign or phishing using 18 structural features (URL length, dots,
hyphens, entropy, suspicious words, etc.). Trains 3 models, compares ROC/AUC/F1.
**Run:** `python syndata.py && python phishing_classifier.py`

### 4. Insider Threat UBA
90 days of daily activity for 50 employees with 3 embedded threats (disgruntled,
malicious, compromised). Builds per-user baselines, scores deviations, produces
risk-ranked user list.
**Run:** `python syndata.py && python insider_threat_detection.py`

### 5. SIEM Alert Correlation
7 days of synthetic SIEM alerts (1,400+) with 3 embedded attack campaigns. Reduces
noise through deduplication, bursts IP reputation scoring, and reconstructs kill
chains mapped to MITRE ATT&CK.
**Run:** `python syndata.py && python siem_correlation.py`

### 6. Malware Static Analysis
3,600 synthetic PE feature vectors across 6 classes (benign + 5 malware families).
Random Forest with feature importance, PCA 2D scatter, ROC curves, and confusion
matrix.
**Run:** `python syndata.py && python malware_analysis.py`

---

## Prerequisites

Python 3.9+ with the packages in each demo's `requirements.txt`.
No external services, API keys, or real network traffic required.

```bash
pip install -r <demo-folder>/requirements.txt
```

---

## Attribution Reminder

If you use any of these demos in a course, workshop, or project, the three mandatory
requirements in [ATTRIBUTION.md](../../ATTRIBUTION.md) apply:

1. **Credit Professor Vinaya Sathyanarayana** in every presentation, handout, and published resource.
2. **Star the repository** at https://github.com/VinayaSharada/KateelLearningDemosToStudents
3. **Email vinallcontact@gmail.com** with a usage notification.
