# from itertools import count

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QTableWidget, QPushButton, QDialog, QMessageBox, QCalendarWidget, QSizePolicy, \
    QLabel
from PyQt5 import uic

from src.logic.bed_manager import BedManager
from src.ui.widgets.calendar import CalendarManager
from src.ui.widgets.combo_boxes import ComboBoxManager
from src.ui.widgets.rooms_card import RoomsCardWidget
from src.ui.widgets.table_widgets import TableWidgetManager
from src.ui.widgets.text_edit import TextEditManager
from src.ui.widgets.radio_buttons import RadioButtonsManager
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.dialog_manager import DialogManager
from src.logic.availability_manager import AvailabilityManager
from src.utils.path_helper import get_resource_path

class RoomsPage(QWidget):
    def __init__(self, parent, db:DatabaseConnector):
        super().__init__()

        UI_PATH = get_resource_path("src/ui/pages/rooms_page.ui")
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.db = db
        # self.vm = VolunteerManager(db)
        # self.am = AvailabilityManager(db)
        # self.bm = BedManager(db)

        # Define widgets
        rooms_container = self.findChild(QWidget, "widgetCard")
        self.rooms_layout = rooms_container.layout()


        room_card = RoomsCardWidget(self)
        self.rooms_layout.addWidget(room_card)


