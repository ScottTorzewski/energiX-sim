import os
import json
import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.multiclass import unique_labels
from joblib import dump

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_IN = os.path.join(BASE_DIR, "data", "edge_events.json")
MODEL_OUT = os.path.join(BASE_DIR, "ml_engine", "rf_model.joblib")
OUTPUT_JSON = os.path.join(BASE_DIR, "data", "ml_results.json")

# Simulated data generation
failure_map = {
    "🔥 High temperature": "motor_overheat",  # Reduced occurrence to not overrepresent motor_overheat
    "⚡ High power draw": "overload",
    "🔧 Abnormal vibration (avg)": "bearing_wear",
    "🔥 High temperature|⚡ High power draw": "critical_overload",
    "⚡ High power draw|🔧 Abnormal vibration (avg)": "bearing_wear_with_power_issue",
    "🔥 High temperature|🔧 Abnormal vibration (avg)": "thermal_mechanical_failure",
    "🔥 High temperature|⚡ High power draw|🔧 Abnormal vibration (avg)": "impending_failure",
    "⚡ High power draw|🔥 High temperature": "power_issue_with_overheating",  # Added more failure types
    "🔧 Abnormal vibration (avg)": "vibration_failure"  # Another type of failure
}

def infer_label(alerts):
    key = "|".join(sorted(alerts))
    return failure_map.get(key, random.choice(list(failure_map.values())))

# Load edge events
with open(DATA_IN, "r") as f:
    data = json.load(f)

# Build dataframe
raw_rows = []
for x in data:
    # Randomize temperature, power, and vibration thresholds for each node
    temp_threshold = random.uniform(70, 80)
    power_threshold = random.uniform(80, 100)
    vibration_threshold = random.uniform(0.5, 1.0)

    raw_rows.append({
        "node_id": x["node_id"],
        "temperature": x["raw"]["temperature"],
        "power_draw": x["raw"]["power_draw"],
        "vibration": x["raw"]["vibration"],
        "alerts": "|".join(sorted(x["alerts"])),
        "label": infer_label(x["alerts"])
    })

df = pd.DataFrame(raw_rows)

# Encode labels
le = LabelEncoder()
df["label_enc"] = le.fit_transform(df["label"])

# Train ML model
X = df[["temperature", "power_draw", "vibration"]]
y = df["label_enc"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=20, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

labels_used = unique_labels(y_test, model.predict(X_test))
print("✅ Model trained. Accuracy report:")
print(classification_report(y_test, model.predict(X_test), target_names=le.inverse_transform(labels_used)))

# Save model
dump((model, le), MODEL_OUT)

# Group by node_id and average readings
df_grouped = df.groupby("node_id").mean(numeric_only=True).reset_index()

# Inference simulation
results = []
for _, row in df_grouped.iterrows():
    input_data = pd.DataFrame([[row["temperature"], row["power_draw"], row["vibration"]]], columns=["temperature", "power_draw", "vibration"])
    prediction = model.predict(input_data)[0]
    risk_score = model.predict_proba(input_data)[0][prediction]

    # Add random variability to risk score calculation
    risk_score += random.uniform(-0.05, 0.05)  # Small fluctuation to simulate more variety

    results.append({
        "node_id": int(row["node_id"]),
        "temperature": round(row["temperature"], 2),
        "power_draw": round(row["power_draw"], 2),
        "vibration": round(row["vibration"], 2),
        "predicted_label": le.inverse_transform([prediction])[0],
        "risk_score": round(float(risk_score), 3)
    })

# Save results
with open(OUTPUT_JSON, "w") as f:
    json.dump(results, f, indent=2)

print(f"📦 Inference complete. Results saved to: {OUTPUT_JSON}")
