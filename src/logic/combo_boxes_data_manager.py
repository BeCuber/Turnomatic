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
    
    def get_province_from_assembly(self, id_assembly):
        """Devuelve el ID de la provincia a partir del ID de la asamblea"""
        query = "SELECT id_province FROM assemblies WHERE id_assembly = ?"
        result = self.db.fetch_query(query, (id_assembly,))
        return result[0][0] if result else None

    def get_ccaa_from_province(self, id_province):
        """Devuelve el ID de la CCAA a partir del ID de la provincia"""
        query = "SELECT id_ccaa FROM provinces WHERE id_province = ?"
        result = self.db.fetch_query(query, (id_province,))
        return result[0][0] if result else None