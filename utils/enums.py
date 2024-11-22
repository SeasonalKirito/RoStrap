from pathlib import Path
import requests

from utils.config import config

class ENUMS:
    def get_latest_version():
        url = "https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["clientVersionUpload"]

    PATHS = {
        "ROBLOX_PLAYER_PATH": str(Path(__file__).parent.parent / f"Roblox/{config.read()["roblox_version"]}/RobloxPlayerBeta.exe"),
        "ROBLOX_PATH": str(Path(__file__).parent.parent / "Roblox"),
        "ROSTRAP_PATH": str(Path(__file__).parent.parent),

        "ADDONS_PATH": str(Path(__file__).parent.parent / "addons")
    }