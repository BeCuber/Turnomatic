from PyQt5.QtGui import QIcon
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

        self.theme = "light"

        # resource paths
        icon_add_room_path = get_resource_path("assets/images/add_room.ico")
        icon_add_bed_path = get_resource_path("assets/images/add_bed.ico")
        icon_menu_path = get_resource_path("assets/images/menu.ico")

        # Fixed buttons
        self.btn_add_room = self.findChild(QPushButton, "btnAddRoom")
        self.btn_menu_no_room = self.findChild(QPushButton, "btnMenuVolNoRoom")
        self.btn_menu_no_room.setStyleSheet("border:none")
        self.btn_add_room.setIcon(QIcon(icon_add_room_path))
        self.btn_menu_no_room.setIcon(QIcon(icon_menu_path))
        self.btn_add_room.clicked.connect(self.on_add_room_clicked)
        self.btn_menu_no_room.clicked.connect(self.on_menunoroom_clicked)

        # Dynamic buttons
        self.add_bed_buttons = []
        self.menu_buttons = []
        self.init_add_bed_btns(icon_add_bed_path)
        self.init_menu_btns(icon_menu_path)









    def init_add_bed_btns(self, path):
        """"""
        for i in range (1, 11):
            btn = self.findChild(QPushButton, f"btnAddBed{i}")
            if btn:
                btn.setIcon(QIcon(path))
                btn.setStyleSheet("border:none")
                btn.clicked.connect(lambda _, n=i: self.on_add_bed_clicked(n))
                self.add_bed_buttons.append(btn)
            else:
                print(f"Error: btnAddBed{i} no se ha encontrado en UI")


    def init_menu_btns(self, path):
        """"""
        for i in range (1, 11):
            btn = self.findChild(QPushButton, f"btnMenu{i}")
            if btn:
                btn.setIcon(QIcon(path))
                btn.setStyleSheet("border:none")
                btn.clicked.connect(lambda _, n=i: self.on_menu_clicked(n))
                self.menu_buttons.append(btn)
            else:
                print(f"Error: btnAddBed{i} no se ha encontrado en UI")


    def on_add_room_clicked(self):
        print("Add room clicked")


    def on_add_bed_clicked(self, room):
        print(f"Add bed clicked on room {room}")


    def on_menu_clicked(self, volunteer):
        print(f"Menu clicked on {volunteer}")


    def on_menunoroom_clicked(self):
        print("Menu no-room clicked")





if __name__ == "__main__":

    pass