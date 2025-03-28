from src.data.db_connector import DatabaseConnector

class ComboBoxesDataManager:
    def __init__(self, db: DatabaseConnector):
        self.db = db

    def get_ccaa(self):
        query = "SELECT id_ccaa, name FROM ccaa ORDER BY name"
        return self.db.fetch_query(query)

    def get_provinces(self, id_ccaa):
        query = "SELECT id_province, name FROM provinces WHERE id_ccaa = ? ORDER BY name"
        return self.db.fetch_query(query, (id_ccaa,))

    def get_assemblies(self, id_province):
        query = "SELECT id_assembly, name FROM assemblies WHERE id_province = ? ORDER BY name"
        return self.db.fetch_query(query, (id_province,))
    
    def get_positions(self):
        query = "SELECT position FROM positions"
        return self.db.fetch_query(query)