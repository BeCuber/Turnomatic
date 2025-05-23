import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

def get_resource_path(relative_path):
    """
        Returns the absolute path to the resources, so it works both in development and when the app is packaged with PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS # PyInstaller extrae aquí
    else:
        base_path = ROOT_DIR
    return os.path.normpath(os.path.join(base_path, relative_path))