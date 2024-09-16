import sys
import subprocess

def open_file(path: str):
        """ 调用系统默认程序打开文件 """
        if sys.platform == "win32":
            subprocess.Popen(["start", path], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])