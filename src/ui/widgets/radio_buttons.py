from PyQt5.QtWidgets import QWidget, QButtonGroup, QRadioButton,QMessageBox, QPlainTextEdit, QPushButton
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager


class RadioButtonsManager():

    def __init__(self, parent: QWidget, db: DatabaseConnector):
        """Initialize tables manager."""
        self.parent = parent
        self.vm = VolunteerManager(db)

        # ButtonGroups
        self.driver_group = QButtonGroup(parent)
        self.exp4x4_group = QButtonGroup(parent)
        self.medication_group = QButtonGroup(parent)
        self.allergy_group = QButtonGroup(parent)

        self.define_form_radio_buttons()

    def define_form_radio_buttons(self):
        """Define radio buttons and group them"""

        self.driver_group.addButton(self.parent.findChild(QRadioButton, "radioButtonCarnetYes"), 1)
        self.driver_group.addButton(self.parent.findChild(QRadioButton, "radioButtonCarnetNo"), 0)

        self.exp4x4_group.addButton(self.parent.findChild(QRadioButton, "radioButton4x4Yes"), 1)
        self.exp4x4_group.addButton(self.parent.findChild(QRadioButton, "radioButton4x4No"), 0)

        self.medication_group.addButton(self.parent.findChild(QRadioButton, "radioButtonMedicationYes"), 1)
        self.medication_group.addButton(self.parent.findChild(QRadioButton, "radioButtonMedicationNo"), 0)

        self.allergy_group.addButton(self.parent.findChild(QRadioButton, "radioButtonAllergyYes"), 1)
        self.allergy_group.addButton(self.parent.findChild(QRadioButton, "radioButtonAllergyNo"), 0)


    def display_form_radio_button_data(self, volunteer_data):
        """Set radio buttons based on the volunteer's data"""

        if volunteer_data:
            # Asignar los valores a los radio buttons
            self.set_group_checked(self.driver_group, volunteer_data["driver"])
            self.set_group_checked(self.exp4x4_group, volunteer_data["exp4x4"])
            self.set_group_checked(self.medication_group, volunteer_data["medication"])
            self.set_group_checked(self.allergy_group, volunteer_data["allergy"])


    def set_group_checked(self, group: QButtonGroup, value: bool):
        """Marca el botón correspondiente en el grupo"""
        button = group.button(1 if value else 0)
        if button:
            button.setChecked(True)


    def get_current_radio_values(self):
        """"""
        def get_checked_value(group: QButtonGroup):
            return group.checkedId() == 1

        return {
            "driver": get_checked_value(self.driver_group),
            "exp4x4": get_checked_value(self.exp4x4_group),
            "medication": get_checked_value(self.medication_group),
            "allergy": get_checked_value(self.allergy_group)
        }

    def update_volunteer_radiobtn(self, id_volunteer):
        """"""
        radio_values = self.get_current_radio_values()
        self.vm.update_volunteer_radiobtn_data(
            id_volunteer,
            driver=radio_values["driver"],
            exp4x4=radio_values["exp4x4"],
            medication=radio_values["medication"],
            allergy=radio_values["allergy"]
        )


    def set_editable(self, editable: bool):
        """Habilita o deshabilita todos los radio buttons"""
        for group in [self.driver_group, self.exp4x4_group, self.medication_group, self.allergy_group]:
            for btn in group.buttons():
                btn.setEnabled(editable)
                if not editable:
                    btn.setStyleSheet("color: black;")
                else:
                    btn.setStyleSheet("")


    def connect_toggle_with_plaintext(self, group: QButtonGroup, field: QPlainTextEdit):
        """Activa o desactiva el campo según si se selecciona 'No'."""
        no_button = group.button(0)
        yes_button = group.button(1)

        # previous_data = field.toPlainText()

        # no_button.toggled.connect(lambda checked: self.on_radio_changed(checked, yes_button, field, previous_data))
        no_button.toggled.connect(lambda checked: self.on_radio_changed(checked, yes_button, field))



    # def on_radio_changed(self, checked: bool, yes_button: QRadioButton, field: QPlainTextEdit, previous_data):
    def on_radio_changed(self, checked: bool, yes_button: QRadioButton, field: QPlainTextEdit):
        # Revisar: radiobutton.toggled.connect(self.onClicked) TODO

        if checked:  # "No" is selected
            field.clear()
            field.setPlaceholderText("")
            field.setEnabled(False)
        else:
            yes_button.setChecked(True)
            field.setEnabled(True)

            # if not previous_data:
            #     field.setPlaceholderText("Describe la información que se deba tener en cuenta")
            # else:
            #     field.setPlainText(previous_data)


            # text_content = field.toPlainText().strip()
            # if text_content:
            #     msg = QMessageBox(self.parent)
            #     msg.setWindowTitle("Confirmar acción")
            #     msg.setText("Hay información escrita. Si seleccionas 'No', se borrará.\n¿Quieres continuar?")
            #
            #     btn_yes = QPushButton("Sí")
            #     btn_no = QPushButton("No")
            #     msg.addButton(btn_yes, QMessageBox.YesRole)
            #     msg.addButton(btn_no, QMessageBox.NoRole)
            #     msg.setDefaultButton(btn_no)
            #
            #     result = msg.exec_()
            #
            #     if msg.clickedButton() == btn_no:
            #         # Revertimos la selección
            #         yes_button.setChecked(True)
            #         return
            #     else:
            #         # Borramos el texto si se confirma
            #         field.clear()
            #         field.setPlaceholderText("")
            #         field.setEnabled(False)