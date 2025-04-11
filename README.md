# EnergiX Sim Suite 🚀

**A full-stack, PC-simulated smart energy inference system that compares Python ML and FPGA-based decision tree logic.**

## 💡 Features
- Sensor simulation pipeline with realistic data
- ML model (RandomForest) trained and evaluated
- FPGA logic (SystemVerilog) for decision tree inference
- Dynamic risk scoring in hardware
- Fully integrated Streamlit dashboard

## 🔧 Technologies
- SystemVerilog (Vivado)
- Python (pandas, scikit-learn)
- Streamlit
- Matplotlib
- JSON/CSV data pipelines

## 📊 Inference Comparison
Visual dashboard comparing:
- Python ML predictions
- FPGA hardware logic results
- Risk score delta analysis

## 📎 Reports
- Timing Slack: 0.1 ns @ 100 MHz ✔️

## 🔄 How to Run
```bash
streamlit run dashboard/dashboard_app.py
