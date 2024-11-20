import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
import sys
import subprocess
from plyer import notification
import threading
import time
import psutil
from pathlib import Path

from UI.preset.loading import start_loading_animation, close_program
from utils.uri_handler import parse_roblox_uri, construct_launch_command


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
if not is_admin():
    print("Please run this script as an administrator.")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit(0)

def launch_roblox(uri=None):
    threading.Thread(target=start_loading_animation, args=("RoStrap","Loading Roblox...") ,daemon=True).start()
    def roblox_check():
        while True:
            if any(proc.name() == "RobloxPlayerBeta.exe" for proc in psutil.process_iter()):
                time.sleep(0.5)
                close_program()
                break
            time.sleep(1)
    
    threading.Thread(target=roblox_check, daemon=True).start()
    cmd = construct_launch_command(uri)
    print(f"Executing: {' '.join(cmd)}")

    subprocess.run(cmd, check=True)

def main():
    icon_path = str(Path(__file__).parent / "assets/logo.ico")
    if len(sys.argv) == 1:
        print("No URI provided. Launching Roblox desktop app...")
        launch_roblox()

    elif len(sys.argv) == 2:
        uri = sys.argv[1]

        try:
            params = parse_roblox_uri(uri)
            print(params)
            
            #notification.notify(
            #    title = "RoStrap",
            #    message = f"Joining server",
            #    timeout = 10,
            #    app_icon = icon_path,
            #    app_name = "RoStrap"
            #)
            print(construct_launch_command(uri))
            launch_roblox(uri)
        except ValueError as e:
            print(f"Error parsing URI: {e}")
            sys.exit(1)

    else:
        print("Usage: python bootstrapper.py [roblox-uri]")
        sys.exit(1)

if __name__ == "__main__":
    main()