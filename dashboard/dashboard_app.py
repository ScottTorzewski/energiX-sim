import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="EnergiX Inference Comparison", layout="wide")
st.title("📊 EnergiX: ML vs FPGA Inference Comparison")

# Load Data
ml_file = "dashboard/ml_results.json"
fpga_file = "dashboard/results.txt"

@st.cache_data
def load_data():
    # Load ML Results
    with open(ml_file, "r") as f:
        ml_data = json.load(f)
    ml_df = pd.DataFrame(ml_data)

    # Load FPGA Results
    fpga_df = pd.read_csv(fpga_file)
    fpga_df.rename(columns={"Temp": "temperature_raw", "Power": "power_draw_raw", "Vib": "vibration_raw"}, inplace=True)
    fpga_df["temperature"] = fpga_df["temperature_raw"] / 100
    fpga_df["power_draw"] = fpga_df["power_draw_raw"] / 100
    fpga_df["vibration"] = fpga_df["vibration_raw"] / 1000
    fpga_df["node_id"] = fpga_df["Test"]

    # Merge
    merged = pd.merge(ml_df, fpga_df, on="node_id", suffixes=("_ml", "_fpga"))
    return merged

data = load_data()

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filter Nodes")
    node_ids = st.multiselect("Select Node IDs", options=sorted(data.node_id.unique()), default=sorted(data.node_id.unique()))
    risk_threshold = st.slider("Minimum Risk Score (ML)", 0.0, 1.0, 0.0, 0.01)
    delta_threshold = st.slider("Max Risk Score Delta", 0.0, 1.0, 1.0, 0.01)

# Apply filters
filtered = data[data["node_id"].isin(node_ids)]
filtered = filtered[filtered["risk_score"] >= risk_threshold]
filtered["risk_delta"] = abs(filtered["risk_score"] - (filtered["Risk"] / 1000))
filtered = filtered[filtered["risk_delta"] <= delta_threshold]

# Display
st.markdown("### 🔬 Node Inference Comparison Table")
st.dataframe(
    filtered[[
        "node_id",
        "temperature_ml", "power_draw_ml", "vibration_ml", "predicted_label", "risk_score",
        "temperature_fpga", "power_draw_fpga", "vibration_fpga", "Class", "Risk",
        "risk_delta"
    ]].round(3),
    use_container_width=True
)

# Risk Score Histogram
st.markdown("### 📈 Risk Score Comparison")
col1, col2 = st.columns(2)
with col1:
    st.subheader("ML Risk Score per Node")
    st.bar_chart(filtered.set_index("node_id")["risk_score"])
with col2:
    st.subheader("FPGA Risk Score per Node")
    st.bar_chart(filtered.set_index("node_id")["Risk"] / 1000)

# Extra Analysis
st.markdown("### 📊 Risk Score Distribution Comparison")
fig, ax = plt.subplots()
ax.hist(filtered["risk_score"], bins=15, alpha=0.6, label="ML Risk", color="skyblue")
ax.hist(filtered["Risk"] / 1000, bins=15, alpha=0.6, label="FPGA Risk", color="orange")
ax.set_xlabel("Risk Score")
ax.set_ylabel("Frequency")
ax.set_title("Distribution of Risk Scores")
ax.legend()
st.pyplot(fig)

st.caption("Compare predicted risk scores from ML (Python) and FPGA (Hardware Logic) paths.")
