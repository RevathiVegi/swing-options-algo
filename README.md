# 📈 Swing Options Algo
A modular, configurable backtesting framework for Index Options Swing Trading
This project provides a robust Python engine for researching and backtesting swing-style options trading strategies on Indian indices such as NIFTY, BANKNIFTY, SENSEX, and select equities.
It includes tools for:
Rule-driven signal generation
Clean PnL normalization
Single & batch backtests
Trade logging and parquet export
Automated HTML reporting

## 🚀 Features
✔️ Smart PnL Normalization
Automatically converts messy trade inputs into clean pnl_rupees floats, handling:
Strings like "1,234.50"
Negative numbers in parentheses (123)
Missing or partial fields
Entry/exit/points-based fallbacks

✔️ Configurable Strategy Framework
Rules are driven by YAML files — no direct code editing required.

✔️ Batch Backtesting
Run multiple symbols or time ranges with one command.

✔️ Detailed HTML Reports
Combines summary tables, trade logs & visual insights.

## 🛠️Installation
1️⃣ Clone the repository
git clone https://github.com/RevathiVegi/swing-options-algo.git
cd swing-options-algo

2️⃣ Create and activate a virtual environment

## Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate


## Windows:
python -m venv .venv
.venv\Scripts\activate

## 3️⃣ Install dependencies
pip install -r requirements.txt

## ▶️ Running Simulations
Single Backtest
python run_sim.py --config config.example.yaml

## Batch Backtest
python run_batch.py --config config.example.yaml --out out_batch

## Generate an HTML Report
python make_report.py \
  --summary backtest_data/backtest_summary.csv \
  --trades_dir backtest_data/trades \
  --parquet_dir backtest_data/parquet \
  --out report.html

## 🧪 Testing
Place your unit tests inside:
tests/


## Run them with:
pytest

## 📂 Project Structure
swing-options-algo/
│
├── engine.py               # Core backtest logic
├── run_sim.py              # Single backtest runner
├── run_batch.py            # Batch backtest runner
├── make_report.py          # HTML report generator
├── utils.py                # Helpers (includes PnL normalize fn)
├── config.example.yaml     # Example configuration
│
├── backtest_data/          # Output datasets
│   ├── trades/
│   ├── parquet/
│   └── backtest_summary.csv
│
└── tests/                  # Test suite (optional)


✔️ Modular Architecture

Easy to extend with new strategy logic or indicators.
