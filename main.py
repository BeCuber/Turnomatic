from PyQt5.QtWidgets import QApplication
import sys
from src.ui.main_window import MainWindow



# Initialize the App
app = QApplication(sys.argv)
UIWindow = MainWindow()
app.exec_()