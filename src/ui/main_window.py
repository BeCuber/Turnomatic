import os

from PyQt5.QtWidgets import QMainWindow, QCalendarWidget, QTableWidget, QTableWidgetItem, QStackedWidget, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.menubar import MenuBarManager
from src.data.db_connector import DatabaseConnector
from src.ui.widgets.combo_boxes import ComboBoxManager

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

        # Connect to database
        self.db = DatabaseConnector()

        # Define widgets
        self.stacked_widget = self.findChild(QStackedWidget, "stackedWidget")
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.volunteer_table = self.findChild(QTableWidget, "volunteerTableWidget")        
        # Config menu manager
        self.menu_manager = MenuBarManager(self, self.stacked_widget)
        # Set calendar page as default
        self.menu_manager.show_calendar()
        # Initialize combobox manager
        self.combobox_manager = ComboBoxManager(self, self.db)

        
        # Default view on volunteer_table
        self.check_day()


        # Click day
        self.calendar.selectionChanged.connect(self.check_day)

        



        # Show the app
        self.show()

    def closeEvent(self, event):
        """Se ejecuta cuando se cierra la ventana"""
        print("Cerrando conexión con la base de datos...")
        self.db.close_connection()  # Cierra la conexión
        event.accept()  # Permite cerrar la ventana

    def check_day(self):
        """Get selected date and update the volunteer list"""
        date_selected = self.calendar.selectedDate().toString("yyyy-MM-dd") # Formate compatible con SQLite
        vm = VolunteerManager(self.db)
        volunteers = vm.check_volunteers_in_date(date_selected)

        # Limpiar la tabla antes de actualizar
        self.volunteer_table.setRowCount(0)

        # Llenar la tabla con los datos obtenidos
        for row_idx, v in enumerate(volunteers):
            self.volunteer_table.insertRow(row_idx)
            self.volunteer_table.setItem(row_idx, 0, QTableWidgetItem(v[0]))  # Name
            self.volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v[1]))  # Lastname_1
            self.volunteer_table.setItem(row_idx, 2, QTableWidgetItem("🚑" if v[3] else "")) # Driver
