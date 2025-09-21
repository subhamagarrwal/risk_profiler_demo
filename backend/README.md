# FastAPI Risk Profiler Backend

## Setup
```bash
pip install fastapi uvicorn pydantic jsonschema yfinance pandas numpy matplotlib requests
```

## Run
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints
- POST /profile - Generate risk profile from user answers
- POST /weights - Get investment weights from profile
- POST /analytics - Run backtesting and get performance analytics

## Dependencies
- Requires Ollama service running on http://localhost:11434
- Uses existing get_json.py and backtest.py modules