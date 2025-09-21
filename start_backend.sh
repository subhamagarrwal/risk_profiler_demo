#!/bin/bash
cd "$(dirname "$0")/backend"
echo "Starting FastAPI backend server..."
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000