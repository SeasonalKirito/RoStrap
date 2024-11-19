import win32gui
import win32con
import win32api
import dearpygui.dearpygui as dpg

import ctypes
from ctypes import c_int
dwm = ctypes.windll.dwmapi

dpg.create_context()

class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", c_int),
                ("cxRightWidth", c_int),
                ("cyTopHeight", c_int),
                ("cyBottomHeight", c_int)
               ]

# Get screen width and height
screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

# Set viewport size
viewport_width = 1000  # Increased width
viewport_height = 800  # Increased height

# Calculate position to center the viewport
viewport_x = (screen_width - viewport_width) // 2
viewport_y = (screen_height - viewport_height) // 2

dpg.create_viewport(title='overlay', width=viewport_width, height=viewport_height, x_pos=viewport_x, y_pos=viewport_y, always_on_top=True, decorated=False, clear_color=[0.0, 0.0, 0.0, 0.0])

dpg.set_viewport_always_top(True)
dpg.setup_dearpygui()

# Set window size
window_width = 250
window_height = 400

# Calculate position to center the window within the viewport
window_x = (viewport_width - window_width) // 2
window_y = (viewport_height - window_height) // 2

with dpg.window(label="Main Window", tag='main_win', no_resize=True, width=window_width, height=window_height, pos=(window_x, window_y), on_close=dpg.stop_dearpygui):
    dpg.add_button(label="Click Me")

dpg.show_viewport()

# Make the window transparent
hwnd = win32gui.FindWindow(None, "overlay")
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

dpg.start_dearpygui()
