# React Risk Profiler Frontend

A modern React.js frontend for the Fintellect Risk Profiler application.

## Features

- **Risk Assessment Form**: 3-question conversational interface
- **Portfolio Configuration**: Interactive weight selection with variants
- **Analytics Dashboard**: Charts and performance metrics
- **Responsive Design**: Works on desktop and mobile devices

## Setup

### Prerequisites
- Node.js 16+ and npm
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The application will open at http://localhost:3000

## Components

### RiskAssessment.js
- Collects user answers to risk tolerance questions
- Calls `/profile` API endpoint
- Shows loading state during LLM processing

### PortfolioConfiguration.js
- Displays generated risk profile
- Allows selection of portfolio variants (defensive/baseline/aggressive)
- Shows asset allocation with explanations

### AnalyticsDashboard.js
- Backtesting results and performance metrics
- Interactive charts for growth and drawdown
- Portfolio comparison table

## API Integration

The frontend communicates with the FastAPI backend through:
- `POST /profile` - Generate risk profile
- `POST /weights` - Calculate portfolio weights  
- `POST /analytics` - Run backtesting analysis

## Build

```bash
npm run build
```

Creates optimized production build in `build/` folder.