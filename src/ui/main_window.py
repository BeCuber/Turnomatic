from PyQt5.QtWidgets import QMainWindow, QCalendarWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import os
from src.data.db_connector import DatabaseConnector

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Load the ui file - dinamic route
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        UI_PATH = os.path.join(BASE_DIR, "main_window.ui")
        uic.loadUi(UI_PATH, self)
        # Establecer titulo de la ventana
        self.setWindowTitle("Turnomatic")
        # Establecer el icono de la ventana
        ICON_PATH = os.path.join(BASE_DIR, "../../assets", "images", "window_icon.ico")
        self.setWindowIcon(QIcon(ICON_PATH))


        # Define our widgets
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.volunteer_table = self.findChild(QTableWidget, "volunteerTableWidget")

        

        # Click day
        self.calendar.selectionChanged.connect(self.check_day)

        # Show the app
        self.show()

    def check_day(self):
        """Get selected date and update the volunteer list"""
        date_selected = self.calendar.selectedDate().toString("yyyy-MM-dd") # Formate compatible con SQLite
        db = DatabaseConnector()
        volunteers = db.check_volunteers_in_date(date_selected)
        db.close_connection()  

        # Limpiar la tabla antes de actualizar
        self.volunteer_table.setRowCount(0)

        # Llenar la tabla con los datos obtenidos
        for row_idx, v in enumerate(volunteers):
            self.volunteer_table.insertRow(row_idx)
            self.volunteer_table.setItem(row_idx, 0, QTableWidgetItem(v[0]))  # Name
            self.volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v[1]))  # Lastname
            self.volunteer_table.setItem(row_idx, 2, QTableWidgetItem("Yes" if v[2] else "No"))  # Driver (1 = Yes, 0 = No)