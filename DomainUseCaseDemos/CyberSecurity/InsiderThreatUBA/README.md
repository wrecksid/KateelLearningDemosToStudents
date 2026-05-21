# Insider Threat Detection — User Behaviour Analytics (UBA)

**Section:** `DomainUseCaseDemos/CyberSecurity/`
**Author:** Professor Vinaya Sathyanarayana

Detect malicious insiders by building per-user behavioural baselines and flagging
deviations in a 90-day synthetic activity dataset. Three insider threat archetypes
are embedded; two complementary detectors surface them.

---

## What This Demo Does

| Stage | Method |
|-------|--------|
| Baseline (days 1–60) | Per-user mean ± std of 7 daily behaviour features |
| Scoring (days 61–90) | Z-score each feature; composite weighted risk score |
| Unsupervised check | Isolation Forest on all 90 days for independent view |

---

## Embedded Insider Profiles

| User | Archetype | Signals in Final 3 Weeks |
|------|-----------|--------------------------|
| `user_003` | Disgruntled | After-hours logins spike; USB events increase sharply |
| `user_017` | Malicious | Data downloads jump to ~500 MB/day; external emails surge |
| `user_031` | Compromised account | Login hour shifts to 02:xx; new-location logins appear |

---

## Behaviour Features

| Feature | Risk Weight |
|---------|-------------|
| `new_location_login` | 4.0 |
| `after_hours` | 3.0 |
| `usb_events` | 2.5 |
| `data_downloaded_mb` | 2.0 |
| `external_emails_sent` | 1.5 |
| `files_accessed` | 1.0 |
| `login_hour` | 1.0 |

---

## Files

| File | Purpose |
|------|---------|
| `syndata.py` | Generates `data/user_activity.csv` (~3,200 user-day records) |
| `insider_threat_detection.py` | Baseline → scoring → IF → dashboard |
| `requirements.txt` | Python dependencies |
| `data/` | Generated CSV |
| `reports/` | Dashboard PNG |

---

## Setup & Run

```bash
cd DomainUseCaseDemos/CyberSecurity/InsiderThreatUBA
pip install -r requirements.txt
python syndata.py
python insider_threat_detection.py
```

---

## Dashboard Panels

1. Top 20 users by mean daily risk score (recent 30 days)
2. Risk score timeline — the three threat users
3. Data-download signal — malicious user vs normal average
4. After-hours + USB events timeline — disgruntled user
5. Login hour distribution — compromised user vs normal
6. Isolation Forest flags per user

---

## Student Extensions

1. Add a **`resignation_flag`** feature and observe how it correlates with the disgruntled profile.
2. Tune the risk weights and observe how the top-5 ranking changes.
3. Apply **DBSCAN** instead of Isolation Forest and compare which users are flagged.
4. Add a **30-day rolling baseline** (vs static first-60-days) for adaptive profiling.
5. Introduce a **false-positive analysis**: add 2 "noisy-normal" users with high variance and measure how often they appear in the top 10.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../ATTRIBUTION.md)
for mandatory credit, star, and usage notification requirements.
