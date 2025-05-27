import os

from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from src.utils.path_helper import get_resource_path
from src.logic.availability_manager import AvailabilityManager
from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.menubar import MenuBarManager
from src.data.db_connector import DatabaseConnector
from src.ui.pages.calendar_page import CalendarPage
from src.ui.pages.volunteer_page import VolunteerPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Load the ui file - dinamic route
        UI_PATH = get_resource_path("src/ui/main_window.ui")
        uic.loadUi(UI_PATH, self)

        # Set icon and title window
        self.setWindowTitle("Turnomatic")
        ICON_PATH = get_resource_path("assets/images/300_trans.ico")
        self.setWindowIcon(QIcon(ICON_PATH))

        # Load stylesheet
        self.apply_stylesheet("light")
        # self.apply_stylesheet("dark")

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


    def apply_stylesheet(self, theme="light"):
        theme_file = f"assets/styles/{theme}.qss"
        QSS_PATH = get_resource_path(theme_file)
        with open(QSS_PATH, "r") as f:
            self.setStyleSheet(f.read())


    def closeEvent(self, event):
        """Se ejecuta cuando se cierra la ventana"""
        print("Cerrando conexión con la base de datos...")
        self.db.close_connection()  # Close the connection
        event.accept()  # Let close the window


if __name__ == "__main__":
    db = DatabaseConnector()
    am = AvailabilityManager(db)
    vm = VolunteerManager(db)
    mw = MainWindow()
    cp = CalendarPage(mw, db)

    periods = am.get_confirmed_availability_by_id_volunteer(1, True)
    # periods = am.get_availability_by_id_volunteer(1)

    print(periods)  # debug
    print(len(periods))


    # print(cp._get_availability_index(periods, 55)) # 1


    am.db.close_connection()