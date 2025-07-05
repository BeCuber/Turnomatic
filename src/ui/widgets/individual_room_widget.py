from datetime import date

from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QMenu, QAction, QFrame

from src.logic.room_manager import RoomManager
from src.utils.path_helper import get_resource_path


class IndividualRoomWidget(QWidget):
    room_name_updated = pyqtSignal(int, str)  # id_room, new_name para el cambio de nombre de hab
    assignment_created_in_room = pyqtSignal(int, dict)


    # def __init__(self, parent: QWidget, id_room: int, room_name: str, capacity: int, day: date, theme: str, room_manager: RoomManager, availability_manager: AvailabilityManager):
    def __init__(self, parent: QWidget, id_room: int, room_dict: dict, no_room_list: list, day: date, theme: str, room_manager: RoomManager):
        super().__init__(parent)

        UI_PATH = get_resource_path("src/ui/widgets/individual_room_widget.ui")
        uic.loadUi(UI_PATH, self)

        self.id_room = id_room
        self.room_dict = room_dict
        self.day = day
        self.theme = theme
        self.room_manager = room_manager
        self.room_name = self.room_dict["room_name"]
        self.no_room_list = no_room_list # <-- [(id_availability, id_volunteer, name), (id_availability, id_volunteer, name)]
        # print(no_room_list)
        self.capacity = self.room_dict["capacity"]
        self.volunteers = self.room_dict["volunteers"] # <-- (id_volunteer, name, id_assignment, id_availability)
        if self.volunteers and isinstance(self.volunteers[0], tuple):
            self.volunteers = [
                {
                    "id_volunteer": vol[0],
                    "name": vol[1],
                    "id_assignment": vol[2],
                    "id_availability": vol[3]
                }
                for vol in self.volunteers
            ]
        self.count_volunteers = 0

        # PICK WIDGETS FROM UI;
            # main container
        self.frame_room = self.findChild(QFrame, "frameRoom")

            # CONFIG Add btn
        self.btn_add_volunteer = self.findChild(QPushButton, "btnAddVolunteer")
        icon_add_vol_path = get_resource_path("assets/images/add_volunteer.ico")
        self.btn_add_volunteer.setIcon(QIcon(icon_add_vol_path))
        self.btn_add_volunteer.setProperty("menu", True)
        self.setup_menu_on_add_vol_btn(self.btn_add_volunteer, self.no_room_list)

            #CONFIG label name
        self.label_room_name = self.findChild(QLineEdit, "labelRoomName")
        self.label_room_name.setText(self.room_name)
        self.label_room_name.setProperty("roomLabel", True)
        self.label_room_name.setReadOnly(True)

        self.label_room_name.mouseDoubleClickEvent = lambda e: self._enable_edit_room_name(e)
        self.label_room_name.returnPressed.connect(self._finish_edit_room_name)

            # Container for placeholders
        self.vbox_vol_same_room = self.findChild(QVBoxLayout, "vBoxVolSameRoom")

        # while self.vbox_vol_same_room.count():
        #     child = self.vbox_vol_same_room.takeAt(0)
        #     if child.widget():
        #         child.widget().deleteLater()
        #

        # print(self.room_dict) # {'room_name': '10', 'capacity': 1, 'volunteers': []}
        # print(self.volunteers) # []
        # if len(self.volunteers) != 0:
        if self.volunteers:
            # self.ids_volunteers = self.volunteers["id_volunteer"]
            for volunteer in self.volunteers:
                self.insert_placeholder_for_bed(volunteer)
        else:
            self.insert_placeholder_for_bed()



    def _enable_edit_room_name(self, event):
        # Es bueno pasar el evento si redefines el mouseDoubleClickEvent
        self.label_room_name.setReadOnly(False)
        self.label_room_name.setFocus()
        event.accept()

    def _finish_edit_room_name(self):
        """"""
        self.label_room_name.setReadOnly(True)
        new_name = self.label_room_name.text()

        if new_name != self.room_name:  # Solo actualiza si ha cambiado
            self.room_name = new_name
            self.room_manager.update_room_name(self.id_room, new_name)
            self.room_name_updated.emit(self.id_room, new_name)

        self.label_room_name.clearFocus()


    def setup_menu_on_add_vol_btn(self, btn: QPushButton, no_room_vol: list):
        """"""
        menu = QMenu(btn)
        # [(id_availability, id_volunteer, name), (id_availability, id_volunteer, name)]
        for vol in no_room_vol:
            id_availability, id_volunteer, volunteer_name = vol
            date_init, date_end = self.room_manager.get_dates_from_availability(id_availability)
            # print(dates) # ('2025-06-06', '2025-08-31')
            vol_data_for_assignment = {
                'id_availability': id_availability,
                'id_volunteer': id_volunteer,
                'name': volunteer_name,
                'date_init': date_init,
                'date_end': date_end
            }

            action = QAction(f"{volunteer_name}", btn)
            action.triggered.connect(lambda _, v=vol_data_for_assignment: self.add_volunteer_to_this_room(v))

            menu.addAction(action)
        btn.setMenu(menu)

        # self.room_content_changed.emit()  # Para que RoomsCardWidget sepa que algo ha cambiado
    def add_volunteer_to_this_room(self, volunteer_data: dict):
        """"""
        # 1 Crear un id_assignment

        try:
            id_assignment = self.room_manager.create_room_assignment(
                id_room=self.id_room,
                id_availability=volunteer_data["id_availability"],
                check_in=volunteer_data["date_init"],
                check_out=volunteer_data["date_end"]
            )
        except Exception as e:
            print(f"Error al crear la asignación: {e}")
            return

        # 2 Insertarlo en la ui propia?
        btn_menu_first_vol = self.findChild(QPushButton, "btnMenu1")
        if self.count_volunteers==1 and not btn_menu_first_vol.isEnabled(): # Si el primer voluntario tiene el btn deshabilitado:
            label_vol_name = self.findChild(QLabel, "labelNameVol1")
            label_vol_name.setText(volunteer_data["name"])
            label_vol_name.setProperty("is_empty", "True")
            # label_vol_name.style().unpolish(label_vol_name)
            # label_vol_name.style().polish(label_vol_name)
            btn_menu_first_vol.setDisabled(False)
        else:
            self.insert_placeholder_for_bed(volunteer_data)

        # 3 Avisar a los padres para que recarguen el ui

        new_assignment_details = {
            "id_volunteer": volunteer_data["id_volunteer"],
            "name": volunteer_data["name"],
            "id_assignment": id_assignment,
            "id_availability": volunteer_data["id_availability"],
            "check_in": volunteer_data["date_init"],
            "check_out": volunteer_data["date_end"]  # TODO cambiar cuando sea != de date_init/end
        }
        self.assignment_created_in_room.emit(self.id_room, new_assignment_details)

    def unassign_volunteer(self, vol_id: int, room_assignment_id: int):
        print(f"Desasignar voluntario {vol_id} de asignación {room_assignment_id}")
        # self.room_manager.unassign_volunteer_from_room(room_assignment_id)  # Nueva función en RoomManager
        # self._load_assigned_volunteers()  # Refrescar solo esta habitación
        # self.room_content_changed.emit()  # Notificar a RoomsCardWidget que se ha cambiado el contenido

    def edit_assignment(self, vol_id: int, room_assignment_id: int):
        print(f"Editar asignación {room_assignment_id} del voluntario {vol_id}")
        # Aquí irá la lógica para abrir un diálogo de edición de asignación



    def insert_placeholder_for_bed(self, volunteer_data: dict = None):
        self.count_volunteers += 1
        h_box_bed_container = QtWidgets.QHBoxLayout()
        h_box_bed_container.setContentsMargins(0, 0, 0, 0)
        h_box_bed_container.setObjectName(f"hBoxNameVolBtnMenu{str(self.count_volunteers)}")

        label_vol_name = QtWidgets.QLabel(self.frame_room)
        label_vol_name.setObjectName(f"labelNameVol{str(self.count_volunteers)}")

        h_box_bed_container.addWidget(label_vol_name)

        btn_menu_vol = QtWidgets.QPushButton(self.frame_room)
        btn_menu_vol.setMaximumSize(QtCore.QSize(12, 12))
        btn_menu_vol.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_menu_vol.setText("")
        btn_menu_vol.setIconSize(QtCore.QSize(12, 12))
        btn_menu_vol.setObjectName(f"btnMenu{str(self.count_volunteers)}")
        icon_menu_path = get_resource_path("assets/images/menu.ico")
        btn_menu_vol.setIcon(QIcon(icon_menu_path))
        btn_menu_vol.setProperty("menu", True)
        self.setup_menu_on_volunteer_btn(btn_menu_vol)

        h_box_bed_container.addWidget(btn_menu_vol)

        h_box_bed_container.setStretch(0, 1)

        if volunteer_data:
            label_vol_name.setText(volunteer_data["name"])
            label_vol_name.setProperty("is_empty", "False")
            # label_vol_name.style().unpolish(label_vol_name)
            # label_vol_name.style().polish(label_vol_name)
            # volunteer_name = volunteer_data.get("name")
            # label_vol_name.setText(volunteer_name)
            # update room_assignment
        else:
            label_vol_name.setText("- Vacía -")
            label_vol_name.setProperty("is_empty", "True")
            # label_vol_name.style().unpolish(label_vol_name)
            # label_vol_name.style().polish(label_vol_name)
            btn_menu_vol.setDisabled(True)

        self.vbox_vol_same_room.addLayout(h_box_bed_container)



    def setup_menu_on_volunteer_btn(self, btn: QPushButton):
        """"""

        menu = QMenu(btn)
        # action_delete = QAction("Quitar cama", btn)
        # h_box_layout = btn.layout()
        # action_delete.triggered.connect(lambda: self.delete_bed(h_box_layout))
        #
        # menu.addAction(action_delete)

        action_change = QAction("Modificar asignación", btn)
        action_remove = QAction("Quitar asignación", btn)
        h_box_layout = btn.layout()
        action_change.triggered.connect(self.change_volunteer)
        action_remove.triggered.connect(self.remove_volunteer)

        menu.addAction(action_change)
        menu.addAction(action_remove)

        btn.setMenu(menu)

    # def delete_bed(self, layout):
    #     """"""
    #     # i = 0
    #     #
    #     # # TODO esta limpieza no estoy segura de dónde iria
    #     #
    #     # while self.vbox_vol_same_room.count():
    #     #     child = self.vbox_vol_same_room.takeAt(0)
    #     #     if child.widget():
    #     #         child.widget().deleteLater()
    #     #
    #     # while i < self.capacity:
    #     #     self.insert_placeholder_for_bed()
    #     #     i += 1
    #     if layout.objectName() != "hBoxNameVolBtnMenu0":
    #         layout.deleteLater()


    def change_volunteer(self):
        pass

    def remove_volunteer(self):
        pass