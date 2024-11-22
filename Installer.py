import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
if not is_admin():
    print("Please run this script as an administrator.")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit(0)

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

import threading
import time
from plyer import notification
from pathlib import Path
import subprocess

from UI.node_map import NODE_MAP
from utils.enums import ENUMS
from utils.registry_handler import WindowsRegistry
from utils.install_handler import Installer
from utils.config import config


icon_path = str(Path(__file__).parent / "assets/logo.ico")

NODES = [
    {"title": "Startup Time (ms)", "description": f"{int(time.time() * 1000) % 1000} ms", "position": (60, 50)},
    {"title": "Current Time", "description": time.strftime("%H:%M:%S"), "position": (250, 50)},
    {"title": "Current Roblox Version", "description": ENUMS.get_latest_version(), "position": (30, 150)},
    {"title": "State", "description": "Installing...", "position": (250, 150)},
]
threading.Thread(target=NODE_MAP.init_ui, args=("RoStrap", NODES), daemon=True).start()

python_executable = sys.executable
WindowsRegistry.register_player(python_executable, f"\"{ENUMS.PATHS['ROSTRAP_PATH']}\\Bootstrapper.py\" \"%1\"")
notification.notify(
    title = "RoStrap",
    message = f"Installed Registry implementations {ENUMS.PATHS['ROSTRAP_PATH']}\\Bootstrapper.py",
    timeout = 5,
    app_icon = icon_path,
    app_name = "RoStrap"
)

time.sleep(1)

try:
    Installer.install(config.read()['roblox_version'], True)
except Exception as e:
    print(e)
    
notification.notify(
    title = "RoStrap",
    message = f"Installed Roblox {config.read()['roblox_version']}",
    timeout = 10,
    app_icon = icon_path,
    app_name = "RoStrap"
)

time.sleep(1)

bootstrapper_path = Path(ENUMS.PATHS['ROSTRAP_PATH']) / "Bootstrapper.py"
if bootstrapper_path.exists():
    subprocess.Popen([python_executable, str(bootstrapper_path)])
else:
    notification.notify(
        title="RoStrap",
        message="RobloxPlayerBeta.exe not found. (WTFFFFFF 💀)",
        timeout=5,
        app_icon=icon_path,
        app_name="RoStrap"
    )
time.sleep(0.25)
NODE_MAP.close_program()