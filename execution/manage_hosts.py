import sys
import subprocess

HOSTS_PATH = "/etc/hosts"
REDIRECT_IP = "127.0.0.1"
START_MARKER = "### DEEP WORK START ###"
END_MARKER = "### DEEP WORK END ###"

def block_domains(domains):
    """
    Adds domains to /etc/hosts to block them.
    Requires sudo access.
    """
    try:
        with open(HOSTS_PATH, "r") as f:
            content = f.read()
        
        if START_MARKER in content:
            print("Deep Work block already active.")
            return

        block_content = f"\n{START_MARKER}\n"
        for domain in domains:
            block_content += f"{REDIRECT_IP} {domain}\n"
            block_content += f"{REDIRECT_IP} www.{domain}\n"
        block_content += f"{END_MARKER}\n"

        # We need to write this as root. Using tee.
        # Construct the full new content is safer but harder with simple sudo tee if we want to append/insert.
        # Actually, appending is easiest.
        
        cmd = f"echo '{block_content}' | sudo tee -a {HOSTS_PATH}"
        subprocess.run(cmd, shell=True, check=True)
        print("Domains blocked.")
        
        # Flush DNS cache
        subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"], check=False)

    except Exception as e:
        print(f"Error blocking domains: {e}")

def unblock_domains():
    """
    Removes the Deep Work block from /etc/hosts.
    Requires sudo access.
    """
    try:
        with open(HOSTS_PATH, "r") as f:
            lines = f.readlines()
        
        new_lines = []
        skip = False
        for line in lines:
            if START_MARKER in line:
                skip = True
            if not skip:
                new_lines.append(line)
            if END_MARKER in line:
                skip = False
        
        # Write back using sudo tee
        new_content = "".join(new_lines)
        
        # This is a bit tricky with sudo. We can write to a temp file and then mv it?
        # Or just echo the whole thing.
        
        # Let's use a temp file approach for safety
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(new_content)
            tmp_path = tmp.name
            
        subprocess.run(["sudo", "mv", tmp_path, HOSTS_PATH], check=True)
        subprocess.run(["sudo", "chmod", "644", HOSTS_PATH], check=True)
        
        print("Domains unblocked.")
        # Flush DNS cache
        subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"], check=False)

    except Exception as e:
        print(f"Error unblocking domains: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_hosts.py <block|unblock> [domain1 domain2 ...]")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "block":
        domains = sys.argv[2:]
        if not domains:
            # Default list
            domains = ["twitter.com", "facebook.com", "instagram.com", "reddit.com", "youtube.com"]
        block_domains(domains)
    elif mode == "unblock":
        unblock_domains()
    else:
        print("Invalid mode. Use 'block' or 'unblock'.")
