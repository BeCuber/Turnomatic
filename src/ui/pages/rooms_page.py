# from itertools import count
from datetime import date, timedelta
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
        self.theme = "light"
        # Connect signal theme_changed from mainwindow
        self.parent.theme_changed.connect(self.on_theme_changed)

        # Define widgets
        rooms_container = self.findChild(QWidget, "widgetCards")
        self.rooms_layout = rooms_container.layout()

        self.display_room_cards(self.theme)


    def on_theme_changed(self, new_theme: str):
        """"""
        self.theme = new_theme
        self.display_room_cards(new_theme)


    def get_week_days(self):
        """Returns a list of 8 days from sunday to next sunday"""
        today = date.today()
        # Calculate how many days to substract to reach last sunday
        days_since_sunday = (today.weekday() + 1) % 7 # .weekday() devuelve 0 a 6 cada dia de la semana
        start_of_week = today - timedelta(days=days_since_sunday)

        week = []
        for i in range(8):
            week.append(start_of_week + timedelta(days=i))
        return week


    def set_day(self, room_card, day):
        """"""
        DAYS_ES = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        title = room_card.findChild(QLabel, "labelTitleCard")
        # title.setText(day.strftime('%A %d/%m'))

        day_name_en = day.strftime('%A')  # Ej: 'Monday'
        day_name_es = DAYS_ES[day_name_en]
        title.setText(f"{day_name_es} {day.strftime('%d/%m')}")


    def display_room_cards(self, theme:str):
        """"""
        # Limpiar el layout
        while self.rooms_layout.count():
            child = self.rooms_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        week_dates = self.get_week_days()
        for day in week_dates:
            room_card = RoomsCardWidget(self)
            self.set_day(room_card, day)
            if date.today() == day:
                title = room_card.findChild(QLabel, "labelTitleCard")
                if theme == "light":
                    title.setStyleSheet("background-color:#90EE90")
                else:
                    title.setStyleSheet("background-color:#4CB093")
            self.rooms_layout.addWidget(room_card)