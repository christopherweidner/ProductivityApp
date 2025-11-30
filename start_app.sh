#!/bin/bash

# Kill any existing instances
pkill -f "python server.py"
pkill -f "vite"

echo "Starting Deep Work App..."

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Start Backend
echo "Starting Backend Server..."
python server.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start Frontend
echo "Starting Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!

echo "App running!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Open http://localhost:5173 in your browser."

# Wait for user to exit
wait
