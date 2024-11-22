import winreg
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WindowsRegistry:
    ROBLOX_PLACE_KEY = "Roblox.Place"

    @staticmethod
    def register_protocol(key, name, handler, handler_param="%1"):
        handler_args = f'"{handler}" {handler_param}'
        logging.info(f"Registering protocol: {key} with handler: {handler_args}")

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{key}") as uri_key:
            with winreg.CreateKey(uri_key, "DefaultIcon") as uri_icon_key:
                with winreg.CreateKey(uri_key, "shell\\open\\command") as uri_command_key:
                    if winreg.QueryValue(uri_key, "") is None:
                        winreg.SetValue(uri_key, "", winreg.REG_SZ, f"URL: {name} Protocol")
                        winreg.SetValue(uri_key, "URL Protocol", winreg.REG_SZ, "")
                        logging.info(f"Set URL Protocol for {key}")

                    if winreg.QueryValue(uri_command_key, "") != handler_args:
                        winreg.SetValue(uri_icon_key, "", winreg.REG_SZ, handler)
                        winreg.SetValue(uri_command_key, "", winreg.REG_SZ, handler_args)
                        logging.info(f"Set command for {key}")

    @staticmethod
    def register_player(handler, handler_param="-player \"%1\""):
        logging.info("Registering player protocols")
        WindowsRegistry.register_protocol("roblox", "Roblox", handler, handler_param)
        WindowsRegistry.register_protocol("roblox-player", "Roblox", handler, handler_param)

    @staticmethod
    def unregister(key):
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{key}")
            logging.info(f"Unregistered {key}")
        except FileNotFoundError:
            logging.warning(f"Failed to unregister {key}: Key not found")
        except Exception as ex:
            logging.error(f"Failed to unregister {key}: {ex}")