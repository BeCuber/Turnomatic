from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMenu, QAction, QLineEdit, \
    QSizePolicy
from PyQt5.QtCore import Qt, QDate
from PyQt5 import uic
from datetime import date

from src.data.db_connector import DatabaseConnector
from src.logic.availability_manager import AvailabilityManager
from src.logic.room_assignment_manager import RoomManager
from src.utils.path_helper import get_resource_path


class RoomsCardWidget(QWidget):
    def __init__(self, parent, day: date, theme: str, db:DatabaseConnector, rooms_map: dict):
        super().__init__()
        UI_PATH = get_resource_path("src/ui/widgets/rooms_card.ui")
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.day = day
        self.theme = theme
        self.db = db
        self.room_manager = RoomManager(db)
        self.am = AvailabilityManager(db)
        self.rooms_map = rooms_map

        # resource paths
        icon_add_room_path = get_resource_path("assets/images/add_room.ico")
        icon_add_bed_path = get_resource_path("assets/images/add_bed.ico")
        self.icon_menu_path = get_resource_path("assets/images/menu.ico")
        if self.theme == "light":
            icon_arrow_down_path = get_resource_path("assets/images/double_arrow_down.ico")
            icon_bed_path = get_resource_path("assets/images/bed.ico")
        else:
            icon_arrow_down_path = get_resource_path("assets/images/double_arrow_down_dark.ico")
            icon_bed_path = get_resource_path("assets/images/bed_dark.ico")

        # Fixed buttons
        self.btn_add_room = self.findChild(QPushButton, "btnAddRoom")
        self.btn_add_room.setIcon(QIcon(icon_add_room_path))
        self.btn_add_room.clicked.connect(self.on_add_room_clicked)

        # Dynamic buttons
        self.add_bed_buttons = []
        self.menu_buttons = []
        self.init_room_name()
        self.init_add_bed_btns(icon_add_bed_path)
        self.init_menu_btns(self.icon_menu_path)

        #labels
        self.display_no_room_title(icon_arrow_down_path)

        # containers
        self.vBoxWithoutRoomList = self.findChild(QVBoxLayout, "vBoxWithoutRoomList")

        # day title
        self.display_header_room_card(icon_bed_path)

        self.load_volunteers_without_room()

    # ==== Header Section - containerTitleCard, containerCurrentOccupied - =====

    def display_header_room_card(self, path):
        """"""
        self._set_day_title()
        self._display_count_beds(path)


    def _set_day_title(self):
        DAYS_ES = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        title = self.findChild(QLabel, "labelTitleCard")

        day_name_en = self.day.strftime('%A')  # Ej: 'Monday'
        day_name_es = DAYS_ES[day_name_en]
        title.setText(f"{day_name_es} {self.day.strftime('%d/%m')}")
        self._apply_today_style()

    def _apply_today_style(self):
        if date.today() == self.day:
            title = self.findChild(QLabel, "labelTitleCard")
            if self.theme == "light":
                title.setStyleSheet("background-color:#90EE90")
            else:
                title.setStyleSheet("background-color:#4CB093")


    def _display_count_beds(self, path):
        """"""
        self.room_icon = self.findChild(QLabel, "labelRoomIcon")
        bed_icon = QPixmap(path)
        self.room_icon.setPixmap(bed_icon.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        label_occupied = self.findChild(QLabel, "labelCurrentOccupiedRooms")
        self._get_current_occupied(label_occupied)

    def _get_current_occupied(self, label:QLabel):
        """"""
        text = f"{self._get_count_occupied_rooms()}/{self._get_total_rooms()}"
        label.setText(text)

    def _get_total_rooms(self):
        """"""
        return "10"

    def _get_count_occupied_rooms(self):
        """"""
        return "5"



    # ==== ScrollArea Rooms Section =====
    def init_room_name(self):
        """"""
        for i in range (1, 11):
            label = self.findChild(QLineEdit, f"labelRoomName{i}")
            if label:
                room_id = i
                if room_id in self.rooms_map:
                    name, capacity = self.rooms_map[room_id]
                    label.setText(name)
                    label.setProperty("roomLabel", True)
                    label.setReadOnly(True)
                    label.room_id = room_id

                    label.mouseDoubleClickEvent = lambda e, l=label: self.enable_edit(l)
                    label.editingFinished.connect(lambda l=label: self.finish_edit(l))
                else:
                    label.setText("N/D")
            else:
                print(f"Error: labelRoomName{i} no se ha encontrado en UI")


    def init_add_bed_btns(self, path):
        """"""
        for i in range (1, 11):
            btn = self.findChild(QPushButton, f"btnAddBed{i}")
            if btn:
                btn.setIcon(QIcon(path))
                btn.setProperty("menu", True)

                btn.clicked.connect(lambda _, r=i: self.add_bed(r))

                self.add_bed_buttons.append(btn)
            else:
                print(f"Error: btnAddBed{i} no se ha encontrado en UI")


    def init_menu_btns(self, path):
        """"""
        for i in range (1, 11):
            btn = self.findChild(QPushButton, f"btnMenu{i}")
            if btn:
                btn.setIcon(QIcon(path))
                btn.setProperty("menu", True)
                btn.clicked.connect(lambda _, n=i: self.on_menu_clicked(n))
                self.menu_buttons.append(btn)
            else:
                print(f"Error: btnAddBed{i} no se ha encontrado en UI")


    def on_add_room_clicked(self):
        print("Add room clicked")


    def add_bed(self, room):
        print(f"Add bed clicked on room {room}")


    def on_menu_clicked(self, volunteer):
        print(f"Menu clicked on {volunteer}")


    def change_room_name(self, id_room: int, new_name: str):
        """"""
        self.parent.update_room_name(id_room, new_name)
        print("Nombre cambiado!")

    def enable_edit(self, lineedit: QLineEdit):
        lineedit.setReadOnly(False)
        lineedit.setFocus()

    def finish_edit(self, lineedit: QLineEdit):
        lineedit.setReadOnly(True)
        new_name = lineedit.text()
        id_room = lineedit.room_id
        self.change_room_name(id_room, new_name)

    # ==== ScrollArea No Room -and title no room- Section =====
    def display_no_room_title(self, path):
        """"""
        self.title_no_room = self.findChild(QLabel, "labelTitleNoRoom")
        self.title_no_room.setTextFormat(Qt.RichText) # habilita html en qlabel

        html = f'<img src="{path}" width="16" height="16"> ' \
           f'<span style="padding: 0 6px;">Sin asignar</span>' \
           f'<img src="{path}" width="16" height="16">'

        self.title_no_room.setText(html)


    def load_volunteers_without_room(self):
        """"""
        volunteers = self.room_manager.get_volunteers_without_room(self.day)

        # Limpiar vBoxWithoutRoomList
        while self.vBoxWithoutRoomList.count():
            child = self.vBoxWithoutRoomList.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        FIXED_ROW_HEIGHT = 30
        for id_availability, id_volunteer, name in volunteers:
            # --- 1. Crear un QWidget contenedor para cada fila ---
            row_container_widget = QWidget()
            # Establecer la política de tamaño y la altura mínima/fija
            row_container_widget.setSizePolicy(
                QSizePolicy.Preferred,  # Horizontal: prefiere su tamaño, puede expandirse si hay espacio
                QSizePolicy.Fixed  # Vertical: ¡Altura fija! No se estirará
            )
            row_container_widget.setMinimumHeight(FIXED_ROW_HEIGHT)
            row_container_widget.setMaximumHeight(FIXED_ROW_HEIGHT)  # Para asegurar que no exceda

            # --- 2. Crear el layout horizontal dentro de este contenedor ---
            h_layout = QHBoxLayout(row_container_widget)  # Asigna el h_layout al row_container_widget
            h_layout.setContentsMargins(0, 0, 0, 0)  # Elimina márgenes extra si no los necesitas
            h_layout.setSpacing(5)  # Espaciado entre elementos

            label = QLabel(name)
            label.setObjectName(f"labelVol_{id_volunteer}")
            label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            btn = QPushButton()
            btn.setMaximumSize(12, 12)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setIconSize(btn.maximumSize())
            btn.setObjectName(f"btnVolMenu_{id_volunteer}")
            btn.setProperty("menu", True)
            btn.setIcon(QIcon(self.icon_menu_path))

            # Crear menú contextual para el botón
            menu = QMenu(btn)
            action_assign = QAction("Asignar habitación", btn)
            action_delete = QAction("Eliminar disponibilidad", btn)

            # Asociar funciones a las acciones
            action_assign.triggered.connect(lambda _, a=id_availability: self.assign_room(a))
            action_delete.triggered.connect(lambda _, v=id_volunteer, a=id_availability: self.unconfirm_availability(v, a))

            menu.addAction(action_assign)
            menu.addAction(action_delete)
            btn.setMenu(menu)

            # Añadir widgets al layout
            h_layout.addWidget(label)
            h_layout.addWidget(btn)

            # self.vBoxWithoutRoomList.addLayout(h_layout)
            self.vBoxWithoutRoomList.addWidget(row_container_widget)
            self.vBoxWithoutRoomList.addStretch(0)


    def assign_room(self, id_availability: int):
        print(f"Asignar habitación a disponibilidad {id_availability}")


    def unconfirm_availability(self, id_volunteer: int, id_availability: int):
        """"""
        self.am.switch_confirmed(id_availability)
        self.am.merge_periods(id_volunteer, 0, id_availability)
        self.parent.display_room_cards()
        print(f"Desconfirmar disponibilidad {id_availability}")



if __name__ == "__main__":

    pass