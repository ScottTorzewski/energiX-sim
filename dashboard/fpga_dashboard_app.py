import streamlit as st
import pandas as pd
import altair as alt

# Page config
st.set_page_config(page_title="EnergiX Risk Dashboard", layout="wide")

# Load and process data
@st.cache_data
def load_data():
    df = pd.read_csv("results.txt")
    df.columns = ["Test", "Temperature", "Power", "Vibration", "Class", "Risk Score"]
    return df

df = load_data()

# High-risk threshold
RISK_THRESHOLD = 700
high_risk_df = df[df["Risk Score"] > RISK_THRESHOLD]

# Header
st.title("⚡ EnergiX Inference Results Dashboard")
st.markdown("This dashboard visualizes inference results from the FPGA simulation pipeline.")

# Main table
st.subheader("📊 Full Inference Results")
st.dataframe(df.style.highlight_max(axis=0, subset=["Risk Score"]))

# High-risk analysis
st.subheader("🚨 High-Risk Predictions")
st.metric(label="Total High-Risk Cases", value=len(high_risk_df))

if not high_risk_df.empty:
    st.dataframe(high_risk_df)

    # Bar chart of high-risk classes
    st.subheader("Class Distribution Among High-Risk Predictions")
    chart = alt.Chart(high_risk_df).mark_bar().encode(
        x=alt.X('Class:O', title='Fault Class'),
        y=alt.Y('count():Q', title='Count'),
        tooltip=['Class', 'count()']
    ).properties(width=600)
    st.altair_chart(chart)
else:
    st.info("No high-risk predictions found.")

# Footer
st.markdown("---")
st.markdown("✅ Powered by Vivado + Streamlit | Scott Torzewski 2025")

