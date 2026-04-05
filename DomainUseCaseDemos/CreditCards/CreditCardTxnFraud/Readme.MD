# Banking-Classification-CreditCardFraud

## Author  
Vinaya Sathyanarayana

---

## Topic  
**Domain:** Banking  
**Sub-Domain:** Credit Cards  
**Technique:** Classification  
**Use Case:** Fraud Detection  
**Algorithms:** Random Forest, SVM, Logistic Regression, KNN  

Detect fraudulent credit card transactions using classification algorithms on synthetic data.

---

## Folder Contents

- `generate_synthetic_data.py`  
  Generates synthetic credit card transaction dataset mimicking real world patterns including fraud labels.  
  Parameters for dataset size, fraud ratio, and locale can be configured.  
  Output file: `syntheticdata.csv`

- `fraud_detection_classification.py`  
  Demonstrates the use of classification models on the synthetic dataset to detect fraud.  
  Includes evaluation metrics, graphs, and explanations of interpretation.  
  Outputs performance comparison for Random Forest, SVM, Logistic Regression, and KNN.

- `requirements.txt`  
  Required Python packages for synthetic data generation and classification demo.

- `setup_venv.sh` and `setup_venv.bat`  
  Scripts to create a Python virtual environment on Linux/macOS and Windows respectively, and install dependencies.

---

## How to Run the Demos

1. **Setup Python Environment**

   On Linux/macOS:
bash setup_venv.sh
source venv/bin/activate

text

On Windows (PowerShell or CMD):
setup_venv.bat
call venv\Scripts\activate

text

2. **Generate Synthetic Data**

Run:
python generate_synthetic_data.py

text

Optional parameters:
- `--rows` (int): Number of transactions to generate (default 10000)  
- `--fraud_ratio` (float): Ratio of fraudulent transactions (default 0.02)  
- `--locale` (str): Faker locale (default en_IN)  
- `--output` (str): Output CSV file name (default syntheticdata.csv)  

3. **Run Fraud Detection Demo**

python fraud_detection_classification.py

text

This will load the syntheticdata.csv file, train models, display graphs and output evaluation metrics and explanations.

---

## Notes for Students

- Explore the effect of dataset size and fraud ratio on model accuracy and recall.  
- Understand the meaning of confusion matrix and error types for fraud detection.  
- Tune hyperparameters of models and compare changes in performance.  
- Examine feature importance to discover key fraud indicators.

---

## Notes for Banks and Practitioners

- This demo shows how machine learning helps detect fraudulent credit card transactions in near real-time.  
- Class imbalance handling and feature engineering are critical due to rarity of fraud cases.  
- Multiple algorithms should be compared to select the best for a specific institution’s usage.  
- False positives and negatives have operational and customer trust impact; understanding confusion matrices helps balance these.  
- Real deployment would require further model validation, additional data sources, and continuous monitoring.

---

## Contact

For questions or feedback, please reach out to the author: Vinaya Sathyanarayana

---
