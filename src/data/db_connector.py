import sqlite3
import os


class DatabaseConnector:
    """If database change to other distinct SQLite3, look for uses for ON DELETE CASCADE"""
    def __init__(self, db_name = "turnomatic.db"):
        """Initialize db and create tables if not exist."""
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = sqlite3.connect(self.db_path)
        # Enable ON DELETE CASCADE
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.c = self.conn.cursor()

        

        self.create_tables()


    def create_tables(self):
        """Create tables if not exist."""
        self.c.execute('''CREATE TABLE IF NOT EXISTS volunteer (
                            id_volunteer INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            lastname_1 TEXT NOT NULL,
                            lastname_2 TEXT DEFAULT '',
                            driver BOOLEAN NOT NULL DEFAULT 0, 
                            id_card TEXT UNIQUE,
                            email TEXT,
                            phone TEXT DEFAULT '',
                            birthdate DATE DEFAULT '1900-01-01',
                            position INTEGER,
                            exp4x4 BOOLEAN NOT NULL DEFAULT 0,
                            assembly INTEGER,
                            medication BOOLEAN NOT NULL DEFAULT 0,
                            medication_description TEXT DEFAULT '',
                            allergy BOOLEAN NOT NULL DEFAULT 0,
                            allergy_description TEXT DEFAULT '',
                            contact_person TEXT DEFAULT ''
                        )''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS availability (
                            id_availability INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_volunteer INTEGER NOT NULL,
                            date_init DATE NOT NULL,
                            date_end DATE NOT NULL,
                            comments TEXT,
                            confirmed BOOLEAN DEFAULT 0,
                            FOREIGN KEY (id_volunteer) REFERENCES volunteer(id_volunteer) ON DELETE CASCADE
                        )''')
        
        self.c.execute("CREATE INDEX IF NOT EXISTS idx_availability_date ON availability (date_init, date_end);")
        
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
    """
    db.execute_query("DROP TABLE IF EXISTS availability")
    db.c.execute('''
        CREATE TABLE IF NOT EXISTS availability (
            id_availability INTEGER PRIMARY KEY AUTOINCREMENT,
            id_volunteer INTEGER NOT NULL,
            date_init DATE NOT NULL,
            date_end DATE NOT NULL,
            comments TEXT,
            confirmed BOOLEAN DEFAULT 0,
            FOREIGN KEY (id_volunteer) REFERENCES volunteer(id_volunteer) ON DELETE CASCADE
        )
    ''')
    db.c.execute("CREATE INDEX IF NOT EXISTS idx_availability_date ON availability (date_init, date_end);")
    
    sample_availability = [
        (1, "2025-03-10", "2025-03-12", "Available for transport", 0),
        (1, "2025-03-14", "2025-03-16", "Morning shifts", 1),
        (1, "2025-03-20", "2025-03-22", "", 0),
        (1, "2025-03-25", "2025-03-30", "", 1),
        (1, "2025-04-02", "2025-04-07", "Evening shifts", 1),
        (1, "2025-04-10", "2025-04-15", "", 0),
        (1, "2025-04-18", "2025-04-25", "Weekends only", 1),

        (2, "2025-03-15", "2025-03-17", "Only afternoons", 0),
        (2, "2025-03-18", "2025-03-19", "Only afternoons", 1),
        (2, "2025-03-20", "2025-03-30", "Only afternoons", 0),
        (2, "2025-04-02", "2025-04-10", "Only afternoons", 1),
        (2, "2025-04-11", "2025-04-20", "Only afternoons", 0),
        (2, "2025-04-22", "2025-04-30", "Only afternoons", 1),

        (3, "2025-03-05", "2025-03-12", "", 0),
        (3, "2025-03-14", "2025-03-18", "Transport help", 1),
        (3, "2025-03-20", "2025-03-25", "", 0),
        (3, "2025-04-05", "2025-04-10", "", 1),
        (3, "2025-04-11", "2025-04-15", "", 0),
        (3, "2025-04-17", "2025-04-20", "", 1),
        (3, "2025-04-21", "2025-04-23", "", 0),
    ]


    db.c.executemany(
        "INSERT INTO availability (id_volunteer, date_init, date_end, comments, confirmed) VALUES (?, ?, ?, ?, ?)", 
        sample_availability
    )
    """

    query = "SELECT * FROM volunteer"
    result = db.fetch_query(query)
    print(result)

    query_1= "DELETE FROM volunteer WHERE id_volunteer=4"
    db.execute_query(query_1)

    query_1= "DELETE FROM volunteer WHERE id_volunteer=5"
    db.execute_query(query_1)

    query = "SELECT * FROM volunteer"
    result = db.fetch_query(query)
    print(result)

    db.close_connection()