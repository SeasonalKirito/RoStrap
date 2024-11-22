import ctypes
import threading
import time
import psutil
import sys
import subprocess

from UI.node_map import NODE_MAP
from utils.enums import ENUMS
from utils.uri_handler import URI

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
if not is_admin():
    print("Please run this script as an administrator.")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit(0)

#ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

NODES = [
    {"title": "State", "description": "Starting Roblox...", "position": (140, 100)},
]

def launch_roblox(uri=None):
    threading.Thread(target=NODE_MAP.init_ui, args=("RoStrap", NODES), daemon=True).start()
    def roblox_check():
        while True:
            if any(proc.name() == "RobloxPlayerBeta.exe" for proc in psutil.process_iter()):
                time.sleep(1.5)
                NODE_MAP.close_program()
                break
            time.sleep(1)
    
    threading.Thread(target=roblox_check, daemon=True).start()
    cmd = URI.construct_launch_command(uri)
    print(f"Executing: {' '.join(cmd)}")

    subprocess.run(cmd, check=True)

def main():
    if len(sys.argv) == 1:
        print("No URI provided. Launching Roblox desktop app...")
        launch_roblox()

    elif len(sys.argv) == 2:
        uri = sys.argv[1]

        try:
            print(URI.parse_roblox_uri(uri))
            print(URI.construct_launch_command(uri))

            launch_roblox(uri)
        except ValueError as e:
            print(f"Error parsing URI: {e}")
            sys.exit(1)

    else:
        print("Usage: python bootstrapper.py [roblox-uri]")
        sys.exit(1)

if __name__ == "__main__":
    main()