import os

from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from src.ui.widgets.menubar import MenuBarManager
from src.data.db_connector import DatabaseConnector
from src.ui.pages.calendar_page import CalendarPage
from src.ui.pages.volunteer_page import VolunteerPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Load the ui file - dinamic route
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        UI_PATH = os.path.join(BASE_DIR, "./main_window.ui")
        uic.loadUi(UI_PATH, self)

        # Set icon and title window
        self.setWindowTitle("Turnomatic")
        ICON_PATH = os.path.join(BASE_DIR, "../../assets", "images", "window_icon.ico")
        self.setWindowIcon(QIcon(ICON_PATH))

        # Connect to database
        self.db = DatabaseConnector()

        # Define widgets
        self.stacked_widget = self.findChild(QStackedWidget, "stackedWidget")

        # Initialize pages
        self.calendar_page = CalendarPage(self, self.db)
        self.volunteer_page = VolunteerPage(self, self.db)

        # Add pages to stack
        self.stacked_widget.addWidget(self.calendar_page)
        self.stacked_widget.addWidget(self.volunteer_page)
 
        # Config menu manager
        self.menu_manager = MenuBarManager(self, self.stacked_widget, self.calendar_page, self.volunteer_page)
        
        # Show the app
        self.show()

    def closeEvent(self, event):
        """Se ejecuta cuando se cierra la ventana"""
        print("Cerrando conexión con la base de datos...")
        self.db.close_connection()  # Close the connection
        event.accept()  # Let close the window
