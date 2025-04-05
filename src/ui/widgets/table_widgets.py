from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QCalendarWidget, QWidget, QAbstractItemView
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager
from src.logic.availability_manager import AvailabilityManager


class TableWidgetManager():

    def __init__(self, parent: QWidget, db: DatabaseConnector):
        """Initialize tables manager."""
        self.parent = parent
        self.vm = VolunteerManager(db)
        self.am = AvailabilityManager(db)

    def add_empty_row(self, table:QTableWidget):
        """Add an empty row to create new registers"""
        row_idx = table.rowCount()
        table.insertRow(row_idx)
        

    # TABLES FOR volunteer_page #

    def define_all_volunteers_table(self, volunteer_table: QTableWidget):

        self.volunteer_table = volunteer_table

        # Add a hidden column at beginning for ID
        volunteer_table.insertColumn(0)
        volunteer_table.setColumnHidden(0, True)

        # Load volunteer list
        volunteer_table.blockSignals(True) # Avoid errors by triggering cellChanged
        self.load_all_volunteers(volunteer_table)
        volunteer_table.blockSignals(False) # Let edit the table

        volunteer_table.cellChanged.connect(self.update_volunteer_in_db)

        # self.add_empty_row(self.volunteer_table)


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

        volunteer_table = self.volunteer_table # Saved on define_all_volunteers_table()
        
        # Get ID volunteer selected
        id_volunteer = volunteer_table.item(row, 0).text()
        
        new_value = volunteer_table.item(row, col).text()

        # Map columns with database names
        column_mapping = {
            1: "name",
            2: "lastname_1",
            3: "lastname_2"
        }

        if col in column_mapping:
            field_name = column_mapping[col]

            query = f"UPDATE volunteer SET {field_name} = ? WHERE id_volunteer = ?"
            self.vm.db.execute_query(query, (new_value, id_volunteer))


    def define_availability_table(self, availability_table: QTableWidget):
        """Configure availability table for edit and connect signals."""
        self.availability_table = availability_table  # ⬅️ Guardamos la tabla como atributo

        # Asegúrate de que la primera columna (ID) está oculta
        availability_table.setColumnHidden(0, True)

        # Conectar para guardar cambios en la base de datos
        availability_table.cellChanged.connect(self.update_availability_in_db)


    def display_individual_availability_data_table(self, id_volunteer, availability_table: QTableWidget):
        """Show availability data for a given volunteer on table."""

        # Hide column at beginning for ID
        #availability_table.setColumnHidden(0, True)
        availability_table.blockSignals(True) # Avoid errors by triggering cellChanged
        availability_table.clearContents()
        availability_table.setRowCount(0) # reset number of rows

        availability = self.am.get_availability_by_id_volunteer(id_volunteer)

        for row_idx, v in enumerate(availability):
            availability_table.insertRow(row_idx)
            availability_table.setItem(row_idx, 0, QTableWidgetItem(str(v["id_availability"])))
            availability_table.setItem(row_idx, 1, QTableWidgetItem(v["date_init"]))
            availability_table.setItem(row_idx, 2, QTableWidgetItem(v["date_end"]))
            availability_table.setItem(row_idx, 3, QTableWidgetItem(v["comments"]))

        availability_table.blockSignals(False) # Let edit the table


    def update_availability_in_db(self, row: int, col: int):
        """Update availability in database when cell is edited."""

        availability_table = self.availability_table

        id_availability = availability_table.item(row, 0).text()
        new_value = availability_table.item(row, col).text()

        column_mapping = {
            1: "date_init",
            2: "date_end",
            3: "comments"
        }

        if col in column_mapping:
            field_name = column_mapping[col]

            query = f"UPDATE availability SET {field_name} = ? WHERE id_availability = ?"
            self.am.db.execute_query(query, (new_value, id_availability))


    # TABLES FOR calendar_page #

    def define_available_volunteer_list(self, volunteer_table: QTableWidget):
        
        # Add a hidden column at beginning for ID
        volunteer_table.insertColumn(0)
        volunteer_table.setColumnHidden(0, True)
        # Avoid editing on list
        volunteer_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        # Select entire row
        volunteer_table.setSelectionBehavior(QAbstractItemView.SelectRows)


    def update_confirmed_volunteer_list(self, calendar:QCalendarWidget, volunteer_table: QTableWidget, confirmed):
        """Get selected date and update the volunteer list."""
        date_selected = calendar.selectedDate().toString("yyyy-MM-dd") 
        volunteers = self.vm.check_volunteers_in_date(date_selected, confirmed)

        # Clean table before update
        volunteer_table.setRowCount(0)

        # Load data on table
        for row_idx, v in enumerate(volunteers):
            volunteer_table.insertRow(row_idx)
            volunteer_table.setItem(row_idx, 0, QTableWidgetItem(str(v["id_volunteer"])))
            volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["name"]))  
            volunteer_table.setItem(row_idx, 2, QTableWidgetItem(v["lastname_1"]))  
            volunteer_table.setItem(row_idx, 3, QTableWidgetItem("🚑" if v["driver"] else ""))
    
