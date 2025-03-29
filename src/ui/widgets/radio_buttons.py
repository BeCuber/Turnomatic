from PyQt5.QtWidgets import QWidget, QButtonGroup, QTableWidget
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager


class RadioButtonsManager():

    def __init__(self, parent: QWidget, db: DatabaseConnector):
        """Initialize tables manager."""
        self.parent = parent
        self.vm = VolunteerManager(db)

    def define_form_radio_buttons(self):
        """Define radio buttons and group them"""
        
        self.driver_group = self.parent.findChild(QButtonGroup, "driver_group")
        self.exp4x4_group = self.parent.findChild(QButtonGroup, "exp4x4_group")
        self.medication_group = self.parent.findChild(QButtonGroup, "medication_group")
        self.allergy_group = self.parent.findChild(QButtonGroup, "allergy_group")
        
        volunteer_table = self.parent.findChild(QTableWidget, "allVolunteerTableWidget")
        volunteer_table.itemSelectionChanged.connect(self.display_form_radio_button)
        

    def display_form_radio_button(self):
        """Set radio buttons based on the volunteer's data"""

        volunteer_table = self.parent.findChild(QTableWidget, "allVolunteerTableWidget")
        selected_items = volunteer_table.selectedItems()

        if not selected_items:
            return  # No hay selección, salir

        row = selected_items[0].row()  # Obtener la fila seleccionada
        volunteer_id = volunteer_table.item(row, 0).text()  # ID está oculto en la columna 0

        # Obtener los datos del voluntario desde la base de datos
        volunteer_data = self.vm.get_volunteer_by_id(volunteer_id)

        if volunteer_data:
            # Asignar los valores a los radio buttons
            self.set_radio_button(self.driver_group, volunteer_data["driver"])
            self.set_radio_button(self.exp4x4_group, volunteer_data["exp4x4"])
            self.set_radio_button(self.medication_group, volunteer_data["medication"])
            self.set_radio_button(self.allergy_group, volunteer_data["allergy"])


    def set_radio_button(self, group, value):
        """Selecciona el radio button correcto en un grupo según el valor de la BD."""
        buttons = group.buttons()  # Obtiene la lista de botones en el grupo

        # El primer botón se asume que es "Sí" y el segundo "No"
        button_yes = buttons[0]
        button_no = buttons[1]

        if value:  # Si el valor es True o 1, seleccionamos "Sí"
            button_yes.setChecked(True)
        else:  # Si es False o 0, seleccionamos "No"
            button_no.setChecked(True)