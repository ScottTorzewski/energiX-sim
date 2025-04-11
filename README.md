# EnergiX Sim Suite 🚀

**A full-stack, PC-simulated smart energy inference system that compares Software-based ML inference (Python) and Hardware-based ML inference (FPGA-based decision tree logic).**

---

## 🧭 System Overview

![EnergiX Flow Diagram](data/diagram.png)

---

## 💡 Features
- Sensor simulation pipeline with realistic data
- ML model (RandomForest) trained and evaluated
- FPGA logic (SystemVerilog) for decision tree inference
- Dynamic risk scoring in hardware
- Fully integrated Streamlit dashboard

---

## 🔧 Technologies
- SystemVerilog (Vivado)
- Python (Pandas, NumPy, scikit-learn)
- Streamlit
- Matplotlib
- JSON/CSV data pipelines

---

## 📊 Inference Comparison
Visual dashboard comparing:
- Python ML predictions
- FPGA hardware logic results
- Risk score delta analysis

---

![EnergiX Flow Diagram](data/diagram2.png)

---

## 🔄 How to Run
```bash
streamlit run dashboard/dashboard_app.py

