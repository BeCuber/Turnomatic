from PyQt5.QtWidgets import QWidget,QTableWidget
from PyQt5 import uic
import os
from src.ui.widgets.combo_boxes import ComboBoxManager
from src.ui.widgets.table_widgets import TableWidgetManager
from src.ui.widgets.text_edit import TextEditManager
from src.ui.widgets.radio_buttons import RadioButtonsManager
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager

class VolunteerPage(QWidget):
    def __init__(self, parent, db:DatabaseConnector):
        super().__init__()

        # Load UI
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        UI_PATH = os.path.join(BASE_DIR, "./volunteer_page.ui")  # specific UI for this page
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.db = db
        self.vm = VolunteerManager(db)

        # Define widgets
        volunteer_table = self.findChild(QTableWidget, "allVolunteerTableWidget")


        # Inicializar 
        self.table_manager = TableWidgetManager(self, self.db)
        self.table_manager.define_all_volunteers_table()

        self.combobox_manager = ComboBoxManager(self, self.db)
        self.combobox_manager.define_form_combobox()

        self.text_edit_manager = TextEditManager(self, self.db)
        self.text_edit_manager.define_volunteer_form_text_fields()

        self.radio_btn_manager = RadioButtonsManager(self, self.db)
        self.radio_btn_manager.define_form_radio_buttons()

        # Select volunteer
        volunteer_table.itemSelectionChanged.connect(lambda: self.display_volunteer_data())



    def display_volunteer_data(self):
        """Show data from selected volunteer on table."""
        
        volunteer_table = self.findChild(QTableWidget, "allVolunteerTableWidget")
        selected_items = volunteer_table.selectedItems()

        if not selected_items:
            return  # No hay selección, salir

        row = selected_items[0].row()  
        volunteer_id = volunteer_table.item(row, 0).text()  # ID está en la columna 0

        # Obtener datos del voluntario solo una vez
        volunteer_data = self.vm.get_volunteer_by_id(volunteer_id)

        # Pasar los datos a los managers para que actualicen la UI
        self.text_edit_manager.display_selected_volunteer_text_data(volunteer_data)
        self.combobox_manager.display_selected_volunteer_combobox_data(volunteer_data)
        self.radio_btn_manager.display_form_radio_button_data(volunteer_data)