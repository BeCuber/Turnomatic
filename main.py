from PyQt5.QtWidgets import QApplication
import sys
from src.ui.main_window import MainWindow
from src.data.db_connector import DatabaseConnector


#db = DatabaseManager()
#db.insert_sample_data()
#db.close_connection()
#print("Sample data inserted!")

# Initialize the App
app = QApplication(sys.argv)
UIWindow = MainWindow()
app.exec_()