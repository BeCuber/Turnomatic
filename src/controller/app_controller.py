from src.ui.main_window import MainWindow
from src.data.db_connector import DatabaseConnector
from src.logic.availability_manager import AvailabilityManager
from src.logic.volunteer_manager import VolunteerManager

class AppController:
    """
    Manages the overall application flow, initializing core components
    like the database connection, data managers, and the main user interface.
    Acts as the central coordinator for the application's MVC architecture.
    """
    def __init__(self):
        """
        Initializes the AppController and its main components.
        """
        self._db_connector = None
        self._availability_manager = None
        self._volunteer_manager = None
        self._main_window = None

        self._initialize_core_components()
        self._initialize_ui()

    def _initialize_core_components(self) -> None:
        """
        Initializes the database connector and data managers.
        """
        # Initialize Database Connector (only once)
        self._db_connector = DatabaseConnector()
        print("Database connection initialized.")

        # Initialize Managers, passing the single DB connector instance
        self._availability_manager = AvailabilityManager(self._db_connector)
        self._volunteer_manager = VolunteerManager(self._db_connector)
        print("Availability and Volunteer managers initialized.")

    def _initialize_ui(self) -> None:
        """
        Initializes the main user interface, passing necessary components.
        """
        # Pass the controller itself or specific managers to MainWindow if needed
        # For now, let's pass the database connector and potentially the managers
        self._main_window = MainWindow(
            db_connector=self._db_connector,
            availability_manager=self._availability_manager, # Pasar managers
            volunteer_manager=self._volunteer_manager # Pasar managers
        )
        print("Main Window initialized.")

    def get_main_window(self) -> MainWindow:
        """
        Returns the initialized main application window.

        Returns:
            MainWindow: The main application window instance.
        """
        return self._main_window