# Minimal Quant Developer Assignment Solution

## Setup
- Requires Python 3 and Flask, numpy
- Run: `python app.py`
- Open http://127.0.0.1:5000/  in browser

## Methodology
- Backend ingests tick data via `/tick` POST endpoint
- Stores last 1000 ticks in memory
- Computes mean price and z-score
- Frontend displays analytics and basic alert if z-score > 2
- Download analytics as CSV

## ChatGPT Usage
- ChatGPT was used to generate code and this README, following assignment instructions for a solution.

## Architecture Diagram
See `architecture.drawio` (placeholder, not detailed)