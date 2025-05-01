from src.data.db_connector import DatabaseConnector


class AvailabilityManager():
    def __init__(self, db: DatabaseConnector):
        self.db = db


    def create_availability(self, id_volunteer, date_init, date_end, comments, confirmed):
        """Validate data and then create a new availability."""

        if not date_init or not date_end:
            raise ValueError("Las fechas de inicio y fin son obligatorias.")

        if date_end < date_init:
            raise ValueError("La fecha de finalización no puede ser anterior a la de inicio.")

        existing_volunteer = self.db.fetch_query_one(
            "SELECT id_volunteer FROM volunteer WHERE id_volunteer = ?", 
            (id_volunteer,)
        )
        if not existing_volunteer:
            raise ValueError("El voluntario no existe.")

        overlapped = self.db.fetch_query_one("""
            SELECT 1 FROM availability 
            WHERE id_volunteer = ? AND NOT (date_end < ? OR date_init > ?)
        """, (id_volunteer, date_init, date_end))

        if overlapped:
            raise ValueError("Ya existe una disponibilidad que solapa con las fechas seleccionadas.")

        query = """
            INSERT INTO availability (id_volunteer, date_init, date_end, comments, confirmed)
            VALUES (?, ?, ?, ?, ?)
        """
        self.db.execute_query(query, (id_volunteer, date_init, date_end, comments, confirmed))

    def read_all_availabilities(self):
        """Get all availabilities in a dictionary"""
        raw_data = self.db.fetch_query_all("SELECT * FROM availability")
        return [{
            "id": v[0], 
            "id_volunteer": v[1], 
            "date_init": v[2], 
            "date_end": v[3], 
            "comments": v[4],
            "confirmed": bool(v[5])
            } for v in raw_data]
    

    def get_availability_by_id_volunteer(self, id_volunteer):
        """Get individual availabilities for a given volunteer."""
        query = "SELECT * FROM availability WHERE id_volunteer = ? ORDER BY date_init DESC"
        raw_data = self.db.fetch_query_all(query, (id_volunteer,))
        return [{
            "id_availability": v[0], 
            "id_volunteer": v[1], 
            "date_init": v[2], 
            "date_end": v[3], 
            "comments": v[4],
            "confirmed": bool(v[5])
            } for v in raw_data]
    

    def update_availability(self, id_availability, id_volunteer, date_init, date_end, comments, confirmed):
        """Update an availibilty."""

        query = "UPDATE availability SET id_volunteer=?, date_init=?, date_end=?, comments=?, confirmed=? WHERE id_availability=?"
        self.db.execute_query(query, (id_volunteer, date_init, date_end, comments, confirmed, id_availability))


    def delete_availability(self, id_availability):
        """Delete an availability."""
        existing = self.db.fetch_query_one("SELECT id_availability FROM availability WHERE id_availability = ?", (id_availability,))
        if not existing:
            raise ValueError("La disponibilidad no existe.")

        query = "DELETE FROM availability WHERE id_availability = ?"
        self.db.execute_query(query, (id_availability,))


    def get_availability_by_date(self, id_volunteer, date):
        """"""
        query = '''SELECT id_availability, date_init, date_end, comments, confirmed FROM availability 
               WHERE id_volunteer = ? AND ? BETWEEN date_init AND date_end'''
        
        return self.db.fetch_query_all(query, (id_volunteer, date))
    

    def get_confirmed_availability_by_id_volunteer(self, id_volunteer, confirmed):
        """"""
        query = '''SELECT id_availability, date_init, date_end, comments 
               FROM availability 
               WHERE id_volunteer = ? AND confirmed = ?
               ORDER BY date_init'''
        return self.db.fetch_query_all(query, (id_volunteer, confirmed))
    

    def isConfirmed(self, id_availability):
        query = '''SELECT confirmed FROM availability WHERE id_availability = ?'''
        result = self.db.fetch_query_one(query, (id_availability,))
        return bool(result[0][0]) if result else False


    def switch_confirmed(self, id_availability):
        current = self.isConfirmed(id_availability)
        new_value = 0 if current else 1
        query = '''UPDATE availability SET confirmed = ? WHERE id_availability = ?'''
        self.db.execute_query(query, (new_value, id_availability))


    def isOverlapped(self, id_volunteer, date_init, date_end):
        query = '''
            SELECT date_init, date_end FROM availability
            WHERE id_volunteer = ?
            AND (
                date_init <= ? AND date_end >= ? -- Solapamiento total o parcial
            )
        '''
        overlapping = self.db.fetch_query_one(query, (id_volunteer, date_end, date_init))
        return overlapping

# from bash: $ python -m src.logic.availability_manager (-m points "src" a module)
if __name__ == "__main__":
    db = DatabaseConnector()
    am = AvailabilityManager(db)

    #print(am.read_all_availabilities()) # it works!
    #am.create_availability(2, "2025-03-24", "2025-03-30", "Carnet A") # it works!
    #am.update_availability(5, 2, "2025-03-25", "2025-03-25", "Carnet A") # it works!
    #am.delete_availability(5) # it works!
    #print(am.read_all_availabilities())


    am.db.close_connection()
