from PyQt5.QtWidgets import QMainWindow, QAction


class MenuBarManager():
    
    def __init__(self, main_window: QMainWindow, stacked_widget):
        """Inicializa el gestor del menú de la ventana principal."""
        self.main_window = main_window
        self.stacked_widget = stacked_widget
        self.setup_menu_actions()

    def setup_menu_actions(self):
        """Configura las acciones del menú."""
        self.menu_calendar = self.main_window.findChild(QAction, "actionCalendario")
        self.menu_calendar.triggered.connect(self.show_calendar)

        self.menu_volunteers = self.main_window.findChild(QAction, "actionLista_voluntarios")
        self.menu_volunteers.triggered.connect(self.show_volunteer_list)

    def show_calendar(self):
        """Cambia a la página del calendario."""
        self.stacked_widget.setCurrentIndex(0)

    def show_volunteer_list(self):
        """Cambia a la página de lista de voluntarios."""
        self.stacked_widget.setCurrentIndex(1)