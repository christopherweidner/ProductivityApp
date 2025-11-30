import csv
import os
from datetime import datetime

LOG_FILE = "activity_log.csv"

def log_activity(timestamp, app_name, window_title, classification):
    """
    Logs the activity to a CSV file.
    """
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "App", "Title", "Classification"])
        
        writer.writerow([timestamp, app_name, window_title, classification])

if __name__ == "__main__":
    log_activity(datetime.now().isoformat(), "TestApp", "TestTitle", "Productive")
