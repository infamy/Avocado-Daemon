from doit.tools import LongRunning

DOIT_CONFIG = {'default_tasks': [],}

def task_pyinstaller():
    #cmd = ["pyinstaller.exe --onefile --icon=avocado.ico avocado.py"]
    cmd = ["pyinstaller.exe --onefile avocado.py"]
    return {'actions': cmd,}

def task_installer():
    return {'actions': ['"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi']}