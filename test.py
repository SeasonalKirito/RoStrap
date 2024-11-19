import sys
import subprocess
import re
from pathlib import Path
import requests
import os
import ctypes
from plyer import notification

def get_latest_version():
    url = "https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["clientVersionUpload"]

latest_version = get_latest_version()
ROBLOX_PLAYER_PATH = str(Path.home() / f"AppData/Local/Roblox/Versions/{latest_version}/RobloxPlayerBeta.exe")
ROBLOX_BOOTSTRAPPER_PATH = str(Path.home() / f"AppData/Local/Roblox/Versions/{latest_version}/RobloxPlayerLauncher.exe")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def parse_roblox_uri(uri):
    """
    Parses a roblox-player URI into a dictionary of parameters.
    """

    if uri.startswith("roblox-player:"):
        param_stream = uri[len("roblox-player:"):]

    elif uri.startswith("roblox://"):
        param_stream = uri[len("roblox://"):]

    else:
        raise ValueError("Invalid Roblox URI")
    
    params = {}
    for item in param_stream.split("+"):
        if ":" in item:
            key, value = item.split(":", 1)
            params[key] = value
            
        else:
            params[item] = True
    return params

def construct_launch_command(uri=None):
    """
    Constructs the command to launch Roblox.
    """
    if uri:
        cmd = [ROBLOX_PLAYER_PATH, uri]
    else:
        cmd = [ROBLOX_PLAYER_PATH, "--app"]
    return cmd

def launch_roblox(uri=None):
    """
    Launches Roblox with the appropriate command.
    """
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
            notification.notify(
                title = "RoStrap",
                message = f"Joining server",
                timeout = 10,
                app_icon = icon_path,
                app_name = "RoStrap"
            )
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