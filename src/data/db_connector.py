import sqlite3
import os

#class DatabaseManager:
class DatabaseConnector:
    def __init__(self, db_name = "turnomatic.db"):
        """Initialize db and create tables if not exist."""
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.create_tables()


    def create_tables(self):
        """Create tables if not exist."""
        self.c.execute('''CREATE TABLE IF NOT EXISTS volunteer (
                            id_volunteer INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            lastname_1 TEXT NOT NULL,
                            lastname_2 TEXT,
                            driver BOOLEAN NOT NULL DEFAULT 0
                        )''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS availability (
                            id_availability INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_volunteer INTEGER NOT NULL,
                            date_init DATE NOT NULL,
                            date_end DATE NOT NULL,
                            comments TEXT,
                            FOREIGN KEY (id_volunteer) REFERENCES volunteer(id_volunteer) ON DELETE CASCADE
                        )''')

        self.conn.commit()  # Guarda cambios en la base de datos


    def execute_query(self, query, params=()):
        """Método reutilizable para ejecutar consultas SQL""" #TODO traducir
        self.c.execute(query, params)
        self.conn.commit()

    
    def fetch_query(self, query, params=()):
        """Método reutilizable para obtener datos""" #TODO traducir
        self.c.execute(query, params)
        return self.c.fetchall()


    def close_connection(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    db = DatabaseConnector()
    db.close_connection()