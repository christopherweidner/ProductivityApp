import subprocess
import sys

def kill_process(process_name):
    """
    Kills a process by its name using pkill.
    """
    try:
        # -i for case insensitive
        subprocess.run(["pkill", "-i", process_name], check=True)
        print(f"Successfully killed process: {process_name}")
        return True
    except subprocess.CalledProcessError:
        print(f"Process not found or could not be killed: {process_name}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python kill_process.py <process_name>")
        sys.exit(1)
    
    process_name = sys.argv[1]
    kill_process(process_name)
