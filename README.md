# EnergiX Sim Suite 🚀

**A full-stack, PC-simulated smart energy inference system that compares Software-based ML inference (Python) and Hardware-based ML inference (FPGA-based decision tree logic).**

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

### Requirements
- This project requires **Python 3.11** due to compatibility issues with `scikit-learn`.  
  Python 3.13 is **not yet supported** and will cause installation errors.  
  👉 [Download Python 3.11 here](https://www.python.org/downloads/release/python-3110/)

### Setup Instructions

```bash
git clone https://github.com/ScottTorzewski/energiX-sim.git
cd energiX-sim
pip install -r requirements.txt
streamlit run dashboard/dashboard_app.py
