from PyQt5.QtWidgets import QMainWindow, QCalendarWidget, QTableWidget, QTableWidgetItem, QStackedWidget, QAction
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import os
from src.logic.volunteer_manager import VolunteerManager

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Load the ui file - dinamic route
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        UI_PATH = os.path.join(BASE_DIR, "main_window.ui")
        uic.loadUi(UI_PATH, self)

        # Set icon and title window
        self.setWindowTitle("Turnomatic")
        ICON_PATH = os.path.join(BASE_DIR, "../../assets", "images", "narval.ico")
        self.setWindowIcon(QIcon(ICON_PATH))

        # Define widgets
        self.stacked_widget = self.findChild(QStackedWidget, "stackedWidget")
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.volunteer_table = self.findChild(QTableWidget, "volunteerTableWidget")

        # Set calendar page as default
        self.show_calendar()

        # Define menubar options -->

        # --> Calendar
        self.menu_calendar = self.findChild(QAction, "actionCalendario")
        self.menu_calendar.triggered.connect(self.show_calendar)

        # --> Menu volunteers
        self.menu_volunteers = self.findChild(QAction, "actionLista_voluntarios")
        self.menu_volunteers.triggered.connect(self.show_volunteer_list)
        
        
        # Default view on volunteer_table
        self.check_day()

        # Click day
        self.calendar.selectionChanged.connect(self.check_day)

        



        # Show the app
        self.show()



    def check_day(self):
        """Get selected date and update the volunteer list"""
        date_selected = self.calendar.selectedDate().toString("yyyy-MM-dd") # Formate compatible con SQLite
        vm = VolunteerManager()
        volunteers = vm.check_volunteers_in_date(date_selected)
        vm.db.close_connection()  

        # Limpiar la tabla antes de actualizar
        self.volunteer_table.setRowCount(0)

        # Llenar la tabla con los datos obtenidos
        for row_idx, v in enumerate(volunteers):
            self.volunteer_table.insertRow(row_idx)
            self.volunteer_table.setItem(row_idx, 0, QTableWidgetItem(v[0]))  # Name
            self.volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v[1]))  # Lastname_1
            self.volunteer_table.setItem(row_idx, 2, QTableWidgetItem("🚑" if v[3] else "")) # Driver

    
    def show_calendar(self):
        """Change to calendar page"""
        self.stacked_widget.setCurrentIndex(0) 

    
    def show_volunteer_list(self):
        """Change to volunteer list page"""
        self.stacked_widget.setCurrentIndex(1) # Change to page_2