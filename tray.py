import pyautogui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings
import os
import pyWinhook as pyHook
import threading
import setting
import gpt_main
import time


app = QApplication([])

app.setQuitOnLastWindowClosed(False)

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
icon = QIcon(os.path.join(CURRENT_DIRECTORY, "icon1.jpeg"))

settingW = None
settings = QSettings("settings.ini", QSettings.IniFormat)
top = int(settings.value("top"))


def open_gpt():
    global settingW
    settings = QSettings("settings.ini", QSettings.IniFormat)
    selected_text = QApplication.clipboard().text()
    settings.setValue("text", selected_text)
    settingW = QtWidgets.QDialog()
    ui = gpt_main.Ui_Form()
    if top:  # Window will be set always on top only when this flag is true
        settingW.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    ui.setupUi(settingW)
    settingW.exec_()
    settingW = None


def open_setting():
    global settingW
    if settingW is not None:
        settingW.close()
    settingW = QtWidgets.QDialog()
    settingW.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    ui = setting.Ui_Form()
    ui.setupUi(settingW)
    settingW.exec_()


def doubleClickFunction(reason):
    if reason == QSystemTrayIcon.DoubleClick:
        open_gpt()


def tray_open_gpt():
    global settingW
    if settingW is not None:
        settingW.close()
    open_gpt()


tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

menu = QMenu()
option1 = QAction("GPT")
option1.setIcon(QIcon("fb.png"))
option2 = QAction("Setting")
option2.setIcon(QIcon("settings.png"))
menu.addAction(option1)
menu.addAction(option2)
option1.triggered.connect(tray_open_gpt)
option2.triggered.connect(open_setting)

quit = QAction("Quit")
quit.setIcon(QIcon("out.png"))


tray.setContextMenu(menu)
tray.activated.connect(doubleClickFunction)


def OnKeyboardEvent(event):
    if event.Key.lower() == "a" and event.Alt and not event.Injected:
        global settingW
        if settingW is not None:
            settingW.close()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.hotkey('ctrl', 'c')
        print(QApplication.clipboard().text())
        open_gpt()
    return True


hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()


def pump_messages():
    quit.triggered.connect(app.quit)
    menu.addAction(quit)


thread = threading.Thread(target=pump_messages)
thread.start()

app.exec_()
