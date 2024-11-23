import ctypes
import threading
import time
import psutil
import sys
import subprocess
from pathlib import Path

from UI.node_map import NODE_MAP
from utils.enums import ENUMS
from utils.uri_handler import URI
from utils.addon_handler import AddonHandler
from utils.config import config

roblox_folder = Path(ENUMS.PATHS["ROBLOX_PATH"])
if not config.read()["roblox_version"] in [folder.name for folder in roblox_folder.iterdir() if folder.is_dir()]:
    print("Invalid Roblox version. Please run the installer first.")
    installer_path = Path(__file__).parent / "installer.py"
    threading.Thread(target=subprocess.run, args=([sys.executable, installer_path],), kwargs={"check": True}, daemon=True).start()
    sys.exit(1)

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

    threading.Thread(target=subprocess.run, args=(cmd,), kwargs={"check": True}, daemon=True).start()
    time.sleep(2.5)
    addons = AddonHandler._get_addons()
    if addons:
        for addon in addons:
            addon_path = Path(ENUMS.PATHS["ADDONS_PATH"]) / addon
            if addon_path.suffix == ".exe":
                threading.Thread(target=subprocess.run, args=(addon_path,), kwargs={"check": True}, daemon=True).start()
            elif addon_path.suffix == ".py":
                threading.Thread(target=subprocess.run, args=([sys.executable, addon_path],), kwargs={"check": True}, daemon=True).start()
            else:
                print(f"Skipping non-executable addon: {addon}")
        print("All addons have been executed.")
    else:
        print("No addons found.")

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