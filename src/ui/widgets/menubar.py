from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QAction

from src.ui.pages.calendar_page import CalendarPage
from src.ui.pages.rooms_page import RoomsPage
from src.ui.pages.volunteer_page import VolunteerPage


class MenuBarManager(QObject):
    # action_triggered = pyqtSignal(str)
    
    def __init__(self, main_window: QMainWindow, stacked_widget, calendar_page: CalendarPage, volunteer_page: VolunteerPage, rooms_page: RoomsPage):
    # def __init__(self, main_window: QMainWindow):
        """Initializes the menu bar manager"""
        super().__init__(main_window)
        self.main_window = main_window
        self.stacked_widget = stacked_widget
        self.calendar_page = calendar_page
        self.volunteer_page = volunteer_page
        self.rooms_page = rooms_page
        self.setup_menu_actions()

    def setup_menu_actions(self):
        """Configures the menu actions."""
        self.menu_calendar = self.main_window.findChild(QAction, "actionCalendario")
        self.menu_calendar.triggered.connect(self.show_calendar)
        # self.menu_calendar.triggered.connect(lambda: self._emit_action_signal("calendar"))

        self.menu_volunteers = self.main_window.findChild(QAction, "actionLista_voluntarios")
        self.menu_volunteers.triggered.connect(self.show_volunteer_list)
        # self.menu_volunteers.triggered.connect(lambda: self._emit_action_signal("volunteer_list"))

        self.menu_rooms = self.main_window.findChild(QAction, "actionCamas")
        self.menu_rooms.triggered.connect(self.show_rooms)
        # self.menu_rooms.triggered.connect(lambda: self._emit_action_signal("rooms"))



        self.light_theme = self.main_window.findChild(QAction, "actionClaro")
        self.light_theme.triggered.connect(lambda: self.main_window.set_theme("light"))
        self.dark_theme = self.main_window.findChild(QAction, "actionOscuro")
        self.dark_theme.triggered.connect(lambda: self.main_window.set_theme("dark"))

        def _emit_action_signal(self, action_name: str) -> None:
            """
            Emits a signal with the name of the triggered menu action.

            Args:
                action_name (str): The identifier of the triggered action.
            """
            self.action_triggered.emit(action_name)

    def show_calendar(self):
        """Cambia a la página del calendario."""
        self.calendar_page.refresh()
        self.calendar_page.display_volunteer_lists()
        self.stacked_widget.setCurrentIndex(0)

    def show_volunteer_list(self):
        """Cambia a la página de lista de voluntarios."""
        self.volunteer_page.display_volunteer_data()
        self.stacked_widget.setCurrentIndex(1)

    def show_rooms(self):
        """"""
        self.rooms_page.refresh()
        self.stacked_widget.setCurrentIndex(2)