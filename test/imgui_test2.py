import ctypes
from ctypes import wintypes

import dearpygui.dearpygui as dpg

dpg.create_context()

# Set dark theme

# Create a single window without a title bar, non-movable, non-resizable, and non-closable
with dpg.window(label="", no_title_bar=True, no_move=True, no_resize=True, no_close=True, width=350, height=100):
    dpg.add_text("This is the top window")
    dpg.add_loading_indicator()

with dpg.window(label="", no_title_bar=True, no_move=True, no_resize=True, no_close=True, width=350, height=200, pos=(0, 100)):
    dpg.add_text("This is the bottom window")
    with dpg.child_window(width=330, height=150, autosize_x=True, autosize_y=True):
        with dpg.child_window(width=330, height=150, autosize_x=True, autosize_y=True) as console_window:
            console = dpg.add_text("", wrap=330)

dpg.create_viewport(title='RoStrap', width=350, height=300)

# Function to enable dark mode for the window
def enable_dark_mode(hwnd):
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    set_window_attribute.argtypes = [wintypes.HWND, wintypes.DWORD, wintypes.LPCVOID, wintypes.DWORD]
    set_window_attribute.restype = ctypes.c_long
    value = ctypes.c_int(2)
    set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))

dpg.setup_dearpygui()
dpg.show_viewport()

# Get the window handle and enable dark mode
hwnd = ctypes.windll.user32.FindWindowW(None, "RoStrap")
enable_dark_mode(hwnd)

# Function to log messages to the console
def log_to_console(message):
    current_text = dpg.get_value(console)
    new_text = current_text + "\n" + message
    dpg.set_value(console, new_text)
    dpg.set_y_scroll(console_window, dpg.get_y_scroll_max(console_window))

# Example usage of logging to the console
log_to_console("This is a log message.")
log_to_console("Another log message.")

dpg.start_dearpygui()
dpg.destroy_context()
