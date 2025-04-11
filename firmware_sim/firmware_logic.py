import os
import json
import random
import time
from collections import deque

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_IN = os.path.join(BASE_DIR, "data", "simulated_data.json")
DATA_OUT = os.path.join(BASE_DIR, "data", "edge_events.json")

# Load sensor data
with open(DATA_IN, "r") as f:
    sensor_data = json.load(f)

# Rolling history for average calculations (simulated firmware buffer)
vibration_history = {}
TEMP_THRESHOLD = 75
POWER_THRESHOLD = 90
VIBRATION_THRESHOLD = 0.8
ROLLING_WINDOW = 5

event_log = []

for entry in sensor_data:
    node = entry["node_id"]

    # Initialize buffer if needed
    if node not in vibration_history:
        vibration_history[node] = deque(maxlen=ROLLING_WINDOW)

    vibration_history[node].append(entry["vibration"])
    avg_vib = sum(vibration_history[node]) / len(vibration_history[node])

    alerts = []

    # Simulated "firmware" logic
    if entry["temperature"] > TEMP_THRESHOLD:
        alerts.append("🔥 High temperature")
    if entry["power_draw"] > POWER_THRESHOLD:
        alerts.append("⚡ High power draw")
    if avg_vib > VIBRATION_THRESHOLD:
        alerts.append("🔧 Abnormal vibration (avg)")

    status = random.choice(['operational', 'maintenance', 'critical'])

    if alerts:
        event_log.append({
            "timestamp": entry["timestamp"],
            "node_id": node,
            "alerts": alerts,
            "rolling_avg_vibration": round(avg_vib, 3),
            "raw": entry
        })

# Save processed events
with open(DATA_OUT, "w") as f:
    json.dump(event_log, f, indent=2)

print(f"✅ Firmware-style edge logic complete. Events saved to: {DATA_OUT}")
print(f"📦 {len(event_log)} events triggered from {len(sensor_data)} records.")
