from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMenu, QAction, QLineEdit, \
    QSizePolicy
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5 import uic, QtWidgets, QtCore
from datetime import date

from src.logic.availability_manager import AvailabilityManager
from src.logic.room_manager import RoomManager
from src.ui.widgets.individual_room_widget import IndividualRoomWidget
from src.utils.path_helper import get_resource_path


class RoomsCardWidget(QWidget):
    room_name_updated_in_card = pyqtSignal(int, str)

    def __init__(self, parent, day: date, theme: str, am: AvailabilityManager, rm: RoomManager, room_dict: dict):
        super().__init__()
        UI_PATH = get_resource_path("src/ui/widgets/rooms_card.ui")
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.day = day
        self.theme = theme
        self.room_manager = rm
        self.am = am
        self.rooms_dict_for_day = room_dict

        self.no_room_volunteers = self.room_manager.get_volunteers_without_room(self.day)
        # ^-> [(id_availability, id_volunteer, name), (id_availability, id_volunteer, name)]

        # resource paths
        self.icon_add_room_path = get_resource_path("assets/images/add_room.ico")
        # icon_add_bed_path = get_resource_path("assets/images/add_volunteer.ico")
        self.icon_menu_path = get_resource_path("assets/images/menu.ico")
        if self.theme == "light":
            self.icon_arrow_down_path = get_resource_path("assets/images/double_arrow_down.ico")
            self.icon_bed_path = get_resource_path("assets/images/bed.ico")
            self.icon_person_path = get_resource_path("assets/images/person.ico")
        else:
            self.icon_arrow_down_path = get_resource_path("assets/images/double_arrow_down_dark.ico")
            self.icon_bed_path = get_resource_path("assets/images/bed_dark.ico")
            self.icon_person_path = get_resource_path("assets/images/person_dark.ico")

        # Fixed buttons
        self.btn_add_room = self.findChild(QPushButton, "btnAddRoom")
        if self.btn_add_room:
            self.btn_add_room.setIcon(QIcon(self.icon_add_room_path))
            self.btn_add_room.clicked.connect(self.on_add_room_clicked)
        else:
            print("Error: btnAddRoom no encontrado en rooms_card.ui")


        #labels
        self.display_no_room_title(self.icon_arrow_down_path)

        # containers
        self.vbox_container_without_room = self.findChild(QVBoxLayout, "vBoxWithoutRoomList")

        self.rooms_layout = self.findChild(QVBoxLayout, "innerRoomsContainer")

        #
        self.load_volunteers_without_room()
        self.display_header_room_card()
        self._populate_room_widgets()


    # ==== Header Section - containerTitleCard, containerCurrentOccupied - =====

    def display_header_room_card(self):
        """"""
        self._set_day_title()
        self._display_count_volunteers()
        self._display_count_beds()


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


    def _display_count_beds(self):
        """"""
        self.room_icon = self.findChild(QLabel, "labelRoomIcon")
        bed_icon = QPixmap(self.icon_bed_path)
        self.room_icon.setPixmap(bed_icon.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        label_occupied = self.findChild(QLabel, "labelCurrentOccupiedRooms")
        self._get_current_occupied(label_occupied)

    def _get_current_occupied(self, label:QLabel):
        """"""
        total_rooms = len(self.rooms_dict_for_day)
        volunteers_today = sum(len(info["volunteers"]) for info in self.rooms_dict_for_day.values())
        text = f"{volunteers_today}/{total_rooms}"
        label.setText(text)

    def _display_count_volunteers(self):
        """"""
        self.count_vol_icon = self.findChild(QLabel, "labelPersonIcon")
        person_icon = QPixmap(self.icon_person_path)
        self.count_vol_icon.setPixmap(person_icon.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        label_volunteers = self.findChild(QLabel, "labelCurrentVolunteers")
        self._current_count_volunteers_today(label_volunteers)


    def _current_count_volunteers_today(self, label:QLabel):
        """"""
        total_vol_assigned = sum(len(room_data["volunteers"]) for room_data in self.rooms_dict_for_day.values())
        total_vol_unassigned = self.vbox_container_without_room.count()
        total = total_vol_assigned + total_vol_unassigned
        label.setText(str(total))


    # ==== ScrollArea Rooms Section =====

    def _populate_room_widgets(self):
        """
        Limpia el layout de habitaciones y crea/añade IndividualRoomWidget
        para 10 habitaciones de prueba.
        """
        # Asegurarse de que el layout existe
        # if not self.rooms_layout:
        #     print("Error: rooms_layout no inicializado.")
        #     return

        # Limpiar cualquier widget existente en el layout
        while self.rooms_layout.count():
            child = self.rooms_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Crear 10 habitaciones de prueba
        # enabled_rooms_today = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # for i in enabled_rooms_today:  # Los IDs de tus habitaciones fijas

        for id_room in self.rooms_dict_for_day:
            room_widget = IndividualRoomWidget(
                parent=self,
                id_room=id_room,
                room_dict=self.rooms_dict_for_day[id_room],
                no_room_list=self.no_room_volunteers,
                day=self.day,
                theme=self.theme,
                room_manager=self.room_manager
            )

            room_widget.setFixedHeight(58)
            room_widget.room_name_updated.connect(self._handle_room_name_update)
            # Añade el widget al layout de la RoomsCardWidget
            self.rooms_layout.addWidget(room_widget)

        # Muy importante: añade un 'stretch' al final para que las habitaciones se apilen arriba
        # self.findChild(QWidget, "scrollAreaRoomsContents").layout().addStretch(1)
        self.rooms_layout.addStretch(1)

        print("10 IndividualRoomWidgets de prueba cargados.")


    def _handle_room_name_update(self, id_room: int, new_name: str):
        """"""
        self.room_name_updated_in_card.emit(id_room, new_name)

    # def _populate_room_widgets(self):
    #     rooms_layout = self.rooms_layout
    #     if not rooms_layout:
    #         print("Error: no se encontró scrollAreaContents.layout()")
    #         return
    #
    #     while rooms_layout.count():
    #         child = rooms_layout.takeAt(0)
    #         if child.widget():
    #             child.widget().deleteLater()
    #
    #     # Ejemplo si rooms_map ya tiene solo las habilitadas:
    #     sorted_room_ids = sorted(self.rooms_map.keys())
    #
    #     for id_room in sorted_room_ids:
    #         room_name, room_capacity = self.rooms_map[id_room]
    #
    #         room_widget = IndividualRoomWidget(
    #             parent=self,
    #             id_room=id_room,
    #             room_name=room_name,
    #             capacity=room_capacity,
    #             day=self.day,
    #             theme=self.theme,
    #             room_manager=self.room_manager,
    #             am=self.am
    #         )
    #
    #         rooms_layout.addWidget(room_widget)
    #
    #     rooms_layout.addStretch(1)
    #     self._get_current_occupied(self.labelCurrentOcupiedRooms) # TODO Debe ser un atributo
    #







    def on_add_room_clicked(self):
        print("Add room clicked")





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
        # Limpiar vBoxWithoutRoomList
        while self.vbox_container_without_room.count():
            child = self.vbox_container_without_room.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for id_availability, id_volunteer, name in self.no_room_volunteers:
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setContentsMargins(0, 0, 0, 0)
            h_layout.setSpacing(3)

            label = QLabel(name)
            label.setObjectName(f"labelVol_{id_volunteer}")
            label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            label.setFixedHeight(30)
            label.setAlignment(Qt.AlignVCenter)

            btn = QPushButton()
            btn.setMaximumSize(12, 12)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setIconSize(btn.maximumSize())
            btn.setObjectName(f"btnVolMenu_{id_volunteer}")
            btn.setProperty("menu", True)
            btn.setIcon(QIcon(self.icon_menu_path))
            btn.setIconSize(QtCore.QSize(12, 12))

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
            h_layout.setStretch(0, 1)

            self.vbox_container_without_room.addLayout(h_layout)

            # self.vbox_container_without_room.setStretch(0, 0) # <-- No hace nada


    def assign_room(self, id_availability: int):
        print(f"Asignar habitación a disponibilidad {id_availability}")


    def unconfirm_availability(self, id_volunteer: int, id_availability: int):
        """"""
        self.am.switch_confirmed(id_availability)
        self.am.merge_periods(id_volunteer, 0, id_availability)
        self.parent.display_room_cards()
        print(f"Desconfirmar disponibilidad {id_availability}")



