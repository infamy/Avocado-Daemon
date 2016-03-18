from bottle import *
import configobj
import os
import json
import platform
import re
import threading

version = 0.1


def check(user, pw):
    if user == settings['Server']['X-Token']:
        return True
    else:
        return False


@route("/")
def index():
    return "SmartController version %0.1f" % version


@route("/settings")
def showsettings():
    displaysettings = settings
    del displaysettings['Server']['X-Token']  # Hide the token
    return displaysettings


@get("/screen")
def screenstatus():
    if platform.system() == "Darwin":
        import subprocess
        if re.search('DevicePowerState"=([0-9])', subprocess.check_output(
                "ioreg -n IODisplayWrangler | grep -i IOPowerManagement",
                shell=True)).group(1) == "4":
            return {"screenison": True}
        else:
            return {"screenison": False}
    if platform.system() == "Windows":
        return {"screenison": "Unknown"}


@put("/screen/<state>")
@auth_basic(check)
def screenset(state):
    if platform.system() == "Darwin":
        import subprocess
        if state == "off":
            subprocess.call('pmset displaysleepnow', shell=True)
            return {"success": True}
        elif state == "on":
            subprocess.call('caffeinate -t 1 -u', shell=True)
            return {"success": True}

    if platform.system() == "Windows":
        def _winsetscreen(state):
            import win32gui
            import win32con
            from os import getpid, system
            from threading import Timer

            MONITOR_OFF = 2
            MONITOR_ON = -1

            def _winforceexit():
                pid = getpid()
                system('taskkill /pid %s /f' % pid)

            t = Timer(1, _winforceexit)
            t.start()
            SC_MONITORPOWER = 0xF170
            if state:
                win32gui.SendMessage(win32con.HWND_BROADCAST,
                                     win32con.WM_SYSCOMMAND,
                                     SC_MONITORPOWER,
                                     MONITOR_ON)
            else:
                win32gui.SendMessage(win32con.HWND_BROADCAST,
                                     win32con.WM_SYSCOMMAND,
                                     SC_MONITORPOWER,
                                     MONITOR_OFF)
            t.cancel()

        if state == "off":
            _winsetscreen(False)
            return {"success": True}
        elif state == "on":
            _winsetscreen(True)
            return {"success": True}


def startbrowser():
    if settings["Browser"]["AutoLaunch"]:
        if platform.system() == "Windows":
            if 'KioskMode' in settings['Browser'] and settings['Browser']['KioskMode']:
                subprocess.call(["C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "--kiosk", settings['Browser']['URL']])
            else:
                subprocess.call(["C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", settings['Browser']['URL']])


if __name__ == "__main__":
    settings = configobj.ConfigObj("settings.conf").dict()
    if 'Debug' in settings['Server'] and settings['Server']['Debug']:
        threading.Timer(1.25, startbrowser).start()
        run(host="0.0.0.0", debug=True)
    else:
        threading.Timer(1.25, startbrowser).start()
        run(host="0.0.0.0")
