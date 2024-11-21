import ctypes
from ctypes import wintypes
import time
import threading
import os

import dearpygui.dearpygui as dpg

def init_ui(title=str, message=str, version=str):
    dpg.create_context()

    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    window_width = 450
    window_height = 300
    x_pos = int((screen_width - window_width) / 2)
    y_pos = int((screen_height - window_height) / 2)

    with dpg.window(label="", no_title_bar=True, no_move=True, no_resize=True, no_close=True, width=window_width, height=window_height):
        with dpg.node_editor(tag="node_editor", width=window_width - 30, height=window_height - 55):
            with dpg.node(label="Startup Time (ms)", pos=(40, 40)):
                with dpg.node_attribute(label="Time", attribute_type=dpg.mvNode_Attr_Static):
                    dpg.add_text(default_value=f"{int(time.time() * 1000)} ms")

            with dpg.node(label="Current Time", pos=(270, 50)):
                with dpg.node_attribute(label="Time", attribute_type=dpg.mvNode_Attr_Static):
                    dpg.add_text(default_value=time.strftime("%H:%M:%S"))

            with dpg.node(label="Current Roblox Version", pos=(30, 150)):
                with dpg.node_attribute(label="Info", attribute_type=dpg.mvNode_Attr_Static):
                    dpg.add_text(default_value=version)

            with dpg.node(label="", pos=(250, 150)):
                with dpg.node_attribute(label="Message", attribute_type=dpg.mvNode_Attr_Static):
                    dpg.add_text(default_value=message)

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

threading.Thread(target=init_ui, args=("RoStrap", "Loading Roblox...", "version-xxxxxxxxxxxx"), daemon=True).start()
time.sleep(5)
close_program()