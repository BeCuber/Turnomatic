from src.data.db_connector import DatabaseConnector

class FormManager:
    def __init__(self, db: DatabaseConnector):
        self.db = db

    def get_positions(self):
        query = "SELECT position FROM positions"
        return self.db.fetch_query(query)
    
    