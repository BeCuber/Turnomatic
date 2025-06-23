from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QDateEdit
from src.logic.volunteer_manager import VolunteerManager
from PyQt5.QtCore import QDate



class TextEditManager:
    def __init__(self, parent: QWidget, vm: VolunteerManager):
        """Initialize text fields manager."""
        self.parent = parent
        self.vm = vm

        self.label_volunteer = self.parent.findChild(QLabel, "labelNameVolunteer")
        self.input_dni = self.parent.findChild(QLineEdit, "lineEditDNI")
        self.input_email = self.parent.findChild(QLineEdit, "lineEditEmail")
        self.input_phone = self.parent.findChild(QLineEdit, "lineEditPhone")
        self.input_medication = self.parent.findChild(QLineEdit, "lineEditMedication")
        self.input_medication.setPlaceholderText("Describe la información que se deba tener en cuenta")
        self.input_allergies = self.parent.findChild(QLineEdit, "lineEditAllergies")
        self.input_allergies.setPlaceholderText("Describe la información que se deba tener en cuenta")
        self.input_contact_person = self.parent.findChild(QLineEdit, "lineEditContactPerson")
        self.input_contact_person.setPlaceholderText("Mercedes - Madre - 666 66 66 66")
        self.date_edit_birth = self.parent.findChild(QDateEdit, "dateEditBirth")
        self.date_edit_birth.setCalendarPopup(True)


    def display_selected_volunteer_text_data(self, volunteer_data):
        """Show data from selected volunteer on table."""

        if volunteer_data:
            self.label_volunteer.setText(f"{volunteer_data['name']} {volunteer_data['lastname_1']}")
            self.input_dni.setText(volunteer_data['id_card'] or '')
            self.input_email.setText(volunteer_data['email'] or '')
            self.input_phone.setText(volunteer_data['phone'] or '')
            # self.input_medication.setPlainText(volunteer_data['medication_description'] or '')
            self.input_medication.setText(volunteer_data['medication_description'] or '')
            # self.input_allergies.setPlainText(volunteer_data['allergy_description'] or '')
            self.input_allergies.setText(volunteer_data['allergy_description'] or '')
            # self.input_contact_person.setPlainText(volunteer_data['contact_person'] or '')
            self.input_contact_person.setText(volunteer_data['contact_person'] or '')

            birthdate = QDate.fromString(volunteer_data["birthdate"], "yyyy-MM-dd")
            self.date_edit_birth.setDate(birthdate)

    
    def set_editable(self, editable: bool):
        """"""

        self.input_dni.setReadOnly(not editable)
        self.input_email.setReadOnly(not editable)
        self.input_phone.setReadOnly(not editable)
        self.input_medication.setReadOnly(not editable)
        self.input_allergies.setReadOnly(not editable)
        self.input_contact_person.setReadOnly(not editable)
        self.date_edit_birth.setEnabled(editable) # it doesnt have ReadOnly method


    def update_volunteer_text(self, id_volunteer):
        """"""
        self.vm.update_volunteer_text_data(
            id_volunteer,
            id_card=self.input_dni.text(),
            email=self.input_email.text(),
            phone=self.input_phone.text(),
            birthdate=self.date_edit_birth.date().toString("yyyy-MM-dd"),
            # medication_description=self.input_medication.toPlainText(),
            medication_description=self.input_medication.text(),
            # allergy_description=self.input_allergies.toPlainText(),
            allergy_description=self.input_allergies.text(),
            # contact_person=self.input_contact_person.toPlainText()
            contact_person=self.input_contact_person.text()
        )


