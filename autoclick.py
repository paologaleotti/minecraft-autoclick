import time
import threading
from pynput.keyboard import Listener, Key
import win32gui
import win32ui
import win32con
import win32api


delay = 0.4  # ogni quanto cliccare (in secondi)

start_stop_key = Key.home  # tasto per avviare o fermare il click
exit_key = Key.end  # tasto per uscire dal programma


def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            global code
            if "Minecraft" in win32gui.GetWindowText(hwnd):
                code = hwnd
                print("FINESTRA RILEVATA: " +
                      win32gui.GetWindowText(hwnd) + " [" + str(hwnd) + "]")
                print("-----------------------")
    win32gui.EnumWindows(winEnumHandler, None)


class ClickMouse(threading.Thread):
    def __init__(self, delay):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        print("Programma chiuso...")
        self.stop_clicking()
        self.program_running = False

    def run(self):
        print("Programma partito!")
        print("Premi [HOME] per avviare/fermare l'autoclick")
        print("Premi [END] per chiudere il programma")

        while self.program_running:
            while self.running:
                win32api.SendMessage(
                    hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON)
                time.sleep(0.05)
                win32api.SendMessage(
                    hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON)

                time.sleep(self.delay)
            time.sleep(0.1)


click_thread = ClickMouse(delay)
list_window_names()

if 'code' in globals():  # se esiste la variabile code (ovvero se esiste la finestra di minecraft)
    click_thread.start()
else:
    print("Minecraft non rilevato.")
    click_thread.exit()
    exit(0)

hwnd = code
win = win32ui.CreateWindowFromHandle(hwnd)


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            print("-- autoclick FERMATO")
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
            print("-- autoclick PARTITO")
    elif key == exit_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
