import ctypes
from ctypes import wintypes
import threading
import os

from utils.config import config
from utils.enums import ENUMS

import dearpygui.dearpygui as dpg

class MENU:
    def init_ui(title=str):
        dpg.create_context()

        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        window_width = 450
        window_height = 300
        x_pos = int((screen_width - window_width) / 2)
        y_pos = int((screen_height - window_height) / 2)

        with dpg.window(label="", no_title_bar=True, no_move=True, no_resize=True, no_close=True, width=window_width, height=window_height):
            def save_all():
                print("Saving all settings...")
                with open("ClientSettings.json", "w") as file:
                    file.write(dpg.get_value(text_editor))

                if dpg.get_value(bootstrapper_title) != "":
                    config.write("bootstrapper_title", dpg.get_value(bootstrapper_title))

                if dpg.get_value(roblox_version) == "Live":
                    config.write("roblox_version", ENUMS.get_latest_version())
                elif dpg.get_value(roblox_version) != "":
                    config.write("roblox_version", dpg.get_value(roblox_version))

            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Save Settings", callback=save_all)

            with dpg.tab_bar():
                with dpg.tab(label="Misc"):
                    with dpg.group(horizontal=True):
                        dpg.add_text("Bootstrapper Title:")
                        bootstrapper_title = dpg.add_input_text(label="", hint=config.read()["bootstrapper_title"], width=200)
                    with dpg.group(horizontal=True):
                        dpg.add_text("Roblox Channel:")
                        roblox_version = dpg.add_input_text(label="", hint=config.read()["roblox_version"], width=200)

                with dpg.tab(label="FFlags"):
                    text_editor = dpg.add_input_text(multiline=True, width=420, height=205)
                    if os.path.exists("ClientSettings.json"):
                        with open("ClientSettings.json", "r") as file:
                            client_settings_code = file.read()
                    else:
                        client_settings_code = ""
                    dpg.set_value(text_editor, client_settings_code)

                with dpg.tab(label="Other"):
                    dpg.add_text("Other Settings")
            

        dpg.create_viewport(title=title, width=window_width, height=window_height, x_pos=x_pos, y_pos=y_pos, resizable=False, always_on_top=True)

        def enable_dark_mode(hwnd):
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            set_window_attribute.argtypes = [wintypes.HWND, wintypes.DWORD, wintypes.LPCVOID, wintypes.DWORD]
            set_window_attribute.restype = ctypes.c_long
            value = ctypes.c_int(2)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))

        dpg.setup_dearpygui()
        dpg.show_viewport()

        hwnd = ctypes.windll.user32.FindWindowW(None, title)
        enable_dark_mode(hwnd)

        
        dpg.start_dearpygui()
        return dpg

    def close_program():
        dpg.stop_dearpygui()

ui_thread = threading.Thread(target=MENU.init_ui, args=("RoStrap",), daemon=True)
ui_thread.start()
ui_thread.join()