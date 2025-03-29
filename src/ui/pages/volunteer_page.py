from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
import os
from src.ui.widgets.combo_boxes import ComboBoxManager
from src.ui.widgets.table_widgets import TableWidgetManager
from src.ui.widgets.text_edit import TextEditManager
from src.ui.widgets.radio_buttons import RadioButtonsManager

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

        # Inicializar 
        self.volunteer_table = TableWidgetManager(self, self.db)
        self.volunteer_table.define_all_volunteers_table()

        self.combobox_manager = ComboBoxManager(self, self.db)
        self.combobox_manager.define_form_combobox()

        self.text_edit_manager = TextEditManager(self, self.db)
        self.text_edit_manager.define_volunteer_form_text_fields()

        self.radio_btn_manager = RadioButtonsManager(self, self.db)
        self.radio_btn_manager.define_form_radio_buttons()