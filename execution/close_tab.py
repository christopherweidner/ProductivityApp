import subprocess
import sys

def close_tab():
    """
    Simulates Cmd+W to close the current tab/window using AppleScript.
    """
    script = '''
    tell application "System Events"
        keystroke "w" using command down
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        print("Sent Cmd+W keystroke.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error sending keystroke: {e}")
        return False

if __name__ == "__main__":
    close_tab()
