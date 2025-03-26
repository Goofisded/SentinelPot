# --------------------
# Dependencies
# --------------------
import socketserver
import threading
import requests
import logging
import datetime
import json
import time
import random
import os

# --------------------
# Variables
# --------------------
WEBHOOK_URL = "webhook here"

HOST = "0.0.0.0"  # ip here
PORT = 2222       # you can change port if you want
MAX_EMBED = 2048
SESSION_LOG = "honeypot_sessions.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

VIRTUAL_FS = {
    "/": {
        "type": "dir",
        "stuff": {
            "Documents": {"type": "dir", "stuff": {"resume.txt": {"type": "file", "data": ""}}},
            "Downloads": {"type": "dir", "stuff": {}},
            "secret.txt": {"type": "file", "data": "database"},
            "readme.md": {"type": "file", "data": "# Goof"}
        }
    }
}

# --------------------
# Main
# --------------------
def shout_to_discord(ip, when, what_they_did):
    cmd_log = "\n".join(what_they_did) if what_they_did else "Nothin' happened"
    desc = (f"**IP:** {ip}\n"
            f"**When:** {when}\n"
            f"**What they tried:**\n```\n{cmd_log}\n```")
    
    if len(desc) > MAX_EMBED:
        desc = desc[:MAX_EMBED - 3] + "..."
    
    discord_msg = {
        "title": "🚨 Honeypot Activity!",
        "description": desc,
        "color": 15158332,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }
    payload = {"embeds": [discord_msg]}
    
    try:
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if response.status_code != 204:
            logging.error("Discord hook failed: " + response.text)
    except Exception as e:
        logging.error("Discord oopsie: " + str(e))

def keep_record(ip, timestamp, commands):
    try:
        with open(SESSION_LOG, "a") as log:
            log.write(f"\n--- New session @ {timestamp} ---\n")
            log.write(f"IP: {ip}\nCommands:\n - " + "\n - ".join(commands) + "\n")
    except Exception as e:
        logging.error("Log file trouble: " + str(e))

def cook_response(cmd, filesystem, current_path):
    cmd = cmd.strip()
    if not cmd:
        return "", current_path, filesystem

    if cmd.lower() in ["exit", "quit"]:
        return "Connection closed!", current_path, filesystem

    if cmd == "ls":
        current = filesystem.get(current_path, {})
        return "  ".join(current.get("stuff", {}).keys()) or "", current_path, filesystem

    if cmd.startswith("pwd"):
        return current_path, current_path, filesystem

    if cmd.startswith("cd "):
        target = cmd.split(maxsplit=1)[1]
        if target == "..":
            current_path = os.path.dirname(current_path.rstrip("/")) or "/"
        else:
            current = filesystem.get(current_path, {})
            if target in current.get("stuff", {}):
                if current["stuff"][target]["type"] == "dir":
                    current_path = os.path.join(current_path, target)
                else:
                    return f"Not a folder: {target}", current_path, filesystem
            else:
                return f"cd: {target} not found", current_path, filesystem
        return "", current_path, filesystem

    if cmd.startswith("cat "):
        filename = cmd.split(maxsplit=1)[1]
        current = filesystem.get(current_path, {})
        if filename in current.get("stuff", {}):
            return current["stuff"][filename].get("data", ""), current_path, filesystem
        return f"cat: {filename} MIA", current_path, filesystem

    if cmd == "whoami":
        return "root", current_path, filesystem

    if cmd.startswith("uname"):
        return "Linux 4.15.0-72-generic #81-Ubuntu SMP 2025 x86_64 GNU/Linux", current_path, filesystem

    return f"Unknown command: {cmd}", current_path, filesystem

class ConnectionHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client_ip = self.client_address[0]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cmd_history = []
        
        filesystem = {"/": VIRTUAL_FS["/"].copy()}
        current_path = "/"
        
        self.request.sendall(b"SSH-2.0-OpenSSH_7.2p2\r\n")
        self.request.sendall(b"login: ")
        username = self.request.recv(1024).decode().strip()
        self.request.sendall(b"Password: ")
        self.request.recv(1024)
        
        self.request.sendall(f"Hey {username}! Type 'exit' to bail\r\n".encode())
        
        while True:
            self.request.sendall(b"Goof$ ")
            try:
                cmd = self.request.recv(1024).decode().strip()
                if not cmd:
                    break
                cmd_history.append(cmd)
                
                time.sleep(random.uniform(0.1, 0.5))
                
                response, current_path, filesystem = cook_response(cmd, filesystem, current_path)
                self.request.sendall(response.encode() + b"\r\n")
                
                if cmd.lower() in ["exit", "quit"]:
                    break
            except:
                break
        
        keep_record(client_ip, timestamp, cmd_history)
        shout_to_discord(client_ip, timestamp, cmd_history)

def fire_up():
    logging.info(f"Pot's hot on {HOST}:{PORT}")
    server = socketserver.ThreadingTCPServer((HOST, PORT), ConnectionHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Powering down...")
        server.shutdown()

if __name__ == "__main__":
    fire_up()