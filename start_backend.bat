@echo off
cd /d "C:\Users\subha\Desktop\Projects\risk-profiler\Fintellect_SIH\backend"
echo Starting FastAPI backend server...
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000