# CI/CD Log Anomaly Detector

## Overview
This project uses **Python + scikit-learn** to detect anomalies in CI/CD pipeline logs (e.g., Jenkins, GitHub Actions).  
It helps identify flaky tests, unusual build failures, and performance regressions early.

## Features
- Log preprocessing (tokenization, vectorization)
- Anomaly detection using Isolation Forest
- Visualization with Matplotlib/Grafana integration
- Sample Jenkins logs included

## Setup
#bash
1. Clone this repo:
#bash
git clone <repo>
cd log-anomaly-detector
pip install -r requirements.txt

2. Sample use:
python src/anomaly_detector.py --input data/sample_logs.csv
