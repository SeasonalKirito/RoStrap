import ctypes
from ctypes import wintypes
import time

import dearpygui.dearpygui as dpg

dpg.create_context()

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Calculate the position to center the window
window_width = 450
window_height = 200
x_pos = int((screen_width - window_width) / 2)
y_pos = int((screen_height - window_height) / 2)

with dpg.window(label="", no_title_bar=True, no_move=True, no_resize=True, no_close=True, width=434.6, height=211):
    dpg.add_text("Loading, please wait...", pos=(12.5, 50))
    progress_bar = dpg.add_progress_bar(label="Loading", width=window_width - 40, height=25, pos=(12.5, 100))

dpg.create_viewport(title='RoStrap', width=window_width, height=window_height, x_pos=x_pos, y_pos=y_pos, resizable=False, always_on_top=True)

def enable_dark_mode(hwnd):
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    set_window_attribute.argtypes = [wintypes.HWND, wintypes.DWORD, wintypes.LPCVOID, wintypes.DWORD]
    set_window_attribute.restype = ctypes.c_long
    value = ctypes.c_int(2)
    set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))

dpg.setup_dearpygui()
dpg.show_viewport()

hwnd = ctypes.windll.user32.FindWindowW(None, "RoStrap")
enable_dark_mode(hwnd)
dpg.start_dearpygui()
dpg.destroy_context()

def update_loading_bar():
    while True:
        for i in range(101):
            dpg.set_value("loading_bar", i / 100.0)
            time.sleep(0.05)