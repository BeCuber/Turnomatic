from PyQt5.QtWidgets import QWidget,QTableWidget, QPushButton, QDialog, QMessageBox
from PyQt5 import uic
import os
from src.ui.widgets.combo_boxes import ComboBoxManager
from src.ui.widgets.table_widgets import TableWidgetManager
from src.ui.widgets.text_edit import TextEditManager
from src.ui.widgets.radio_buttons import RadioButtonsManager
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.dialog_manager import DialogManager

class VolunteerPage(QWidget):
    def __init__(self, parent, db:DatabaseConnector):
        super().__init__()

        # Load UI
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        UI_PATH = os.path.join(BASE_DIR, "./volunteer_page.ui")  # specific UI for this page
        uic.loadUi(UI_PATH, self)

        self.parent = parent
        self.db = db
        self.vm = VolunteerManager(db)

        # Define widgets
        self.volunteer_table = self.findChild(QTableWidget, "allVolunteerTableWidget")
        self.availability_table = self.findChild(QTableWidget, "tableWidgetIndividualAvailability")
        self.btn_add_volunteer = self.findChild(QPushButton, "btnAddVolunteer")
        self.btn_delete_volunteer = self.findChild(QPushButton, "btnDeleteVolunteer")
        self.btn_add_availability = self.findChild(QPushButton, "btnAddAvailability")
        self.btn_delete_availability = self.findChild(QPushButton, "btnDeleteAvailability")


        # Inicialize
        self.table_manager = TableWidgetManager(self, self.db)
        self.table_manager.define_all_volunteers_table(self.volunteer_table)
        self.table_manager.define_availability_table(self.availability_table)

        self.combobox_manager = ComboBoxManager(self, self.db)
        self.combobox_manager.define_form_combobox()

        self.text_edit_manager = TextEditManager(self, self.db)
        self.text_edit_manager.define_volunteer_form_text_fields()

        self.radio_btn_manager = RadioButtonsManager(self, self.db)
        self.radio_btn_manager.define_form_radio_buttons()

        # Default view
        self.volunteer_table.selectRow(0)
        self.display_volunteer_data()

        # Select volunteer
        self.volunteer_table.itemSelectionChanged.connect(lambda: self.display_volunteer_data())


        # Buttons
        self.btn_add_volunteer.clicked.connect(self.create_volunteer)
        self.btn_delete_volunteer.clicked.connect(self.delete_volunteer)
        self.btn_add_availability.clicked.connect(self.create_availability)
        self.btn_delete_availability.clicked.connect(self.delete_availability)



    def display_volunteer_data(self):
        """Show data from selected volunteer on table."""
        
        selected_items = self.volunteer_table.selectedItems()

        if not selected_items:
            return  

        row = selected_items[0].row()  
        volunteer_id = self.volunteer_table.item(row, 0).text()  # ID on column 0

        volunteer_data = self.vm.get_volunteer_by_id(volunteer_id)

        # Pass data to managers to update UI
        self.text_edit_manager.display_selected_volunteer_text_data(volunteer_data)
        self.combobox_manager.display_selected_volunteer_combobox_data(volunteer_data)
        self.radio_btn_manager.display_form_radio_button_data(volunteer_data)
        self.table_manager.display_individual_availability_data_table(volunteer_id, self.availability_table)


    def create_volunteer(self):
        dialog = DialogManager(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            data = dialog.get_data()

            if not data["name"] or not data["lastname_1"] or not data["id_card"]:
                QMessageBox.warning(self, "Error", "El nombre, primer apellido y documento identificativo son obligatorios.")
                return

            # Insertar en la base de datos
            new_id = self.vm.create_volunteer(
                name=data["name"],
                lastname_1=data["lastname_1"],
                lastname_2=data["lastname_2"],
                driver=data["driver"],
                id_card=data["id_card"],
                email="",
                phone="",
                birthdate="1900-01-01", 
                position=0,
                exp4x4=0,
                assembly=0,
                medication=0,
                medication_description="",
                allergy=0,
                allergy_description="",
                contact_person=""
            )

            # Actualizar tabla
            self.volunteer_table.blockSignals(True)
            self.table_manager.load_all_volunteers(self.volunteer_table)
            self.volunteer_table.blockSignals(False)

            self.select_volunteer_row_by_id(new_id)

            # Mostrar confirmación
            QMessageBox.information(self, "Éxito", "Voluntario creado correctamente.")


    def delete_volunteer(self):
        selected_items = self.volunteer_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Atención", "Por favor, selecciona un voluntario para eliminar.")
            return

        selected_row = selected_items[0].row()
        id_volunteer = self.volunteer_table.item(selected_row, 0).text()

        # Confirmar con el usuario
        confirm = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este voluntario?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            self.vm.delete_volunteer(id_volunteer)
            QMessageBox.information(self, "Éxito", "Voluntario eliminado correctamente.")
            self.table_manager.load_all_volunteers(self.volunteer_table)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

        


    def create_availability(self):
        pass


    def delete_availability(self):
        pass


    def get_selected_volunteer_table_id(self):
        """Returns the id_* of the selected row in either table, or None if no row is selected."""

        selected_table = self.volunteer_table

        if selected_table:
            selected_row = selected_table.selectedIndexes()[0].row()  # Get the selected row
            id_volunteer = selected_table.item(selected_row, 0).text()  # Get ID from column 0
            return int(id_volunteer) 

        return None


    def select_volunteer_row_by_id(self, id_volunteer: int):
        """Select the row corresponding to the given volunteer ID."""
        for row in range(self.volunteer_table.rowCount()):
            item = self.volunteer_table.item(row, 0)  # ID is in hidden column 0
            if item and int(item.text()) == id_volunteer:
                self.volunteer_table.selectRow(row)
                break
