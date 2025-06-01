from PyQt5.QtWidgets import QApplication
import sys
from src.ui.main_window import MainWindow


# Initialize the App
app = QApplication(sys.argv)
# app.setStyle('Fusion')
UIWindow = MainWindow()
app.exec_()