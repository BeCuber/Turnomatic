from PyQt5.QtWidgets import QWidget, QComboBox, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import os
from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.combo_boxes import ComboBoxManager  # Importamos ComboBoxManager

class VolunteerPage(QWidget):
    def __init__(self, parent, db):
        super().__init__()

        # Load UI
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        UI_PATH = os.path.join(BASE_DIR, "./volunteer_page.ui")  # specific UI for this page
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.db = db

        # Define widgets
        self.combobox_positions = self.findChild(QComboBox, "comboBoxPosition")
        self.volunteer_table = self.findChild(QTableWidget, "allVolunteerTableWidget")

        # Inicializar ComboBoxManager
        self.combobox_manager = ComboBoxManager(self, self.db)
        #self.combobox_manager.populate_combobox_positions()

        # Load volunteer list
        self.load_volunteers()

    def load_volunteers(self):
        vm = VolunteerManager(self.db)
        volunteers = vm.read_all_volunteers()  

        self.volunteer_table.setRowCount(0)

        for row_idx, v in enumerate(volunteers):
            self.volunteer_table.insertRow(row_idx)
            self.volunteer_table.setItem(row_idx, 0, QTableWidgetItem(v["name"]))  
            self.volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["lastname_1"]))  
            self.volunteer_table.setItem(row_idx, 2, QTableWidgetItem("🚑" if v["driver"] else ""))  
            
