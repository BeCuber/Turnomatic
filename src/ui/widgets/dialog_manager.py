# src/ui/widgets/dialogs.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QRadioButton, QButtonGroup, QMessageBox, QDateEdit, QTextEdit, QCheckBox, QDialogButtonBox
from PyQt5.QtCore import QDate

class DialogManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setMinimumWidth(300)


    def new_volunteer_dialog(self):
        """"""
        self.setWindowTitle("Nuevo Voluntario")
        layout = QVBoxLayout()

        # Campos de entrada
        self.name_input = QLineEdit()
        self.lastname1_input = QLineEdit()
        self.lastname2_input = QLineEdit()
        self.id_card_input = QLineEdit()

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Primer apellido:"))
        layout.addWidget(self.lastname1_input)
        layout.addWidget(QLabel("Segundo apellido:"))
        layout.addWidget(self.lastname2_input)
        layout.addWidget(QLabel("NIF/NIE/Pasaporte:"))
        layout.addWidget(self.id_card_input)

        # Radio buttons para driver
        layout.addWidget(QLabel("¿Conduce?"))
        self.radio_group = QButtonGroup(self)
        self.radio_yes = QRadioButton("Sí")
        self.radio_no = QRadioButton("No")
        self.radio_no.setChecked(True)  # por defecto no

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_yes)
        radio_layout.addWidget(self.radio_no)

        self.radio_group.addButton(self.radio_yes)
        self.radio_group.addButton(self.radio_no)

        layout.addLayout(radio_layout)

        # Botones
        buttons_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_save = QPushButton("Guardar")

        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_save)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        # Conexiones
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.validate_volunteer_and_accept)

        return self


    def validate_volunteer_and_accept(self):
        if not self.name_input.text() or not self.lastname1_input.text() or not self.id_card_input.text():
            QMessageBox.warning(self, "Error", "Nombre, primer apellido y documento de identidad son obligatorios.")
            return
        self.accept()  # Cierra el diálogo con resultado OK


    def get_new_volunteer_data(self):
        return {
            "name": self.name_input.text(),
            "lastname_1": self.lastname1_input.text(),
            "lastname_2": self.lastname2_input.text(),
            "driver": self.radio_yes.isChecked(),
            "id_card": self.id_card_input.text()
        }


    def new_availability_dialog(self):
        self.setWindowTitle("Nueva disponibilidad")
        layout = QVBoxLayout()

        self.date_init = QDateEdit()
        self.date_init.setCalendarPopup(True)
        self.date_init.setDate(QDate.currentDate())

        self.date_end = QDateEdit()
        self.date_end.setCalendarPopup(True)
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setMinimumDate(self.date_init.date())

        self.date_init.dateChanged.connect(self.update_end_date)

        self.comments_input = QLineEdit()
        self.confirmed_checkbox = QCheckBox("¿Confirmado?")

        layout.addWidget(QLabel("Fecha inicio:"))
        layout.addWidget(self.date_init)

        layout.addWidget(QLabel("Fecha fin:"))
        layout.addWidget(self.date_end)

        layout.addWidget(QLabel("Comentarios:"))
        layout.addWidget(self.comments_input)

        layout.addWidget(self.confirmed_checkbox)

        # Botones
        buttons_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_save = QPushButton("Guardar")

        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_save)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept)

        return self

    def update_end_date(self, new_date):
        self.date_end.setMinimumDate(new_date)
        if self.date_end.date() < new_date:
            self.date_end.setDate(new_date)

    def get_new_availability_data(self):
        return {
            "date_init": self.date_init.date().toString("yyyy-MM-dd"),
            "date_end": self.date_end.date().toString("yyyy-MM-dd"),
            "comments": self.comments_input.text(),
            "confirmed": self.confirmed_checkbox.isChecked()
        }
