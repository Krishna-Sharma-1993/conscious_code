#python
import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(log_file):
    df = pd.read_csv(log_file)
    features = df[['duration', 'error_count']]  # Example features
    model = IsolationForest(contamination=0.1, random_state=42)
    df['anomaly'] = model.fit_predict(features)
    print(df[df['anomaly'] == -1])

if __name__ == "__main__":
    detect_anomalies("data/sample_logs.csv")
