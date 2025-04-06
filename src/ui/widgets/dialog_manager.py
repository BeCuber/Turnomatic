# src/ui/widgets/dialogs.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QRadioButton, QButtonGroup, QMessageBox

class DialogManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Voluntario")
        self.setMinimumWidth(300)

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
        self.btn_save.clicked.connect(self.validate_and_accept)

    def validate_and_accept(self):
        if not self.name_input.text() or not self.lastname1_input.text() or not self.id_card_input.text():
            QMessageBox.warning(self, "Error", "Nombre, primer apellido y documento de identidad son obligatorios.")
            return
        self.accept()  # Cierra el diálogo con resultado OK

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "lastname_1": self.lastname1_input.text(),
            "lastname_2": self.lastname2_input.text(),
            "driver": self.radio_yes.isChecked(),
            "id_card": self.id_card_input.text()
        }
