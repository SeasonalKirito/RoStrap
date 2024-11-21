import threading
import time

from UI.node_map import NODE_MAP
from utils.enums import get_latest_version

NODES = [
    {"title": "Startup Time (ms)", "description": f"{int(time.time() * 1000)} ms", "position": (40, 40)},
    {"title": "Current Time", "description": time.strftime("%H:%M:%S"), "position": (270, 50)},
    {"title": "Current Roblox Version", "description": get_latest_version(), "position": (30, 150)},
    {"title": "", "description": "Installing", "position": (250, 150)},
]
threading.Thread(target=NODE_MAP.init_ui, args=("RoStrap", NODES), daemon=True).start()
time.sleep(5)
NODE_MAP.close_program()