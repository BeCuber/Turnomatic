from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QCalendarWidget, QWidget
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager
from src.logic.availability_manager import AvailabilityManager


class TableWidgetManager():

    def __init__(self, parent: QWidget, db: DatabaseConnector):
        """Initialize tables manager."""
        self.parent = parent
        self.vm = VolunteerManager(db)
        self.am = AvailabilityManager(db)
        

    # TABLES FOR volunteer_page #

    def define_all_volunteers_table(self, volunteer_table: QTableWidget):

        # Add a hidden column at beginning for ID
        volunteer_table.insertColumn(0)
        volunteer_table.setColumnHidden(0, True)

        # Load volunteer list
        volunteer_table.blockSignals(True) # Avoid errors by triggering cellChanged
        self.load_all_volunteers(volunteer_table)
        volunteer_table.blockSignals(False) # Let edit the table

        volunteer_table.cellChanged.connect(self.update_volunteer_in_db)


    def load_all_volunteers(self, volunteer_table: QTableWidget):
        
        volunteers = self.vm.read_all_volunteers()

        volunteer_table.setRowCount(0)

        for row_idx, v in enumerate(volunteers):
            volunteer_table.insertRow(row_idx)
            volunteer_table.setItem(row_idx, 0, QTableWidgetItem(str(v["id_volunteer"])))
            volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["name"]))
            volunteer_table.setItem(row_idx, 2, QTableWidgetItem(v["lastname_1"]))  
            volunteer_table.setItem(row_idx, 3, QTableWidgetItem(v["lastname_2"]))
    
    
    def update_volunteer_in_db(self, row, col):
        """Update database when edit a cell."""
        
        # Get ID volunteer selected
        volunteer_id = self.volunteer_table.item(row, 0).text()
        
        new_value = self.volunteer_table.item(row, col).text()

        # Map columns with database names
        column_mapping = {
            1: "name",
            2: "lastname_1",
            3: "lastname_2"
        }

        if col in column_mapping:
            field_name = column_mapping[col]

            query = f"UPDATE volunteer SET {field_name} = ? WHERE id_volunteer = ?"
            self.vm.db.execute_query(query, (new_value, volunteer_id))


    def display_individual_availability_data_table(self, volunteer_id, availability_table: QTableWidget):
        """Show availability data for a given volunteer on table."""

        availability_table.clear()
        availability_table.setRowCount(0) # reset number of rows
        availability = self.am.get_availability_by_id_volunteer(volunteer_id)

        for row_idx, v in enumerate(availability):
            availability_table.insertRow(row_idx)
            availability_table.setItem(row_idx, 0, QTableWidgetItem(v["date_init"]))
            availability_table.setItem(row_idx, 1, QTableWidgetItem(v["date_end"]))
            availability_table.setItem(row_idx, 2, QTableWidgetItem(v["comments"]))


    # TABLES FOR calendar_page #

    def update_confirmed_volunteer_list(self, calendar:QCalendarWidget, confirmed_volunteer_table: QTableWidget):
        """Get selected date and update the volunteer list."""
        date_selected = calendar.selectedDate().toString("yyyy-MM-dd") 
        #vm = VolunteerManager(self.db)
        volunteers = self.vm.check_confirmed_volunteers_in_date(date_selected)

        # Clean table before update
        confirmed_volunteer_table.setRowCount(0)

        # Load data on table
        for row_idx, v in enumerate(volunteers):
            confirmed_volunteer_table.insertRow(row_idx)
            confirmed_volunteer_table.setItem(row_idx, 0, QTableWidgetItem(v["name"]))  
            confirmed_volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["lastname_1"]))  
            confirmed_volunteer_table.setItem(row_idx, 2, QTableWidgetItem("🚑" if v["driver"] else ""))
    
    
    def update_not_confirmed_volunteer_list(self, calendar:QCalendarWidget, not_confirmed_volunteer_table:QTableWidget):
        """Get selected date and update the volunteer list."""
        date_selected = calendar.selectedDate().toString("yyyy-MM-dd") 
        #vm = VolunteerManager(self.db)
        volunteers = self.vm.check_not_confirmed_volunteers_in_date(date_selected)

        # Clean table before update
        not_confirmed_volunteer_table.setRowCount(0)

        # Load data on table
        for row_idx, v in enumerate(volunteers):
            not_confirmed_volunteer_table.insertRow(row_idx)
            not_confirmed_volunteer_table.setItem(row_idx, 0, QTableWidgetItem(v["name"]))  
            not_confirmed_volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["lastname_1"]))  
            not_confirmed_volunteer_table.setItem(row_idx, 2, QTableWidgetItem("🚑" if v["driver"] else ""))
