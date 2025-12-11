# Swing Options Algo — Production Build

A modular options trade simulator and simple engines.

## Quick start (local)
1. Create & activate virtualenv:
   python3 -m venv .venv
   source .venv/bin/activate

2. Install deps:
   pip install -r requirements.txt

3. Run:
   python simulator.py -c swing_options/config/production.yaml

## Quick start (docker)
docker build -t swing-options .
docker run --rm swing-options

## Run tests
pytest -q

