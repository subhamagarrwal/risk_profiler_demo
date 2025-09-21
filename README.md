# Fintellect Risk Profiler

A comprehensive financial risk profiling system that uses AI to assess investor risk tolerance and provide personalized portfolio recommendations with backtesting analytics.

## Architecture

### Backend (FastAPI)
- **`/profile`** - Converts conversational answers into structured risk profiles using LLM
- **`/weights`** - Calculates optimal asset allocation with guardrails
- **`/analytics`** - Runs backtesting and performance analysis

### Frontend (React)
- **Risk Assessment** - 3-question conversational interface  
- **Portfolio Configuration** - Interactive weight selection with variants
- **Analytics Dashboard** - Charts and performance metrics visualization

### Core Modules
- `get_json.py` - Risk profiling and portfolio optimization logic
- `backtest.py` - Backtesting and performance metrics functions
- `RiskProfiler.Modelfile` - Ollama model configuration

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama with llama3.1:8b-instruct-q4_0 model

### 1. Setup Ollama Model
```bash
# Install the model
ollama pull llama3.1:8b-instruct-q4_0

# Create the risk-profiler model
ollama create risk-profiler -f RiskProfiler.Modelfile

# Verify model is running
ollama list
```

### 2. Start Backend API

**Windows (using batch file):**
```bash
# Double-click start_backend.bat or run:
start_backend.bat
```

**Mac/Linux (using shell script):**
```bash
# Make script executable and run:
chmod +x start_backend.sh
./start_backend.sh
```

**Manual startup (all platforms):**
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the API server
python main.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

### 3. Start Frontend

**Windows (using batch file):**
```bash
# Double-click start_frontend.bat or run:
start_frontend.bat
```

**Mac/Linux (using shell script):**
```bash
# Make script executable and run:
chmod +x start_frontend.sh
./start_frontend.sh
```

**Manual startup (all platforms):**
```bash
cd frontend

# Install dependencies  
npm install

# Start development server
npm start
```

Frontend will be available at http://localhost:3000

## API Endpoints

### POST `/profile`
Generate risk profile from user conversational answers.

**Request:**
```json
{
  "answers": {
    "answer1": "I'd hold but feel stressed",
    "answer2": "Prefer steady growth, some risk okay", 
    "answer3": "Down payment in ~3 years"
  }
}
```

**Response:**
```json
{
  "profile": {...},
  "axes": {"loss_aversion": 0.50, "liquidity": 0.75, ...},
  "score": 62.5,
  "label": "Balanced Builder"
}
```

### POST `/weights`
Calculate investment weights with guardrails.

**Request:**
```json
{
  "label": "Balanced Builder",
  "variant": "baseline", 
  "axes": {"loss_aversion": 0.50, ...}
}
```

**Response:**
```json
{
  "weights": {"equity": 0.60, "bonds": 0.35, "cash": 0.05},
  "explanations": ["Using baseline allocation..."]
}
```

### POST `/analytics`  
Run backtesting analytics and generate performance comparisons.

**Request:**
```json
{
  "user_weights": {"equity": 0.60, "bonds": 0.35, "cash": 0.05},
  "label": "Balanced Builder",
  "axes": {...}
}
```

**Response:**
```json
{
  "portfolios": [...],
  "growth_chart": {...},
  "drawdown_chart": {...},
  "comparisons": [...]
}
```

## Features

### Risk Profiling
- AI-powered conversational assessment
- 5-axis risk scoring (time horizon, loss aversion, liquidity, income stability, knowledge)
- Composite scoring with descriptive labels

### Portfolio Optimization  
- Policy-based asset allocation
- Guardrail enforcement (liquidity needs, loss aversion caps)
- Multiple variants (defensive, baseline, aggressive)

### Backtesting & Analytics
- Historical performance simulation using Indian market ETFs
- Key metrics: CAGR, volatility, max drawdown, recovery time
- Interactive charts and comparative analysis
- Plain-language explanations

## Troubleshooting

### Backend Issues
- **Ollama connection errors**: Ensure Ollama is running on http://localhost:11434
- **Import errors**: Check that `get_json.py` and `backtest.py` are in parent directory
- **Data fetch errors**: Verify internet connection for yfinance data

### Frontend Issues  
- **API connection errors**: Ensure backend is running on port 8000
- **CORS errors**: Backend includes CORS middleware for localhost:3000
- **Chart rendering issues**: Charts use Chart.js - ensure all dependencies are installed

## Data Sources

The system uses Indian market ETFs for backtesting:
- **Equity**: NIFTYBEES.NS (Nifty 50 ETF)
- **Bonds**: NETFLTGILT.NS (Government Securities ETF) 
- **Cash**: LIQUIDBEES.NS (Liquid Fund ETF)

Historical data from 2014-present via Yahoo Finance API.
