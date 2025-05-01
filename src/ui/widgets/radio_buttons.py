from PyQt5.QtWidgets import QWidget, QButtonGroup, QRadioButton,QMessageBox, QPlainTextEdit, QPushButton
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager


class RadioButtonsManager():

    def __init__(self, parent: QWidget, db: DatabaseConnector):
        """
        Initializes the radio button manager, groups the buttons and sets up logic.

        Args:
            parent (QWidget): The parent widget containing the radio buttons.
            db (DatabaseConnector): The database connector.
        """
        self.parent = parent
        self.vm = VolunteerManager(db)

        # ButtonGroups
        self.driver_group = QButtonGroup(parent)
        self.exp4x4_group = QButtonGroup(parent)
        self.medication_group = QButtonGroup(parent)
        self.allergy_group = QButtonGroup(parent)

        self.define_form_radio_buttons()

    def define_form_radio_buttons(self):
        """
            Groups the radio buttons by functionality and assigns IDs to "Yes" (1) and "No" (0).
        """

        self.driver_group.addButton(self.parent.findChild(QRadioButton, "radioButtonCarnetYes"), 1)
        self.driver_group.addButton(self.parent.findChild(QRadioButton, "radioButtonCarnetNo"), 0)

        self.exp4x4_group.addButton(self.parent.findChild(QRadioButton, "radioButton4x4Yes"), 1)
        self.exp4x4_group.addButton(self.parent.findChild(QRadioButton, "radioButton4x4No"), 0)

        self.medication_group.addButton(self.parent.findChild(QRadioButton, "radioButtonMedicationYes"), 1)
        self.medication_group.addButton(self.parent.findChild(QRadioButton, "radioButtonMedicationNo"), 0)

        self.allergy_group.addButton(self.parent.findChild(QRadioButton, "radioButtonAllergyYes"), 1)
        self.allergy_group.addButton(self.parent.findChild(QRadioButton, "radioButtonAllergyNo"), 0)


    def display_form_radio_button_data(self, volunteer_data):
        """
            Sets radio buttons based on volunteer data.

            Args:
                volunteer_data (dict): A dictionary containing boolean values for each group.
        """

        if volunteer_data:
            # Asignar los valores a los radio buttons
            self.set_group_checked(self.driver_group, volunteer_data["driver"])
            self.set_group_checked(self.exp4x4_group, volunteer_data["exp4x4"])
            self.set_group_checked(self.medication_group, volunteer_data["medication"])
            self.set_group_checked(self.allergy_group, volunteer_data["allergy"])

            # self.on_radio_changed(medication_group, field)


    def set_group_checked(self, group: QButtonGroup, value: bool):
        """
            Marks the correct radio button in the group based on value.

            Args:
                group (QButtonGroup): The button group.
                value (bool): True for "Yes", False for "No".
        """
        button = group.button(1 if value else 0)
        if button:
            button.setChecked(True)


    def get_current_radio_values(self):
        """
            Returns the current selected values for each group.

            Returns:
                dict: Dictionary with keys 'driver', 'exp4x4', 'medication', 'allergy' and boolean values.
        """
        def get_checked_value(group: QButtonGroup):
            return group.checkedId() == 1

        return {
            "driver": get_checked_value(self.driver_group),
            "exp4x4": get_checked_value(self.exp4x4_group),
            "medication": get_checked_value(self.medication_group),
            "allergy": get_checked_value(self.allergy_group)
        }


    def update_volunteer_radiobtn(self, id_volunteer):
        """
            Updates the volunteer's radio button fields in the database.

            Args:
                id_volunteer (int): The ID of the volunteer to update.
        """
        radio_values = self.get_current_radio_values()
        self.vm.update_volunteer_radiobtn_data(
            id_volunteer,
            driver=radio_values["driver"],
            exp4x4=radio_values["exp4x4"],
            medication=radio_values["medication"],
            allergy=radio_values["allergy"]
        )


    def set_editable(self, editable: bool):
        """
            Enables or disables all radio buttons.

            Args:
                editable (bool): Whether the radio buttons should be editable.
        """
        for group in [self.driver_group, self.exp4x4_group, self.medication_group, self.allergy_group]:
            for btn in group.buttons():
                btn.setEnabled(editable)
                if not editable:
                    btn.setStyleSheet("color: black;")
                else:
                    btn.setStyleSheet("")


    def connect_toggle_with_plaintext(self, group: QButtonGroup, field: QPlainTextEdit):
        """
            Connects the radio buttons to a QPlainTextEdit so it is only enabled when "Yes" is selected.

            Args:
                group (QButtonGroup): The group of radio buttons (Yes/No).
                field (QPlainTextEdit): The associated text field.
        """

        group.button(0).toggled.connect(
            lambda checked: self.on_radio_changed(group, field)
        )


    def on_radio_changed(self, group: QButtonGroup, field: QPlainTextEdit):
        """
            Updates the enabled state of the field based on radio button selection.

            Args:
                group (QButtonGroup): The radio group being monitored.
                field (QPlainTextEdit): The text field to enable or disable.
        """

        if group.checkedId() == 0: # 'No' selected
            text_content = field.toPlainText().strip()
            if text_content:
                msg = QMessageBox(self.parent)
                msg.setWindowTitle("Confirmar acción")
                msg.setText("Hay información escrita. Si seleccionas 'No', se borrará.\n¿Quieres continuar?")

                btn_yes = QPushButton("Sí")
                btn_no = QPushButton("No")
                msg.addButton(btn_yes, QMessageBox.YesRole)
                msg.addButton(btn_no, QMessageBox.NoRole)
                msg.setDefaultButton(btn_no)

                msg.exec_()

                if msg.clickedButton() == btn_no:
                    group.button(1).setChecked(True)
                    return
            field.clear()
            field.setPlaceholderText("")
            field.setEnabled(False)
        else: # 'Sí' selected
            field.setPlaceholderText("Describe la información que se deba tener en cuenta")
            field.setEnabled(True)


