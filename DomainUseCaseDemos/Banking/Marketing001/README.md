# Banking Pattern Mining for Marketing Upsell and Cross Sell

## Author
Vinaya Sathyanarayana

## Topic Overview

This project demonstrates the use of **frequent itemset mining (pattern mining)** techniques in the **banking domain** for marketing upsell and cross sell of financial products.

### Domain Context
Banks offer multiple financial products such as savings accounts, credit cards, loans, insurance, and mutual funds. Understanding how customers tend to own combinations of these products can help banks design targeted marketing campaigns for upselling and cross selling.

### Techniques Covered
- Downward Closure Property of Frequent Patterns
  - Apriori Algorithm and its extensions/improvements
- Mining Frequent Patterns using Vertical Data Format
- FP-Growth Algorithm (Frequent Pattern Growth)
- Mining Closed Patterns
- Mining Maximal Patterns

### Use Case
The goal is to identify common product bundles owned by customers and generate association rules that can inform marketing decisions on promotions and targeting.

---

## Files Description

- `synthetic_data_generator.py`: Generates synthetic banking customer data with product ownership flags, to simulate real-life banking data. Configurable size and locale support.
- `pattern_mining_demo.py`: Loads synthetic data and applies multiple frequent itemset mining algorithms, visualizes results, generates association rules, and explains how to interpret outputs.
- `requirements.txt`: Python dependencies needed to run the programs.
  
---

## Instructions

1. **Generate Synthetic Data**

   Run the data generator first to create a CSV file:
