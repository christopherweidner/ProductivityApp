# Enforce Focus Directive

## Goal
Ruthlessly eliminate distractions.

## Tools
- `execution/kill_process.py`: Terminate specific applications.
- `execution/manage_hosts.py`: Block access to websites.
- `execution/send_notification.py`: Scold the user.

## Process
1. **Identify**: Check if the active window is on the "Wasteful" list or classified as such by LLM.
2. **Block**:
    - If it's a browser tab on a blacklisted site (if possible to detect) or a known distraction app (Discord, Steam), KILL IT.
    - Ensure `/etc/hosts` blocks common distraction domains (twitter.com, youtube.com, reddit.com).
3. **Intervene**:
    - Send a notification with a stoic, commanding message.
    - Log the infraction.
