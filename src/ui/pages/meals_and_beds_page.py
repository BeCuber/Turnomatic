from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QTableWidget, QPushButton, QDialog, QMessageBox, QCalendarWidget, QSizePolicy
from PyQt5 import uic

from src.ui.widgets.calendar import CalendarManager
from src.ui.widgets.combo_boxes import ComboBoxManager
from src.ui.widgets.table_widgets import TableWidgetManager
from src.ui.widgets.text_edit import TextEditManager
from src.ui.widgets.radio_buttons import RadioButtonsManager
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.dialog_manager import DialogManager
from src.logic.availability_manager import AvailabilityManager
from src.utils.path_helper import get_resource_path

class MealsBedsPage(QWidget):
    def __init__(self, parent, db:DatabaseConnector):
        super().__init__()

        UI_PATH = get_resource_path("src/ui/pages/meals_and_beds_page.ui")
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.db = db
        self.vm = VolunteerManager(db)
        self.am = AvailabilityManager(db)