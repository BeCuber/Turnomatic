from PyQt5.QtWidgets import QWidget, QCalendarWidget, QTableWidget, QPushButton
from PyQt5 import uic
from datetime import datetime, timedelta # para merge

from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.calendar import CalendarManager
from src.ui.widgets.table_widgets import TableWidgetManager
from src.logic.availability_manager import AvailabilityManager
from src.data.db_connector import DatabaseConnector
from src.utils.path_helper import get_resource_path


class CalendarPage(QWidget):
    def __init__(self, parent, db: DatabaseConnector):
        super().__init__()
        self.am = AvailabilityManager(db)

        # Load UI
        UI_PATH = get_resource_path("src/ui/pages/calendar_page.ui")  # specific UI for this page
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.db = db

        # Define widgets
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")

        self.confirmed_volunteer_table = self.findChild(QTableWidget, "volunteerTableWidget")
        self.not_confirmed_volunteer_table = self.findChild(QTableWidget, "notConfirmedVolunteerTable")
        
        self.btn_add = self.findChild(QPushButton, "btnAddConfirmed")
        self.btn_substract = self.findChild(QPushButton, "btnSubstractConfirmed")

        # Connect signal theme_changed from mainwindow
        self.parent.theme_changed.connect(self.on_theme_changed)
        

        #Initialize
        self.calendar_manager = CalendarManager(self, self.db)
        self.table_manager = TableWidgetManager(self, self.db, self.calendar_manager)

        self.table_manager.define_available_volunteer_list(self.confirmed_volunteer_table)
        self.table_manager.define_available_volunteer_list(self.not_confirmed_volunteer_table)

        # Default view and update in day change
        self.calendar.selectionChanged.connect(lambda: self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table, 1))
        self.calendar.selectionChanged.connect(lambda: self.table_manager.update_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table, 0))

        self.display_volunteer_lists()

        self.calendar_manager.set_heatmap(self.calendar)


        self.btn_add.clicked.connect(lambda: self.change_confirmed(self.not_confirmed_volunteer_table))
        self.btn_substract.clicked.connect(lambda: self.change_confirmed(self.confirmed_volunteer_table))


    def on_theme_changed(self, theme: str):
        """"""
        self.calendar_manager.update_heatmap_style(self.calendar, theme)
        # self.display_volunteer_data()


    def display_volunteer_lists(self):
        """"""
        self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table, 1)
        self.table_manager.update_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table, 0)


    def change_confirmed(self, volunteer_table:QTableWidget):
        """Mark selected date as confirmed and update the availability table accordingly."""

        selected_items = volunteer_table.selectedItems()
        if not selected_items:
            return

        id_volunteer = self.get_selected_volunteer_id()

        selected_date_str = self.calendar.selectedDate().toString("yyyy-MM-dd")
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        
        availability_list = self.am.get_availability_by_date(id_volunteer, selected_date_str)
        if not availability_list:
            return

        # Select the availability register where selected_date belongs
        id_availability, date_init_str, date_end_str, comments, confirmed = self.am.get_availability_by_date(id_volunteer, selected_date)[0]
        date_init = datetime.strptime(date_init_str, "%Y-%m-%d").date()
        date_end = datetime.strptime(date_end_str, "%Y-%m-%d").date()

        new_confirmed = not confirmed # switch confirmed value for the new register
        changed_id_availability = None # variable to save the id to use in merge_periods

        # If selected_date is one day only, just update 'confirmed' field
        if date_init == date_end:
            self.am.switch_confirmed(id_availability)
            changed_id_availability = id_availability
        
        # If selected_date is the first day in the register
        elif selected_date == date_init:
            self.am.update_availability(id_availability, id_volunteer, (date_init + timedelta(days=1)).isoformat(), date_end.isoformat(), comments, confirmed)
            self.am.create_availability(id_volunteer, selected_date.isoformat(), selected_date.isoformat(), comments, not confirmed)
            changed_id_availability = self.db.get_last_inserted_id()

        # If selected_date is the last day in the register
        elif selected_date == date_end:
            self.am.update_availability(id_availability, id_volunteer, date_init.isoformat(), (date_end - timedelta(days=1)).isoformat(), comments, confirmed)
            self.am.create_availability(id_volunteer, selected_date.isoformat(), selected_date.isoformat(), comments, not confirmed)
            changed_id_availability = self.db.get_last_inserted_id()
        
        # If selected day is in the middle of a register: divide on three parts
        else:
            self.am.update_availability(id_availability, id_volunteer, date_init.isoformat(), (selected_date - timedelta(days=1)).isoformat(), comments, confirmed)
            self.am.create_availability(id_volunteer, selected_date.isoformat(), selected_date.isoformat(), comments, not confirmed)
            changed_id_availability = self.db.get_last_inserted_id()
            self.am.create_availability(id_volunteer, (selected_date + timedelta(days=1)).isoformat(), date_end.isoformat(), comments, confirmed)

        # Update QTableWidgets
        self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table, 1)
        self.table_manager.update_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table, 0)

        if changed_id_availability:
            self.am.merge_periods(id_volunteer, new_confirmed, changed_id_availability)


        self.calendar_manager.set_heatmap(self.calendar)

    
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
            return int(id_volunteer)  

        return None

    def refresh(self):
        """Updates the heatmap"""
        self.calendar_manager.set_heatmap(self.calendar)



# from bash: $ python -m src.ui.pages.calendar_page (-m points "src" a module)
if __name__ == "__main__":
    db = DatabaseConnector()
    am = AvailabilityManager(db)
    vm = VolunteerManager(db)



    am.db.close_connection()


