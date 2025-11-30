import csv
import os
from datetime import datetime

LOG_FILE = "activity_log.csv"

def generate_daily_report():
    """
    Analyzes the log file and generates a daily report.
    """
    if not os.path.exists(LOG_FILE):
        return "No activity log found."
        
    total_entries = 0
    productive_entries = 0
    wasteful_entries = 0
    
    # Simple analysis for today
    today = datetime.now().strftime("%Y-%m-%d")
    
    with open(LOG_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Timestamp"].startswith(today):
                total_entries += 1
                if row["Classification"] == "Productive":
                    productive_entries += 1
                elif row["Classification"] == "Wasteful":
                    wasteful_entries += 1
    
    if total_entries == 0:
        return "No data for today."
        
    score = (productive_entries / total_entries) * 10
    
    report = f"""
    Daily Performance Report ({today})
    ---------------------------------
    Total Blocks: {total_entries}
    Productive: {productive_entries}
    Wasteful: {wasteful_entries}
    
    Discipline Score: {score:.1f}/10
    """
    
    return report

if __name__ == "__main__":
    print(generate_daily_report())
