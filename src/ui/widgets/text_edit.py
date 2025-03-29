from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPlainTextEdit, QTableWidget
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager
from src.ui.widgets.table_widgets import TableWidgetManager


class TextEditManager():
    def __init__(self, parent: QWidget, db: DatabaseConnector):
        """Initialize text fields manager."""
        self.parent = parent
        self.vm = VolunteerManager(db)
        self.twm = TableWidgetManager(self.parent, self.vm.db)

    
    def define_volunteer_form_text_fields(self):

        self.label_volunteer = self.parent.findChild(QLabel, "labelNameVolunteer")
        self.input_dni = self.parent.findChild(QLineEdit, "lineEditDNI")
        self.input_email = self.parent.findChild(QLineEdit, "lineEditEmail")
        self.input_phone = self.parent.findChild(QLineEdit, "lineEditPhone")
        self.input_medication = self.parent.findChild(QPlainTextEdit, "plainTextEditMedication")
        self.input_allergies = self.parent.findChild(QPlainTextEdit, "plainTextEditAllergies")
        self.input_contact_person = self.parent.findChild(QPlainTextEdit, "plainTextEditContactPerson")

        volunteer_table = self.parent.findChild(QTableWidget, "allVolunteerTableWidget")
        volunteer_table.itemSelectionChanged.connect(self.display_selected_volunteer_text_data)
        

    def display_selected_volunteer_text_data(self):
        """Show data from selected volunteer on table."""
        volunteer_table = self.parent.findChild(QTableWidget, "allVolunteerTableWidget")
        selected_items = volunteer_table.selectedItems()

        if not selected_items:
            return  # No hay selección, salir

        row = selected_items[0].row()  # Obtener la fila seleccionada
        volunteer_id = volunteer_table.item(row, 0).text()  # ID está oculto en la columna 0

        # Obtener los datos del voluntario desde la base de datos
        volunteer_data = self.vm.get_volunteer_by_id(volunteer_id)

        if volunteer_data:
            self.label_volunteer.setText(f"{volunteer_data['name']} {volunteer_data['lastname_1']}")
            self.input_dni.setText(volunteer_data['id_card'] or '')
            self.input_email.setText(volunteer_data['email'] or '')
            self.input_phone.setText(volunteer_data['phone'] or '')
            self.input_medication.setPlainText(volunteer_data['medication_description'] or '')
            self.input_allergies.setPlainText(volunteer_data['allergy_description'] or '')
            self.input_contact_person.setPlainText(volunteer_data['contact_person'] or '')





