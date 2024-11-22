import threading
import time

from UI.node_map import NODE_MAP
from utils.enums import ENUMS

NODES = [
    {"title": "Startup Time (ms)", "description": f"{int(time.time() * 1000) % 1000} ms", "position": (60, 50)},
    {"title": "Current Time", "description": time.strftime("%H:%M:%S"), "position": (250, 50)},
    {"title": "Current Roblox Version", "description": ENUMS.get_latest_version(), "position": (30, 150)},
    {"title": "State", "description": "Installing...", "position": (250, 150)},
]
threading.Thread(target=NODE_MAP.init_ui, args=("RoStrap", NODES), daemon=True).start()
time.sleep(5)
NODE_MAP.close_program()