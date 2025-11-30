#!/bin/bash

# Kill any existing instances
pkill -f "python server.py"
pkill -f "vite"

echo "Starting Deep Work App..."

# Start Backend
echo "Starting Backend Server..."
source .venv/bin/activate
python server.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start Frontend
echo "Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo "App running!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Open http://localhost:5173 in your browser."

# Wait for user to exit
wait
