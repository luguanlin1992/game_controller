import win32gui
import time
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def select_window():
    print('请在5秒内点击目标窗口...')
    time.sleep(5)
    hwnd = win32gui.GetForegroundWindow()
    rect = win32gui.GetWindowRect(hwnd)
    title = win32gui.GetWindowText(hwnd)
    return {
        'hwnd': hwnd,
        'title': title,
        'left': rect[0],
        'top': rect[1],
        'width': rect[2]-rect[0],
        'height': rect[3]-rect[1]
    }
