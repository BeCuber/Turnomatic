import sqlite3
import os


class DatabaseConnector:
    """If database change to other distinct SQLite3, look for uses for ON DELETE CASCADE"""
    def __init__(self, db_name = "turnomatic.db"):
        """Initialize db and create tables if not exist."""
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

        # Enable ON DELETE CASCADE
        self.c.execute("PRAGMA foreign_keys = ON;")

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
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS ccaa (
                            id_ccaa INTEGER PRIMARY KEY,
                            name TEXT NOT NULL
                        )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS provinces (
                            id_province INTEGER PRIMARY KEY,
                            id_ccaa INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            FOREIGN KEY (id_ccaa) REFERENCES ccaa(id_ccaa) ON DELETE CASCADE
                        )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS assemblies (
                            id_assembly INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_province INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            FOREIGN KEY (id_province) REFERENCES provinces(id_province) ON DELETE CASCADE
                        )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS positions (
                        id_position INTEGER PRIMARY KEY AUTOINCREMENT,
                        position TEXT NOT NULL
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

    query = "SELECT COUNT(*) from ccaa;"
    print("ccaa: " + str(db.fetch_query(query)))

    query = "SELECT COUNT(*) from provinces;"
    print("provinces: " + str(db.fetch_query(query)))

    query = "SELECT COUNT(*) from assemblies;"
    print("assemblies: " + str(db.fetch_query(query)))

    db.close_connection()