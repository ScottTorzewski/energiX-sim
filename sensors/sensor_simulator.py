import os
import json
import csv
import random
from datetime import datetime, timedelta

# Constants
NUM_NODES = 20
DURATION_MINUTES = 60  # 1 hour of data
INTERVAL_SECONDS = 60  # one data point per minute

# Output path 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

json_path = os.path.join(DATA_DIR, "simulated_data.json")
csv_path = os.path.join(DATA_DIR, "simulated_data.csv")

# Generate timestamps
start_time = datetime.now()
timestamps = [
    (start_time + timedelta(seconds=i * INTERVAL_SECONDS)).isoformat()
    for i in range(DURATION_MINUTES)
]

# Simulate data
data = []

for t in timestamps:
    for node_id in range(1, NUM_NODES + 1):
        # Randomize failure thresholds for each data point
        temp_threshold = random.uniform(70, 80)  # Random threshold for temperature
        power_threshold = random.uniform(80, 100)  # Random threshold for power draw
        vibration_threshold = random.uniform(0.5, 1.0)  # Random threshold for vibration

        # Simulate node data
        entry = {
    "timestamp": t,
    "node_id": node_id,
    "temperature": round(random.uniform(20, 80), 2),
    "vibration": round(random.uniform(0, 1), 3),
    "power_draw": round(random.uniform(10, 100), 2),
    "humidity": round(random.uniform(30, 90), 2),
    "airflow": round(random.uniform(0.1, 2.0), 2),
    "fan_speed": round(random.uniform(500, 5000), 1),
    "node_status": random.choice(['operational', 'maintenance', 'critical'])  # Added random status to simulate different failure modes
}
        data.append(entry)

# Write JSON
with open(json_path, "w") as jf:
    json.dump(data, jf, indent=2)

# Write CSV
with open(csv_path, "w", newline="") as cf:
    writer = csv.DictWriter(cf, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

print(f"✅ Simulated data saved to:\n- {json_path}\n- {csv_path}")
