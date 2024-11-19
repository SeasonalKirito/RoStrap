from pathlib import Path
import requests

def get_latest_version():
    url = "https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["clientVersionUpload"]

PATHS = {
    "ROBLOX_PLAYER_PATH": str(Path.home() / f"AppData/Local/Roblox/Versions/{get_latest_version()}/RobloxPlayerBeta.exe"),
    "ROBLOX_BOOTSTRAPPER_PATH": str(Path.home() / f"AppData/Local/Roblox/Versions/{get_latest_version()}/RobloxPlayerLauncher.exe")
}