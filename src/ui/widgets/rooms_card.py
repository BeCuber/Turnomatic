from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QDate
from PyQt5 import uic

from src.utils.path_helper import get_resource_path


# from rooms_card_ui import Ui_Form

class RoomsCardWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        UI_PATH = get_resource_path("src/ui/widgets/rooms_card.ui")
        uic.loadUi(UI_PATH, self)
