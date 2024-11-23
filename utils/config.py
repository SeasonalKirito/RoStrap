import json
from pathlib import Path

class config():
    CONFIG_FILE = "settings.json"

    def read(config_file=None):
        if config_file is None:
            config_file = Path(__file__).parent.parent / config.CONFIG_FILE

        try:
            with open(config_file, "r") as file:
                config_data = json.load(file)
                return config_data
        except FileNotFoundError:
            print("[-] Config file not found. Please create a config.json file.")
            return None
        except json.JSONDecodeError:
            print("[-] Config file is not a valid JSON file.")
            return None
    
    def write(key, value):
        config_data = config.read()
        if config_data is not None:
            config_data[key] = value
            with open(config.CONFIG_FILE, "w") as file:
                json.dump(config_data, file, indent=4)
            print("[+] Config file has been updated.")