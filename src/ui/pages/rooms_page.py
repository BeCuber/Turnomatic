from datetime import date, timedelta
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QCalendarWidget
from PyQt5 import uic

from src.logic.availability_manager import AvailabilityManager
from src.logic.room_manager import RoomManager
from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.rooms_card import RoomsCardWidget
from src.data.db_connector import DatabaseConnector
from src.utils.path_helper import get_resource_path

class RoomsPage(QWidget):
    def __init__(self, parent, db:DatabaseConnector, am: AvailabilityManager, vm: VolunteerManager):
        super().__init__(parent)

        UI_PATH = get_resource_path("src/ui/pages/rooms_page.ui")
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.db = db
        self.am = am
        self.vm = vm
        self.room_manager = RoomManager(db)
        self.theme = "light"
        # self.rooms_map = self.room_manager.get_all_rooms()


        # Connect signal theme_changed from mainwindow
        self.parent.theme_changed.connect(self.on_theme_changed)

        # Define widgets
        self.display_header()

        # Crea el calendario
        self.calendar_popup = QCalendarWidget()
        self.calendar_popup.setWindowFlags(Qt.Popup)
        self.calendar_popup.setGridVisible(True)
        self.calendar_popup.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar_popup.clicked.connect(self.on_calendar_date_selected)

        rooms_container = self.findChild(QWidget, "widgetCards")
        self.rooms_layout = rooms_container.layout()

        self.current_week_start = self.get_start_of_week(date.today()) # dia de referencia

        self.rooms_dict_for_week = self.room_manager.get_all_data_for_week(self.current_week_start)

        self.update_calendar_theme(self.theme)
        self.display_room_cards()


    def display_header(self):
        """"""
        icon_previous_path = get_resource_path("assets/images/previous.ico")
        icon_next_path = get_resource_path("assets/images/next.ico")
        icon_today_path = get_resource_path("assets/images/today.ico")

        self.btn_previous = self.findChild(QPushButton, "btnPrevious")
        self.btn_next = self.findChild(QPushButton, "btnNext")
        self.btn_go_to_date = self.findChild(QPushButton, "btnGoToDate")

        self.btn_previous.setIcon(QIcon(icon_previous_path))
        self.btn_next.setIcon(QIcon(icon_next_path))
        self.btn_go_to_date.setIcon(QIcon(icon_today_path))

        self.btn_previous.clicked.connect(self.on_previous_clicked)
        self.btn_next.clicked.connect(self.on_next_clicked)
        self.btn_go_to_date.clicked.connect(self.show_calendar_popup)


    def on_previous_clicked(self):
        self.current_week_start -= timedelta(days=7)
        self.refresh()


    def on_next_clicked(self):
        self.current_week_start += timedelta(days=7)
        self.refresh()


    def show_calendar_popup(self):
        button_pos = self.btn_go_to_date.mapToGlobal(self.btn_go_to_date.rect().bottomLeft())
        self.calendar_popup.move(button_pos)
        self.calendar_popup.show()


    def on_calendar_date_selected(self, selected_date: QDate):
        py_date = selected_date.toPyDate()  # Convertimos QDate a datetime.date
        self.current_week_start = self.get_start_of_week(py_date)
        self.calendar_popup.hide()
        self.refresh()


    def on_theme_changed(self, new_theme: str):
        """"""
        self.theme = new_theme
        self.update_calendar_theme(new_theme)
        self.display_room_cards()

    def update_calendar_theme(self, theme: str):
        """Carga y aplica el .qss al calendar_popup"""
        self.theme = theme
        qss_path = get_resource_path(f"assets/styles/{theme}.qss")
        try:
            with open(qss_path, "r", encoding="utf-8") as f:
                self.calendar_popup.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error cargando stylesheet del calendario: {e}")


    def get_start_of_week(self, ref_date: date) -> date:
        """"""
        days_since_sunday = (ref_date.weekday() + 1) % 7
        return ref_date - timedelta(days=days_since_sunday)


    def get_week_days(self):
        """Returns a list of 8 days from sunday to next sunday"""
        return [self.current_week_start + timedelta(days=i) for i in range(8)]  # domingo → domingo


    def display_room_cards(self):
        """"""
        # Limpiar el layout
        while self.rooms_layout.count():
            child = self.rooms_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for day in self.get_week_days():
            room_card = RoomsCardWidget(self, day, self.theme, self.am, self.room_manager, self.rooms_dict_for_week[day])
            # room_card.room_name_updated_in_card.connect(self.refresh)
            # room_card.room_data_changed.connect(self.refresh)
            room_card.refresh_required.connect(self.refresh)
            self.rooms_layout.addWidget(room_card)

    def refresh(self):
        self.rooms_dict_for_week = self.room_manager.get_all_data_for_week(self.current_week_start)
        self.display_room_cards()
