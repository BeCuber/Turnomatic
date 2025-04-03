from PyQt5.QtWidgets import QWidget, QCalendarWidget, QTableWidget, QAbstractItemView
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

        # Define widgets
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")

        self.confirmed_volunteer_table = self.findChild(QTableWidget, "volunteerTableWidget")
        self.not_confirmed_volunteer_table = self.findChild(QTableWidget, "notConfirmedVolunteerTable")
        
        #Initialize
        self.table_manager = TableWidgetManager(self, self.db)

        self.table_manager.define_available_volunteer_list(self.confirmed_volunteer_table)
        self.table_manager.define_available_volunteer_list(self.not_confirmed_volunteer_table)

        # Default view and update in day change
        self.calendar.selectionChanged.connect(lambda: self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table, 1))
        self.calendar.selectionChanged.connect(lambda: self.table_manager.update_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table, 0))
        
        self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table, 1)
        self.table_manager.update_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table, 0)

        # nito: dia calendar, id_volunteer
        id_volunteer = self.get_selected_volunteer_id()

        
    
    def get_selected_volunteer_id(self):
        """Returns the id_volunteer of the selected row in either table, or None if no row is selected."""

        selected_table = None
        if self.confirmed_volunteer_table.selectedIndexes():
            selected_table = self.confirmed_volunteer_table
        elif self.not_confirmed_volunteer_table.selectedIndexes():
            selected_table = self.not_confirmed_volunteer_table

        if selected_table:
            selected_row = selected_table.selectedIndexes()[0].row()  # Get the selected row
            id_volunteer = selected_table.item(selected_row, 0).text()  # Get ID from column 0
            return int(id_volunteer)  # Convert to integer (if needed)

        return None  # No row selected
