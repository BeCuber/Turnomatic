from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager


class TableWidgetManager():

    def __init__(self, parent: QWidget, db: DatabaseConnector):
        """Initialize tables manager."""
        self.parent = parent
        self.vm = VolunteerManager(db)
        

    def define_all_volunteers_table(self):

        self.volunteer_table = self.parent.findChild(QTableWidget, "allVolunteerTableWidget")
        # Add a hidden column at beginning for ID
        self.volunteer_table.insertColumn(0)
        self.volunteer_table.setColumnHidden(0, True)

        # Load volunteer list
        self.volunteer_table.blockSignals(True)  # 🔴 Avoid errors by triggering cellChanged
        self.load_all_volunteers()
        self.volunteer_table.blockSignals(False)  # 🟢 Let edit the table

        self.volunteer_table.cellChanged.connect(self.update_volunteer_in_db)



    def load_all_volunteers(self):
        
        volunteers = self.vm.read_all_volunteers()  

        self.volunteer_table.setRowCount(0)

        for row_idx, v in enumerate(volunteers):
            self.volunteer_table.insertRow(row_idx)
            self.volunteer_table.setItem(row_idx, 0, QTableWidgetItem(str(v["id_volunteer"])))
            self.volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["name"]))
            self.volunteer_table.setItem(row_idx, 2, QTableWidgetItem(v["lastname_1"]))  
            self.volunteer_table.setItem(row_idx, 3, QTableWidgetItem(v["lastname_2"]))  
              
    
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
