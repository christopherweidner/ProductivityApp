import subprocess
import json

def get_active_window():
    """
    Returns the application name and window title of the active window using AppleScript.
    """
    script = '''
    global frontApp, frontAppName, windowTitle
    
    set windowTitle to ""
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set frontAppName to name of frontApp
        tell process frontAppName
            try
                set windowTitle to name of front window
            end try
        end tell
    end tell
    
    return "{\\"app\\": \\"" & frontAppName & "\\", \\"title\\": \\"" & windowTitle & "\\"}"
    '''
    
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        # The output is a JSON string, but osascript might return it with quotes around it if not careful,
        # or we might need to parse it manually if it's not perfect JSON.
        # However, the script constructs a JSON string.
        
        # Sometimes osascript returns things like: "{\"app\": \"Code\", \"title\": \"foo\"}"
        # We need to parse that.
        
        # Let's try to parse it directly.
        try:
            data = json.loads(output)
            return data
        except json.JSONDecodeError:
            # Fallback if something went wrong with the JSON construction in AppleScript
            print(f"Error decoding JSON from AppleScript: {output}")
            return {"app": "Unknown", "title": "Unknown"}
            
    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}")
        return {"app": "Unknown", "title": "Unknown"}

if __name__ == "__main__":
    info = get_active_window()
    print(json.dumps(info, indent=2))
