import win32gui
import win32con
import win32api
import dearpygui.dearpygui as dpg
import time
import threading

def start_loading_animation(title=str, message=str):
    dpg.create_context()

    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    viewport_width, viewport_height = 1000, 800
    viewport_x, viewport_y = (screen_width - viewport_width) // 2, (screen_height - viewport_height) // 2

    dpg.create_viewport(title='overlay', width=viewport_width, height=viewport_height, x_pos=viewport_x, y_pos=viewport_y, always_on_top=True, decorated=False, clear_color=[0.0, 0.0, 0.0, 0.0])
    dpg.set_viewport_always_top(True)
    dpg.setup_dearpygui()

    window_width, window_height = 250, 75
    window_x, window_y = (viewport_width - window_width) // 2, (viewport_height - window_height) // 2

    with dpg.window(label=title, tag='main_win', no_resize=True, no_close=True, width=window_width, height=window_height, pos=(window_x, window_y)):
        dpg.add_text(message)
        progress_bar = dpg.add_progress_bar(label="Loading", width=window_width - 20, height=20)

    dpg.show_viewport()

    # Make the window transparent
    hwnd = win32gui.FindWindow(None, "overlay")
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

    def pulse_progress_bar():
        while True:
            for i in range(101):
                dpg.set_value(progress_bar, i / 100.0)
                time.sleep(0.02)
            dpg.set_value(progress_bar, 0.0)
            time.sleep(0.25)

    threading.Thread(target=pulse_progress_bar, daemon=True).start()
    dpg.start_dearpygui()
    return dpg

def close_program():
    dpg.stop_dearpygui()