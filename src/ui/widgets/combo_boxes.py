from PyQt5.QtWidgets import QMainWindow, QComboBox
from PyQt5.QtCore import Qt
from src.data.db_connector import DatabaseConnector
from src.logic.location_manager import LocationManager


class ComboBoxManager():
    
    def __init__(self, main_window: QMainWindow, db: DatabaseConnector):
        """Initilize combo boxes manager."""
        self.main_window = main_window
        #self.db = db
        self.lm = LocationManager(db)
        self.define_combobox_widgets()
        self.populate_combobox_ccaa()
        self.connect_signals()

    def define_combobox_widgets(self):
        """Defines all combobox"""

        self.combobox_ccaa = self.main_window.findChild(QComboBox, "comboBoxCcaa")
        self.combobox_provinces = self.main_window.findChild(QComboBox, "comboBoxProvince")
        self.combobox_assemblies = self.main_window.findChild(QComboBox, "comboBoxAssembly")

        # Disable dependant combobox by default
        self.combobox_provinces.setEnabled(False)
        self.combobox_assemblies.setEnabled(False)

    def populate_combobox_ccaa(self):
        """Load data from ccaa table in database"""
        #query = "SELECT id_ccaa, name FROM ccaa ORDER BY name"
        #results = self.db.fetch_query(query)

        self.combobox_ccaa.clear() 
        self.combobox_ccaa.addItem("Selecciona una CCAA", -1) # Default option
        #for id_ccaa, name in results:
        for id_ccaa, name in self.lm.get_ccaa():
            self.combobox_ccaa.addItem(name, id_ccaa)
        
        self.populate_combobox_provinces(self.combobox_ccaa.currentData())

    def populate_combobox_provinces(self, id_ccaa):
        "Load data from provinces depending on ccaa selected in comboBoxCcaa"
        #id_ccaa = self.combobox_ccaa.currentData()

        if id_ccaa == -1: # If CCAA selected is not valid
            self.combobox_provinces.clear()
            self.combobox_provinces.setEnabled(False)

            self.combobox_assemblies.clear()
            self.combobox_assemblies.setEnabled(False) 

            return
        
        #query = "SELECT id_province, name FROM provinces WHERE id_ccaa = ? ORDER BY name"
        #results = self.db.fetch_query(query, (id_ccaa,))

        self.combobox_provinces.clear()
        self.combobox_provinces.addItem("Selecciona una provincia", -1)
        #for id_province, name in results:
        for id_province, name in self.lm.get_provinces(id_ccaa):
            self.combobox_provinces.addItem(name, id_province)

        self.combobox_provinces.setEnabled(True)

        self.populate_combobox_assemblies(self.combobox_provinces.currentData())

    def populate_combobox_assemblies(self, id_province):
        "Load data from assemblies depending on province selected in comboBoxProvince"
        #id_province = self.combobox_provinces.currentData()

        if id_province == -1:
            self.combobox_assemblies.clear()
            self.combobox_assemblies.setEnabled(False)
            return
        
        #query = "SELECT id_assembly, name FROM assemblies WHERE id_province = ? ORDER BY name"
        #results = self.db.fetch_query(query, (id_province,))

        self.combobox_assemblies.clear()
        self.combobox_assemblies.addItem("Selecciona una asamblea", -1)
        #for id_assembly, name in results:
        for id_assembly, name in self.lm.get_assemblies(id_province):
            self.combobox_assemblies.addItem(name, id_assembly)

        self.combobox_assemblies.setEnabled(True)

    def connect_signals(self):
        """Conects comboboxes"""
        self.combobox_ccaa.currentIndexChanged.connect(lambda: self.populate_combobox_provinces(self.combobox_ccaa.currentData()))
        self.combobox_provinces.currentIndexChanged.connect(lambda: self.populate_combobox_assemblies(self.combobox_provinces.currentData()))