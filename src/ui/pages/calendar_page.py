from PyQt5.QtWidgets import QWidget, QCalendarWidget, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import os
from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.table_widgets import TableWidgetManager

class CalendarPage(QWidget):
    def __init__(self, parent, db):
        super().__init__()

        # Load UI
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        UI_PATH = os.path.join(BASE_DIR, "./calendar_page.ui")  # specific UI for this page
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.db = db
        #self.vm = VolunteerManager(self.db)

        # Define widgets
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.confirmed_volunteer_table = self.findChild(QTableWidget, "volunteerTableWidget")
        self.not_confirmed_volunteer_table = self.findChild(QTableWidget, "notConfirmedVolunteerTable")

        #Initialize
        self.table_manager = TableWidgetManager(self, self.db)

        # Default view
        self.calendar.selectionChanged.connect(lambda: self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table))
        self.calendar.selectionChanged.connect(lambda: self.table_manager.update_not_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table))
        self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table)
        self.table_manager.update_not_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table)
    '''
    def update_confirmed_volunteer_list(self):
        """Get selected date and update the volunteer list."""
        date_selected = self.calendar.selectedDate().toString("yyyy-MM-dd") 
        #vm = VolunteerManager(self.db)
        volunteers = self.vm.check_confirmed_volunteers_in_date(date_selected)

        # Clean table before update
        self.confirmed_volunteer_table.setRowCount(0)

        # Load data on table
        for row_idx, v in enumerate(volunteers):
            self.confirmed_volunteer_table.insertRow(row_idx)
            self.confirmed_volunteer_table.setItem(row_idx, 0, QTableWidgetItem(v["name"]))  
            self.confirmed_volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["lastname_1"]))  
            self.confirmed_volunteer_table.setItem(row_idx, 2, QTableWidgetItem("🚑" if v["driver"] else ""))
    
    
    def update_not_confirmed_volunteer_list(self):
        """Get selected date and update the volunteer list."""
        date_selected = self.calendar.selectedDate().toString("yyyy-MM-dd") 
        #vm = VolunteerManager(self.db)
        volunteers = self.vm.check_not_confirmed_volunteers_in_date(date_selected)

        # Clean table before update
        self.not_confirmed_volunteer_table.setRowCount(0)

        # Load data on table
        for row_idx, v in enumerate(volunteers):
            self.not_confirmed_volunteer_table.insertRow(row_idx)
            self.not_confirmed_volunteer_table.setItem(row_idx, 0, QTableWidgetItem(v["name"]))  
            self.not_confirmed_volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["lastname_1"]))  
            self.not_confirmed_volunteer_table.setItem(row_idx, 2, QTableWidgetItem("🚑" if v["driver"] else ""))
    '''