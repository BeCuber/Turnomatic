from PyQt5.QtWidgets import QWidget, QCalendarWidget, QTableWidget, QPushButton
from PyQt5 import uic
import os
from datetime import datetime, timedelta
#from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.table_widgets import TableWidgetManager
from src.logic.availability_manager import AvailabilityManager
from src.data.db_connector import DatabaseConnector

class CalendarPage(QWidget):
    def __init__(self, parent, db):
        super().__init__()
        self.am = AvailabilityManager(db)

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
        
        self.btn_add = self.findChild(QPushButton, "btnAddConfirmed")
        self.btn_substract = self.findChild(QPushButton, "btnSubstractConfirmed")
        

        #Initialize
        self.table_manager = TableWidgetManager(self, self.db)

        self.table_manager.define_available_volunteer_list(self.confirmed_volunteer_table)
        self.table_manager.define_available_volunteer_list(self.not_confirmed_volunteer_table)

        # Default view and update in day change
        self.calendar.selectionChanged.connect(lambda: self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table, 1))
        self.calendar.selectionChanged.connect(lambda: self.table_manager.update_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table, 0))
        
        # self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table, 1)
        # self.table_manager.update_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table, 0)
        self.display_volunteer_lists()

        # nito: dia calendar, id_volunteer
        #id_volunteer = self.get_selected_volunteer_id()

        self.btn_add.clicked.connect(lambda: self.change_confirmed(self.not_confirmed_volunteer_table))
        self.btn_substract.clicked.connect(lambda: self.change_confirmed(self.confirmed_volunteer_table))


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

        # If selected_date is one day only, just update 'confirmed' field
        if date_init == date_end:
            self.am.switch_confirmed(id_availability)
        
        # If selected_date is the first day in the register
        elif selected_date == date_init:
            self.am.update_availability(id_availability, id_volunteer, (date_init + timedelta(days=1)).isoformat(), date_end.isoformat(), comments, confirmed)
            self.am.create_availability(id_volunteer, selected_date.isoformat(), selected_date.isoformat(), comments, not confirmed)

        # If selected_date is the last day in the register
        elif selected_date == date_end:
            self.am.update_availability(id_availability, id_volunteer, date_init.isoformat(), (date_end - timedelta(days=1)).isoformat(), comments, confirmed)
            self.am.create_availability(id_volunteer, selected_date.isoformat(), selected_date.isoformat(), comments, not confirmed)
        
        # If selected day is in the middle of a register: divide on three parts
        else:
            self.am.update_availability(id_availability, id_volunteer, date_init.isoformat(), (selected_date - timedelta(days=1)).isoformat(), comments, confirmed)
            self.am.create_availability(id_volunteer, selected_date.isoformat(), selected_date.isoformat(), comments, not confirmed)
            self.am.create_availability(id_volunteer, (selected_date + timedelta(days=1)).isoformat(), date_end.isoformat(), comments, confirmed)

        # Fusionar períodos adyacentes si procede
        #self.merge_periods(id_volunteer)

        # Update QTableWidgets
        self.table_manager.update_confirmed_volunteer_list(self.calendar, self.confirmed_volunteer_table, 1)
        self.table_manager.update_confirmed_volunteer_list(self.calendar, self.not_confirmed_volunteer_table, 0)

    
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
    
    # TODO No te cargues esto aún:
    # def merge_periods(self, id_volunteer, confirmed):
    #     """"""
    #     periods = self.am.get_confirmed_availability_by_id_volunteer(id_volunteer, confirmed)
    #     if not periods or len(periods) < 2:
    #         return  # Nothing to merge
    #
    #     print(periods)
    #
    #     # Estructura: [(id_availability, date_init, date_end, comments), ...]
    #     merged_periods = []
    #     ids_to_delete = []
    #
    #     current_period = periods[0]
    #     current_id_availability = current_period[0]
    #     current_start = datetime.strptime(periods[0][1], "%Y-%m-%d").date() # date_init of first register
    #     current_end = datetime.strptime(periods[0][2], "%Y-%m-%d").date() # date_end of first register
    #     current_comment = periods[3]
    #
    #     for next_period in periods[1:]: # [1:] slice list
    #
    #         next_id_availability = next_period[0]
    #         next_start = datetime.strptime(next_period[1], "%Y-%m-%d").date()
    #         next_end = datetime.strptime(next_period[2], "%Y-%m-%d").date()
    #         next_comment = next_period[3]
    #
    #         # Are they contiguous?
    #         if next_start <= current_end + timedelta(days=1):
    #             current_end = max(current_end, next_end)
    #             if next_comment and next_comment != current_comment:
    #                 current_comment += f" | {next_comment}"
    #
    #             merged_periods.append((current_start, current_end, current_comment))
    #             ids_to_delete.append(current_id_availability, next_id_availability)
    #
    #         else:
    #             print("No son adyacentes")





# from bash: $ python -m src.ui.pages.calendar_page (-m points "src" a module)
if __name__ == "__main__":
    db = DatabaseConnector()
    am = AvailabilityManager(db)
    #cp = CalendarPage(QMainWindow, db)

    periods = am.get_confirmed_availability_by_id_volunteer(1, 1)
    if not periods or len(periods) < 2:
        print("nothing to merge")  # Nada que fusionar
        
    print(periods)
        

    am.db.close_connection()
