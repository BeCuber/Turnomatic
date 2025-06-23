from PyQt5.QtWidgets import QApplication
import sys

from src.controller.app_controller import AppController


# Initialize the App
app = QApplication(sys.argv)
controller = AppController()
UIWindow = controller.get_main_window()
app.exec_()