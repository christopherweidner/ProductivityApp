import time
import json
import sys
import os
from datetime import datetime
from execution.get_active_window import get_active_window
from execution.classify_activity import classify_activity
from execution.close_tab import close_tab
from execution.send_notification import send_notification
from execution.generate_persona_response import generate_persona_response
from execution.log_activity import log_activity

# Configuration
CHECK_INTERVAL = 5 # Check every 5 seconds for smoother timer updates
WORK_DURATION = 25 * 60 # 25 minutes
BREAK_DURATION = 5 * 60 # 5 minutes
STATUS_FILE = "agent_status.json"

def update_status(mode, time_remaining):
    """Writes the current status to a JSON file."""
    status = {
        "mode": mode,
        "time_remaining": time_remaining,
        "running": True
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f)

def main():
    print("Deep Work Agent Started. Pomodoro Mode.")
    
    mode = "WORK"
    timer = WORK_DURATION
    
    try:
        while True:
            # 0. Update Status File
            update_status(mode, timer)
            
            # 1. Timer Logic
            timer -= CHECK_INTERVAL
            if timer <= 0:
                if mode == "WORK":
                    mode = "BREAK"
                    timer = BREAK_DURATION
                    send_notification("Deep Work Complete", "Take a 5 minute break. You earned it.")
                else:
                    mode = "WORK"
                    timer = WORK_DURATION
                    send_notification("Break Over", "Back to work. Focus.")
                update_status(mode, timer)

            # 2. Get Active Window
            window_info = get_active_window()
            app_name = window_info.get("app", "Unknown")
            window_title = window_info.get("title", "Unknown")
            
            # 3. Classify Activity
            classification = classify_activity(app_name, window_title)
            timestamp = datetime.now().isoformat()
            
            print(f"[{timestamp}] [{mode}] {app_name} - {window_title} : {classification}")
            
            # 4. Log Activity
            log_activity(timestamp, app_name, window_title, classification)
            
            # 5. Intervene if Wasteful AND in WORK mode
            if mode == "WORK" and classification == "Wasteful":
                # Generate strict response
                message = generate_persona_response()
                
                # Notify (Alert)
                send_notification("Deep Work Alert", message)
                
                # Close Tab (Less aggressive than killing the app)
                close_tab()
            
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nDeep Work Session Ended.")
        # Clean up status file
        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)

if __name__ == "__main__":
    # Ensure we can import from execution module if running from root
    sys.path.append('.') 
    main()
