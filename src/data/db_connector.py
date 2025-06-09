import sqlite3
from src.utils.path_helper import get_resource_path


class DatabaseConnector:
    """
        If database change to other distinct SQLite3, look for uses for ON DELETE CASCADE

        Handles connection and operations for an SQLite3 database.

        Attributes:
            db_path (str): Full path to the database file.
            conn (sqlite3.Connection): Active connection to the database.

        Notes:
            - Enables foreign key constraints (PRAGMA foreign_keys = ON).
            - Always closes the cursor to prevent memory leaks.
    """
    def __init__(self, db_name = "src/data/turnomatic.db"):
        """
            Initializes the database connection and creates tables if they do not exist.

        Args:
            db_name (str): Name of the SQLite database file. Default is "turnomatic.db".
        """
        # self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.db_path = get_resource_path(db_name)
        self.conn = sqlite3.connect(self.db_path)
        # Enable ON DELETE CASCADE
        self.conn.execute("PRAGMA foreign_keys = ON;")

        self.create_tables()


    def create_tables(self):
        """
        Calls internal methods to create all required tables.
        """
        self._create_table_volunteer()
        self._create_table_availability()
        self._create_table_ccaa()
        self._create_table_provinces()
        self._create_table_assemblies()
        self._create_table_positions()
        self._create_table_rooms()
        self._create_table_room_assignment()
        self.conn.commit()


    def _create_table_volunteer(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS volunteer (
                    id_volunteer INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    lastname_1 TEXT NOT NULL,
                    lastname_2 TEXT DEFAULT '',
                    driver BOOLEAN NOT NULL DEFAULT 0, 
                    id_card TEXT UNIQUE,
                    email TEXT,
                    phone TEXT DEFAULT '',
                    birthdate TEXT DEFAULT '1900-01-01',
                    position INTEGER,
                    exp4x4 BOOLEAN NOT NULL DEFAULT 0,
                    assembly INTEGER,
                    medication BOOLEAN NOT NULL DEFAULT 0,
                    medication_description TEXT DEFAULT '',
                    allergy BOOLEAN NOT NULL DEFAULT 0,
                    allergy_description TEXT DEFAULT '',
                    contact_person TEXT DEFAULT ''
                )
            ''')
        finally:
            cursor.close()

    def _create_table_availability(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS availability (
                    id_availability INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_volunteer INTEGER NOT NULL,
                    date_init TEXT NOT NULL,
                    date_end TEXT NOT NULL,
                    comments TEXT,
                    confirmed BOOLEAN DEFAULT 0,
                    FOREIGN KEY (id_volunteer) REFERENCES volunteer(id_volunteer) ON DELETE CASCADE
                )
            ''')
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_availability_date ON availability (date_init, date_end);")
        finally:
            cursor.close()

    def _create_table_ccaa(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ccaa (
                    id_ccaa INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            ''')
        finally:
            cursor.close()

    def _create_table_provinces(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS provinces (
                    id_province INTEGER PRIMARY KEY,
                    id_ccaa INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    FOREIGN KEY (id_ccaa) REFERENCES ccaa(id_ccaa) ON DELETE CASCADE
                )
            ''')
        finally:
            cursor.close()

    def _create_table_assemblies(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS assemblies (
                    id_assembly INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_province INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    FOREIGN KEY (id_province) REFERENCES provinces(id_province) ON DELETE CASCADE
                )
            ''')
        finally:
            cursor.close()

    def _create_table_positions(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS positions (
                    id_position INTEGER PRIMARY KEY AUTOINCREMENT,
                    position TEXT NOT NULL
                )
            ''')
        finally:
            cursor.close()

    def _create_table_rooms(self):
        """
            Create rooms table.
            Each row represents a room with its number of beds (capacity).
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rooms (
                    id_room INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_name TEXT UNIQUE NOT NULL,
                    capacity INT DEFAULT 1
                )
            ''')
        finally:
            cursor.close()

    def _create_table_room_assignment(self):
        """
            Create the room assignment table.
            Each row represents the occupancy of a room on a specific date
            by a volunteer (based on their availability).
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS room_assignment (
                    id_assignment INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_room INTEGER NOT NULL,
                    id_availability INTEGER NOT NULL,
                    check_in TEXT NOT NULL,
                    check_out TEXT NOT NULL,
                    FOREIGN KEY (id_room) REFERENCES rooms(id_room) ON DELETE CASCADE,
                    FOREIGN KEY (id_availability) REFERENCES availability(id_availability) ON DELETE CASCADE
                )
            ''')
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_room_assignment ON room_assignment (check_in, check_out);")
        finally:
            cursor.close()


    def execute_query(self, query, params=()):
        """
            Executes a write query (INSERT, UPDATE, DELETE).

            Args:
                query (str): SQL query string.
                params (tuple): Optional parameters for the query.

            Raises:
                sqlite3.Error: If an error occurs during execution.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error al ejecutar query:", e)
            self.conn.rollback()
            raise
        finally:
            cursor.close()


    def execute_many_query(self, query, params=()):
        """
            Executes a write query for multiple sets of parameters (INSERT, UPDATE, DELETE).

            Args:
                query (str): SQL query string.
                params (list of tuple): List of parameter tuples for the query.
                                         Defaults to an empty tuple if no parameters are provided.

            Raises:
                sqlite3.Error: If an error occurs during execution.
            """

        cursor = self.conn.cursor()
        try:
            cursor.executemany(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error al ejecutar executemany:", e)
            self.conn.rollback()
            raise
        finally:
            cursor.close()
    
    def fetch_query_all(self, query, params=()):
        """
            Executes a SELECT query and returns all results.

            Args:
                query (str): SQL query string.
                params (tuple): Optional parameters for the query.

            Returns:
                list of tuple: The result set.

            Raises:
                sqlite3.Error: If an error occurs during execution.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print("Error al ejecutar fetch:", e)
            raise
        finally:
            cursor.close()


    def fetch_query_one(self, query, params=()):
        """
            Executes a SELECT query and returns a single result.

            Args:
                query (str): SQL query string.
                params (tuple): Optional parameters for the query.

            Returns:
                tuple or None: The first row of the result, or None if empty.

            Raises:
                sqlite3.Error: If an error occurs during execution.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print("Error al ejecutar fetch", e)
            raise
        finally:
            cursor.close()


    def get_last_inserted_id(self):
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]


    def close_connection(self):
        """
        Closes the database connection.
        """
        self.conn.close()


if __name__ == "__main__":
    db = DatabaseConnector()
    # """
    # db.execute_query("DROP TABLE IF EXISTS room_assignment")
    # db.c.execute('''
    #     CREATE TABLE IF NOT EXISTS availability (
    #         id_availability INTEGER PRIMARY KEY AUTOINCREMENT,
    #         id_volunteer INTEGER NOT NULL,
    #         date_init DATE NOT NULL,
    #         date_end DATE NOT NULL,
    #         comments TEXT,
    #         confirmed BOOLEAN DEFAULT 0,
    #         FOREIGN KEY (id_volunteer) REFERENCES volunteer(id_volunteer) ON DELETE CASCADE
    #     )
    # ''')
    # db.c.execute("CREATE INDEX IF NOT EXISTS idx_availability_date ON availability (date_init, date_end);")
    #
    # sample_availability = [
    #     (1, "2025-03-10", "2025-03-12", "Available for transport", 0),
    #     (1, "2025-03-14", "2025-03-16", "Morning shifts", 1),
    #     (1, "2025-03-20", "2025-03-22", "", 0),
    #     (1, "2025-03-25", "2025-03-30", "", 1),
    #     (1, "2025-04-02", "2025-04-07", "Evening shifts", 1),
    #     (1, "2025-04-10", "2025-04-15", "", 0),
    #     (1, "2025-04-18", "2025-04-25", "Weekends only", 1),
    #
    #     (2, "2025-03-15", "2025-03-17", "Only afternoons", 0),
    #     (2, "2025-03-18", "2025-03-19", "Only afternoons", 1),
    #     (2, "2025-03-20", "2025-03-30", "Only afternoons", 0),
    #     (2, "2025-04-02", "2025-04-10", "Only afternoons", 1),
    #     (2, "2025-04-11", "2025-04-20", "Only afternoons", 0),
    #     (2, "2025-04-22", "2025-04-30", "Only afternoons", 1),
    #
    #     (3, "2025-03-05", "2025-03-12", "", 0),
    #     (3, "2025-03-14", "2025-03-18", "Transport help", 1),
    #     (3, "2025-03-20", "2025-03-25", "", 0),
    #     (3, "2025-04-05", "2025-04-10", "", 1),
    #     (3, "2025-04-11", "2025-04-15", "", 0),
    #     (3, "2025-04-17", "2025-04-20", "", 1),
    #     (3, "2025-04-21", "2025-04-23", "", 0),
    # ]
    #
    #
    # db.c.executemany(
    #     "INSERT INTO availability (id_volunteer, date_init, date_end, comments, confirmed) VALUES (?, ?, ?, ?, ?)",
    #     sample_availability
    # )
    # """

    # db.execute_query("DROP TABLE IF EXISTS bed_assignment")

    # db.execute_query("DROP TABLE IF EXISTS room_assignment")
    query = "SELECT name FROM sqlite_master WHERE type='table';"

    print(db.fetch_query_all(query))

    db.close_connection()