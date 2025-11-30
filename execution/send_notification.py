import subprocess
import sys

def send_notification(title, message):
    """
    Sends a macOS system alert (modal) using osascript.
    """
    # 'display alert' creates a modal dialog that steals focus/requires interaction.
    # We escape double quotes in the message/title to avoid AppleScript syntax errors.
    safe_title = title.replace('"', '\\"')
    safe_message = message.replace('"', '\\"')
    
    script = f'display alert "{safe_title}" message "{safe_message}" as critical giving up after 5'
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        print(f"Alert sent: {title} - {message}")
    except subprocess.CalledProcessError as e:
        print(f"Error sending alert: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send_notification.py <title> <message>")
        sys.exit(1)
    
    title = sys.argv[1]
    message = sys.argv[2]
    send_notification(title, message)
