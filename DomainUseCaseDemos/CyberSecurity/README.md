# CyberSecurity Demos

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `DomainUseCaseDemos/CyberSecurity/`

Hands-on cybersecurity demos designed for students learning how data science and machine
learning techniques apply to real-world threat detection, log analysis, and security
operations. All demos use synthetic data with realistic formats — no real infrastructure
is exposed or required.

---

## Demos

| Folder | Topic | Difficulty |
|--------|-------|-----------|
| [ServerLogIntrusion](ServerLogIntrusion/) | Intrusion detection from server logs | Intermediate |

---

## ServerLogIntrusion

**[→ Open Demo](ServerLogIntrusion/)**

Detect cyberattacks by parsing and analysing three standard log formats that every
production Linux server generates:

| Log File | Format | Attack Scenarios Embedded |
|----------|--------|--------------------------|
| `apache_access.log` | Apache Combined Log Format | SQL injection, path traversal, XSS, HTTP flood, malicious scanner |
| `ssh_auth.log` | Linux syslog (OpenSSH) | SSH brute force (139 attempts → successful login) |
| `firewall.log` | iptables / netfilter kernel log | Port scan across 40 distinct ports |

All attacker IPs use RFC 5737 non-routable ranges (`192.0.2.0/24`, `198.51.100.0/24`,
`203.0.113.0/24`) — safe for classroom use without any real IP exposure.

**Detection algorithms (7):**

1. SSH brute-force — sliding-window failed-login rate
2. SQL injection — regex pattern matching on request URIs
3. Path traversal — directory escape sequence detection
4. Cross-site scripting (XSS) — script injection pattern matching
5. Malicious scanner user-agent — known bad UA string matching
6. HTTP flood / DoS — request-rate cardinality counting per IP
7. Port scan — distinct destination-port count per source IP

**Attack → MITRE ATT&CK mapping included in the README and detection script.**

**Files:**
```
ServerLogIntrusion/
├── README.md                  # full lab guide with learning exercises
├── intrusion_detection.py     # 7-detector analysis script, matplotlib 2x3 dashboard
├── generate_logs.py           # reproducible log generator (--seed, --days flags)
├── requirements.txt
└── data/
    ├── apache_access.log      # 205 lines, Apache Combined Log Format
    ├── ssh_auth.log           # 214 lines, Linux syslog SSH auth
    └── firewall.log           # 90 lines, iptables kernel log
```

**Quick start:**
```bash
cd DomainUseCaseDemos/CyberSecurity/ServerLogIntrusion
pip install -r requirements.txt
python intrusion_detection.py
```

---

## Planned / Suggested Future Demos

The following demos would fit naturally in this section. Contributions are welcome —
see [CONTRIBUTING.md](../../CONTRIBUTING.md).

| Demo Idea | Techniques | Suggested Folder |
|-----------|------------|-----------------|
| Network Traffic Anomaly Detection | Isolation Forest, DBSCAN on synthetic PCAP-derived flow data | `NetworkAnomalyDetection/` |
| Phishing URL Classifier | NLP + feature engineering on URL structure | `PhishingURLClassifier/` |
| Insider Threat Detection | User behaviour analytics, sequence anomalies | `InsiderThreatUBA/` |
| SIEM Alert Correlation | Rule-based + ML alert triage on synthetic SIEM events | `SIEMAlertCorrelation/` |
| Malware Feature Analysis | Static PE feature classification (synthetic feature vectors) | `MalwareStaticAnalysis/` |

---

## Prerequisites

Python 3.9+ with the packages in each demo's `requirements.txt`. No external services,
no API keys, and no real network traffic required.

---

## Attribution Reminder

If you use any of these demos in a course, workshop, or project, the three mandatory
requirements in [ATTRIBUTION.md](../../ATTRIBUTION.md) apply:

1. **Credit Professor Vinaya Sathyanarayana** in every presentation, handout, and published resource.
2. **Star the repository** at https://github.com/VinayaSharada/KateelLearningDemosToStudents
3. **Email vinallcontact@gmail.com** with a usage notification.
