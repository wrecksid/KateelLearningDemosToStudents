# Phishing URL Classifier

**Section:** `DomainUseCaseDemos/CyberSecurity/`
**Author:** Professor Vinaya Sathyanarayana

Classify URLs as benign or phishing using engineered URL-structure features.
Three classifiers are trained and compared; a 2×3 dashboard visualises performance.

---

## What This Demo Does

Phishing URLs have recognisable structural patterns: they tend to be longer, use
more dots and hyphens, embed IP addresses, use uncommon TLDs, skip HTTPS, and bury
brand names in subdomains. This demo extracts 18 such features and trains:

| Model | Why Included |
|-------|-------------|
| Logistic Regression | Linear baseline; coefficients are interpretable |
| Random Forest | Ensemble; provides feature importance ranking |
| Gradient Boosting | Usually achieves the best AUC on tabular data |

---

## Features Extracted from Each URL

| Feature | Phishing Signal |
|---------|----------------|
| `url_length` | Phishing URLs average 2–3× longer |
| `num_dots` | Deeper subdomain nesting to mimic real domains |
| `num_hyphens` | Hyphens used to concatenate brand names (pay-pal-secure.xyz) |
| `has_ip_address` | IP in place of domain name — strong phishing indicator |
| `tld_is_common` | .xyz / .tk / .top — uncommon TLDs overrepresented in phishing |
| `has_https` | ~82% phishing URLs lack HTTPS in this dataset |
| `url_entropy` | Randomised subdomains → higher Shannon entropy |
| `num_suspicious_words` | "login", "verify", "secure", "update", "account" |
| `brand_in_subdomain` | paypal.attacker.com pattern |

---

## Files

| File | Purpose |
|------|---------|
| `syndata.py` | Generates `data/url_features.csv` (4,500 labelled records) |
| `phishing_classifier.py` | Trains 3 models, prints reports, saves dashboard |
| `requirements.txt` | Python dependencies |
| `data/` | Generated CSV (created by syndata.py) |
| `reports/` | Dashboard PNG (created by the classifier script) |

---

## Setup & Run

```bash
cd DomainUseCaseDemos/CyberSecurity/PhishingURLClassifier
pip install -r requirements.txt
python syndata.py
python phishing_classifier.py
```

---

## Dashboard Panels

1. ROC curves for all three models
2. Feature importance (Random Forest)
3. Confusion matrix of the best-AUC model
4. AUC bar comparison
5. Precision / Recall / F1 grouped bar
6. URL length distribution by class

---

## Student Extensions

1. Add a **`domain_age_days`** synthetic feature and observe its importance.
2. Try **XGBoost** or **LightGBM** and compare against Gradient Boosting.
3. Apply **SHAP** values to explain individual predictions.
4. Experiment with the class imbalance — increase phishing ratio to 1:10 and retrain.
5. Add a **threshold sweep** plot showing precision vs recall vs F1 vs threshold.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../ATTRIBUTION.md)
for mandatory credit, star, and usage notification requirements.
