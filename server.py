import subprocess
import sys
import os
import csv
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for frontend

AGENT_PROCESS = None
LOG_FILE = "activity_log.csv"
STATUS_FILE = "agent_status.json"

@app.route('/api/start', methods=['POST'])
def start_agent():
    global AGENT_PROCESS
    if AGENT_PROCESS and AGENT_PROCESS.poll() is None:
        return jsonify({"status": "Already running"}), 200
    
    try:
        # Run unbuffered to see output immediately if needed
        AGENT_PROCESS = subprocess.Popen(
            [sys.executable, "-u", "deep_work_agent.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return jsonify({"status": "Started", "pid": AGENT_PROCESS.pid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_agent():
    global AGENT_PROCESS
    if AGENT_PROCESS and AGENT_PROCESS.poll() is None:
        AGENT_PROCESS.terminate()
        try:
            AGENT_PROCESS.wait(timeout=5)
        except subprocess.TimeoutExpired:
            AGENT_PROCESS.kill()
        AGENT_PROCESS = None
        
        # Clean up status file
        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)
            
        return jsonify({"status": "Stopped"}), 200
    return jsonify({"status": "Not running"}), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    global AGENT_PROCESS
    is_running = AGENT_PROCESS is not None and AGENT_PROCESS.poll() is None
    
    status_data = {
        "running": is_running,
        "mode": "IDLE",
        "time_remaining": 0
    }
    
    if is_running and os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                file_data = json.load(f)
                status_data.update(file_data)
        except Exception:
            pass # Ignore read errors (race conditions)
            
    return jsonify(status_data), 200

@app.route('/api/logs', methods=['GET'])
def get_logs():
    if not os.path.exists(LOG_FILE):
        return jsonify([]), 200
    
    logs = []
    try:
        with open(LOG_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append(row)
        # Return last 100 logs
        return jsonify(logs[-100:]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Server on port 5001...")
    app.run(port=5001, debug=True)
