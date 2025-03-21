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


    def check_volunteers_in_date(self, date):
        """Check how many volunteers are available in one day"""
        self.c.execute('''SELECT v.name, v.lastname_1, v.lastname_2, a.date_init, a.date_end, a.comments
                            FROM volunteer v
                            JOIN availability a ON v.id_volunteer = a.id_volunteer
                            WHERE ? BETWEEN a.date_init AND a.date_end''', (date,))
        return self.c.fetchall() # Devuelve una lista con los resultados
    
    def insert_sample_data(self):
        """Insert sample data to test."""
        sample_volunteers = [
            ("Alice", "Smith", "Brown", 1),
            ("Bob", "Johnson", "Davis", 0),
            ("Charlie", "Miller", "Wilson", 1),
        ]
        self.c.executemany("INSERT INTO volunteer (name, lastname_1, lastname_2, driver) VALUES (?, ?, ?, ?)", sample_volunteers)

        sample_availability = [
            (1, "2025-03-10", "2025-03-12", "Available for transport"),
            (1, "2025-03-20", "2025-03-22", ""),
            (2, "2025-03-15", "2025-03-17", "Only afternoons"),
            (3, "2025-03-05", "2025-03-25", ""),
        ]
        self.c.executemany("INSERT INTO availability (id_volunteer, date_init, date_end, comments) VALUES (?, ?, ?, ?)", sample_availability)

        self.conn.commit()

    def close_connection(self):
        """Close database connection"""
        self.conn.close()

# Si quieres probarlo, descomenta estas líneas:
# db = DatabaseManager()
# db.close_connection()