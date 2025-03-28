from PyQt5.QtWidgets import QWidget, QCalendarWidget, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import os
from src.logic.volunteer_manager import VolunteerManager

class CalendarPage(QWidget):
    def __init__(self, parent, db):
        super().__init__()

        # Load UI
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        UI_PATH = os.path.join(BASE_DIR, "./calendar_page.ui")  # specific UI for this page
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.db = db

        # Define widgets
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.volunteer_table = self.findChild(QTableWidget, "volunteerTableWidget")

        # Default view
        self.calendar.selectionChanged.connect(self.update_volunteer_list)
        self.update_volunteer_list()

    def update_volunteer_list(self):
        """Get selected date and update the volunteer list."""
        date_selected = self.calendar.selectedDate().toString("yyyy-MM-dd") 
        vm = VolunteerManager(self.db)
        volunteers = vm.check_volunteers_in_date(date_selected)

        # Clean table before update
        self.volunteer_table.setRowCount(0)

        # Load data on table
        for row_idx, v in enumerate(volunteers):
            self.volunteer_table.insertRow(row_idx)
            self.volunteer_table.setItem(row_idx, 0, QTableWidgetItem(v["name"]))  
            self.volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["lastname_1"]))  
            self.volunteer_table.setItem(row_idx, 2, QTableWidgetItem("🚑" if v["driver"] else ""))
