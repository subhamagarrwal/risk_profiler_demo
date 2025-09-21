#!/bin/bash
cd "$(dirname "$0")/frontend"
echo "Installing frontend dependencies..."
npm install
echo ""
echo "Starting React frontend server..."
npm start