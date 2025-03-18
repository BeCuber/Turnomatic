from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import os

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Load the ui file - dinamic route
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        UI_PATH = os.path.join(BASE_DIR, "main_window.ui")
        uic.loadUi(UI_PATH, self)


        # Define our widgets


        # Click the button
        #self.button.clicked.connect(self.add_window)

        # Show the app
        self.show()

    def add_window(self):
        
        pass