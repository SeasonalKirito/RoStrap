import ctypes
from ctypes import wintypes
import time
import threading
import os

import dearpygui.dearpygui as dpg

class NODE_MAP:
    def init_ui(title=str, nodes=list):
        dpg.create_context()

        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        window_width = 450
        window_height = 300
        x_pos = int((screen_width - window_width) / 2)
        y_pos = int((screen_height - window_height) / 2)

        with dpg.window(label="", no_title_bar=True, no_move=True, no_resize=True, no_close=True, width=window_width, height=window_height):
            with dpg.node_editor(tag="node_editor", width=window_width - 31, height=window_height - 53):
                for node in nodes:
                    with dpg.node(label=node["title"], pos=node["position"]):
                        with dpg.node_attribute(label=node["title"], attribute_type=dpg.mvNode_Attr_Static):
                            dpg.add_text(default_value=node["description"])

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

        
        threading.Thread(target=dpg.start_dearpygui(), daemon=True).start()
        return dpg

    def close_program():
        dpg.stop_dearpygui()