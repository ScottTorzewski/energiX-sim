import streamlit as st
import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_SENSOR = os.path.join(BASE_DIR, "data", "simulated_data.json")
DATA_EDGE = os.path.join(BASE_DIR, "data", "edge_events.json")
DATA_ML = os.path.join(BASE_DIR, "data", "ml_results.json")

st.set_page_config(layout="wide")
st.title("energiX | Industrial Node Risk Monitoring Dashboard")

# Load files
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

sensor_data = load_json(DATA_SENSOR)
edge_data = load_json(DATA_EDGE)
ml_data = load_json(DATA_ML)

# Sidebar controls
st.sidebar.header("🔎 Filter")
min_risk = st.sidebar.slider("Minimum Risk Score", 0.0, 1.0, 0.5, 0.01)

# Display total nodes + high risk
df_ml = pd.DataFrame(ml_data)
df_high_risk = df_ml[df_ml["risk_score"] >= min_risk]

st.metric("📡 Total Nodes", len(df_ml))
st.metric("⚠️ High Risk Nodes", len(df_high_risk))

# Show table
st.subheader("🔍 Risk Summary Table")
st.dataframe(df_high_risk.sort_values("risk_score", ascending=False), use_container_width=True)

# Detailed node viewer
st.subheader("📊 Node Risk Breakdown")
selected = st.selectbox("Choose a node to inspect", df_ml.index)

with st.expander("Sensor Readings"):
    st.json(sensor_data[selected])

with st.expander("Firmware Alerts"):
    st.json(edge_data[selected])

with st.expander("ML Inference"):
    st.json(ml_data[selected])

# Chart
st.subheader("📈 Risk Score Distribution")
st.bar_chart(df_ml["risk_score"])