from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PyQt5.QtGui import QIcon, QGuiApplication
from PyQt5 import uic

from src.logic.availability_manager import AvailabilityManager
from src.logic.volunteer_manager import VolunteerManager
from src.ui.pages.rooms_page import RoomsPage
from src.utils.path_helper import get_resource_path
from src.ui.widgets.menubar import MenuBarManager
from src.data.db_connector import DatabaseConnector
from src.ui.pages.calendar_page import CalendarPage
from src.ui.pages.volunteer_page import VolunteerPage


class MainWindow(QMainWindow):
    theme_changed = pyqtSignal(str)  # signal on value for update theme

    def __init__(self, db_connector: DatabaseConnector, availability_manager: AvailabilityManager, volunteer_manager: VolunteerManager):
        super().__init__()

        QApplication.setOrganizationName("Ordesa")
        QApplication.setApplicationName("Turnomatic")

        self.settings = QSettings()

        self.current_theme = self.settings.value("theme/current", "light")

        # Load the ui file - dinamic route
        UI_PATH = get_resource_path("src/ui/main_window.ui")
        uic.loadUi(UI_PATH, self)

        # Set icon and title window
        self.setWindowTitle("Turnomatic")
        ICON_PATH = get_resource_path("assets/images/300_trans.ico")
        self.setWindowIcon(QIcon(ICON_PATH))

        # Connect to database
        # self.db = DatabaseConnector()
        self.db = db_connector
        self._availability_manager = availability_manager
        self._volunteer_manager = volunteer_manager

        # Define widgets
        self.stacked_widget = self.findChild(QStackedWidget, "stackedWidget")

        # Initialize pages
        self.calendar_page = CalendarPage(self, self.db, self._availability_manager, self._volunteer_manager)
        self.volunteer_page = VolunteerPage(self, self.db, self._availability_manager, self._volunteer_manager)
        self.rooms_page = RoomsPage(self, self.db, self._availability_manager, self._volunteer_manager)

        # Add pages to stack
        self.stacked_widget.addWidget(self.calendar_page)
        self.stacked_widget.addWidget(self.volunteer_page)
        self.stacked_widget.addWidget(self.rooms_page)

        # Set initial style theme

        self._apply_full_theme(self.current_theme)
        self.set_initial_window_size_and_position()

        # Config menu manager
        self.menu_manager = MenuBarManager(self, self.stacked_widget, self.calendar_page, self.volunteer_page, self.rooms_page)
        # self.menu_manager.action_triggered.connect(self._handle_menu_action)

        # Show the app
        self.show()

    # def _handle_menu_action(self, action_name: str) -> None:
    #     """
    #     Handles the menu action triggered by MenuBarManager and changes the stacked widget page.
    #
    #     Args:
    #         action_name (str): The identifier of the triggered action.
    #     """
    #     if action_name == "calendar":
    #         self.stacked_widget.setCurrentWidget(self.calendar_page)
    #         self.calendar_page.refresh()
    #         self.calendar_page.display_volunteer_lists()
    #     elif action_name == "volunteer_list":
    #         self.stacked_widget.setCurrentWidget(self.volunteer_page)
    #         self.volunteer_page.display_volunteer_data()
    #     elif action_name == "rooms":
    #         self.stacked_widget.setCurrentWidget(self.rooms_page)
    #         self.rooms_page.refresh()
    #     # elif action_name == "documentation":
    #     #     print("Abrir documentación (a implementar).")  #  otras acciones
    #         # Aquí
    #     else:
    #         print(f"Unhandled menu action: {action_name}")

    def _apply_full_theme(self, theme_name: str):
        """"""
        self._apply_stylesheet_to_app(theme_name)

        self.calendar_page.update_page_theme_styles(theme_name)
        # rooms_page se hará en la siguiente parte, volunteer_page si tiene estilos python
        # self.rooms_page.update_page_theme_styles(theme_name)
        # self.volunteer_page.update_page_theme_styles(theme_name)

    def _apply_stylesheet_to_app(self, theme):
        """"""
        # self.current_theme = theme
        theme_file = f"assets/styles/{theme}.qss"
        QSS_PATH = get_resource_path(theme_file)
        try:
            with open(QSS_PATH, "r", encoding="utf-8") as f:
                stylesheet = f.read()

            QApplication.instance().setStyleSheet(stylesheet)
            self.theme_changed.emit(theme)

        except Exception as e:
            print(f"Error applying stylesheet {QSS_PATH}: {e}")
            return

        # self.calendar_page.refresh()

    def set_theme(self, theme_name: str):
        """
        Change the app's theme and save the preference.
        """
        if self.current_theme != theme_name:  # Solo cambiar si es un tema diferente
            self.current_theme = theme_name
            self._apply_full_theme(theme_name)

            self.settings.setValue("theme/current", theme_name)
        else:
            print(f"El tema ya es '{theme_name}'. No se requiere cambio.")


    def set_initial_window_size_and_position(self, percentage_width=0.8, percentage_height=0.8):
        """
        Calculates the window's initial size and position
        based on a percentage of the screen size (80% default) and centers it.
        """
        screen = QGuiApplication.primaryScreen().geometry()
        # Calcular el tamaño de la ventana
        window_width = int(screen.width() * percentage_width)
        window_height = int(screen.height() * percentage_height)

        # Calcular la posición para centrar la ventana
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2

        # Establecer la geometría de la ventana
        self.setGeometry(x, y, window_width, window_height)


    def closeEvent(self, event):
        """Se ejecuta cuando se cierra la ventana"""
        print("Cerrando conexión con la base de datos...")
        self.db.close_connection()  # Close the connection
        event.accept()  # Let close the window
