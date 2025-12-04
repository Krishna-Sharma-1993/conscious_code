"""
utils.py
Helper utilities for reading/writing JSON, simple logging, and small helpers.
"""
import json
from pathlib import Path
from datetime import datetime

def load_json(path):
    with open(path) as f:
        return json.load(f)

def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def simple_report_path():
    return f"reports/report_{int(datetime.utcnow().timestamp())}.html"
