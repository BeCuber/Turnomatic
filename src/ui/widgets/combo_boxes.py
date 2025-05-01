from PyQt5.QtWidgets import QComboBox, QWidget
from src.data.db_connector import DatabaseConnector
from src.logic.combo_boxes_data_manager import ComboBoxesDataManager
from src.logic.volunteer_manager import VolunteerManager


class ComboBoxManager():
    
    def __init__(self, parent: QWidget, db: DatabaseConnector):
        """Initilize combo boxes manager."""
        self.parent = parent
        self.vm = VolunteerManager(db)
        self.cbdm = ComboBoxesDataManager(db)


    def define_form_combobox(self):
        """Defines form combobox"""

        self.combobox_ccaa = self.parent.findChild(QComboBox, "comboBoxCcaa")
        self.combobox_provinces = self.parent.findChild(QComboBox, "comboBoxProvince")
        self.combobox_assemblies = self.parent.findChild(QComboBox, "comboBoxAssembly")
        self.combobox_positions = self.parent.findChild(QComboBox, "comboBoxPosition")

        # Disable dependant combobox by default
        self.combobox_provinces.setEnabled(False)
        self.combobox_assemblies.setEnabled(False)

        # Populate form comboboxes
        self.populate_combobox_ccaa()
        self.connect_signals()
        self.populate_combobox_positions()


    def display_selected_volunteer_combobox_data(self, volunteer_data):
        """Show data from selected volunteer on table."""

        if volunteer_data:
            self.combobox_positions.setCurrentIndex(volunteer_data['position'])

            id_assembly = volunteer_data["assembly"]

            self.combobox_ccaa.setCurrentIndex(-1)
            self.combobox_provinces.setCurrentIndex(-1)
            self.combobox_assemblies.setCurrentIndex(-1)

            id_province = self.cbdm.get_province_from_assembly(id_assembly)
            if not id_province:
                return

            id_ccaa = self.cbdm.get_ccaa_from_province(id_province)
            if not id_ccaa:
                return

            index_ccaa = self.combobox_ccaa.findData(id_ccaa)
            self.combobox_ccaa.setCurrentIndex(index_ccaa)

            index_province = self.combobox_provinces.findData(id_province)
            self.combobox_provinces.setCurrentIndex(index_province)

            index_assembly = self.combobox_assemblies.findData(id_assembly)           
            self.combobox_assemblies.setCurrentIndex(index_assembly)
        

    def populate_combobox_positions(self):
        "Load data from positions."

        self.combobox_positions.clear()
        self.combobox_positions.addItem("Selecciona un puesto", -1)

        for position in self.cbdm.get_positions():
            self.combobox_positions.addItem(position[0])


    def populate_combobox_ccaa(self):
        """Load data from ccaa table in database"""

        self.combobox_ccaa.clear() 
        self.combobox_ccaa.addItem("Selecciona una CCAA", -1) # Default option

        for id_ccaa, name in self.cbdm.get_ccaa():
            self.combobox_ccaa.addItem(name, id_ccaa)
        
        self.populate_combobox_provinces(self.combobox_ccaa.currentData())


    def populate_combobox_provinces(self, id_ccaa):
        "Load data from provinces depending on ccaa selected in comboBoxCcaa"

        if id_ccaa == -1: # If CCAA selected is not valid
            self.combobox_provinces.clear()
            self.combobox_provinces.setEnabled(False)

            self.combobox_assemblies.clear()
            self.combobox_assemblies.setEnabled(False) 

            return
        
        self.combobox_provinces.clear()
        self.combobox_provinces.addItem("Selecciona una provincia", -1)

        for id_province, name in self.cbdm.get_provinces(id_ccaa):
            self.combobox_provinces.addItem(name, id_province)

        self.combobox_provinces.setEnabled(True)

        self.populate_combobox_assemblies(self.combobox_provinces.currentData())


    def populate_combobox_assemblies(self, id_province):
        "Load data from assemblies depending on province selected in comboBoxProvince"

        if id_province == -1:
            self.combobox_assemblies.clear()
            self.combobox_assemblies.setEnabled(False)
            return
        
        self.combobox_assemblies.clear()
        self.combobox_assemblies.addItem("Selecciona una asamblea", -1)

        for id_assembly, name in self.cbdm.get_assemblies(id_province):
            self.combobox_assemblies.addItem(name, id_assembly)

        self.combobox_assemblies.setEnabled(True)


    def connect_signals(self):
        """Conects comboboxes"""
        self.combobox_ccaa.currentIndexChanged.connect(lambda: self.populate_combobox_provinces(self.combobox_ccaa.currentData()))
        self.combobox_provinces.currentIndexChanged.connect(lambda: self.populate_combobox_assemblies(self.combobox_provinces.currentData()))


    def set_editable(self, editable: bool):
        """"""
        readonly_style = "QComboBox { background-color: #f5f5f5; border: 1px solid #ccc; }"
        editable_style = ""

        self.combobox_ccaa.setEnabled(editable)
        self.combobox_provinces.setEnabled(editable)
        self.combobox_assemblies.setEnabled(editable)
        self.combobox_positions.setEnabled(editable)

        style = editable_style if editable else readonly_style

        self.combobox_ccaa.setStyleSheet(style)
        self.combobox_provinces.setStyleSheet(style)
        self.combobox_assemblies.setStyleSheet(style)
        self.combobox_positions.setStyleSheet(style)

    def update_volunteer_combobox(self, id_volunteer):
        self.vm.update_volunteer_combobox_data(
            id_volunteer,
            position=self.combobox_positions.currentIndex(),
            assembly=self.combobox_assemblies.currentData()
        )