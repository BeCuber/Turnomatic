from PyQt5.QtWidgets import QMainWindow, QAction

from src.ui.pages.calendar_page import CalendarPage
from src.ui.pages.rooms_page import RoomsPage
from src.ui.pages.volunteer_page import VolunteerPage


class MenuBarManager():
    
    def __init__(self, main_window: QMainWindow, stacked_widget, calendar_page: CalendarPage, volunteer_page: VolunteerPage, meals_and_beds_page: RoomsPage):
        """Inicializa el gestor del menú de la ventana principal."""
        self.main_window = main_window
        self.stacked_widget = stacked_widget
        self.calendar_page = calendar_page
        self.volunteer_page = volunteer_page
        self.meals_and_beds_page = meals_and_beds_page
        self.setup_menu_actions()

    def setup_menu_actions(self):
        """Configura las acciones del menú."""
        self.menu_calendar = self.main_window.findChild(QAction, "actionCalendario")
        self.menu_calendar.triggered.connect(self.show_calendar)

        self.menu_volunteers = self.main_window.findChild(QAction, "actionLista_voluntarios")
        self.menu_volunteers.triggered.connect(self.show_volunteer_list)

        self.menu_meal_bed = self.main_window.findChild(QAction, "actionComidas_y_camas")
        self.menu_meal_bed.triggered.connect(self.show_meal_bed)

        self.light_theme = self.main_window.findChild(QAction, "actionClaro")
        self.light_theme.triggered.connect(lambda: self.main_window.apply_stylesheet("light"))
        self.dark_theme = self.main_window.findChild(QAction, "actionOscuro")
        self.dark_theme.triggered.connect(lambda: self.main_window.apply_stylesheet("dark"))

    def show_calendar(self):
        """Cambia a la página del calendario."""
        self.calendar_page.refresh()
        self.calendar_page.display_volunteer_lists()
        self.stacked_widget.setCurrentIndex(0)

    def show_volunteer_list(self):
        """Cambia a la página de lista de voluntarios."""
        self.volunteer_page.display_volunteer_data()
        self.stacked_widget.setCurrentIndex(1)

    def show_meal_bed(self):
        # self.menu_meal_bed
        self.stacked_widget.setCurrentIndex(2)