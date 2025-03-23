from src.data.db_connector import DatabaseConnector


class AvailabilityManager():
    def __init__(self, db: DatabaseConnector):
        self.db = db

    
    # CRUD FOR availability #

    def create_availability(self, id_volunteer, date_init, date_end, comments):
        """Validate data and then create a new availability if id_vonteer exists."""

        existing_volunteer = self.db.fetch_query("SELECT id_volunteer FROM volunteer WHERE id_volunteer = ?", (id_volunteer,))
        if not existing_volunteer:
            raise ValueError("El voluntario no existe.") # TODO: Mostrar en ventana de error

        if not date_init or not date_end:
            raise ValueError("Las fechas de inicio y fin son obligatorias") # TODO: Mostrar en ventana de error

        query = "INSERT INTO availability (id_volunteer, date_init, date_end, comments) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (id_volunteer, date_init, date_end, comments))


    def read_all_availabilities(self):
        """Get all availabilities in a dictionary"""
        raw_data = self.db.fetch_query("SELECT * FROM availability")
        return [{
            "id": v[0], 
            "id_volunteer": v[1], 
            "date_init": v[2], 
            "date_end": v[3], 
            "comments": v[4]
            } for v in raw_data]
    

    def update_availability(self, id_availability, id_volunteer, date_init, date_end, comments):
        """Update an availibilty."""

        query = "UPDATE availability SET id_volunteer=?, date_init=?, date_end=?, comments=? WHERE id_availability=?"
        self.db.execute_query(query, (id_volunteer, date_init, date_end, comments, id_availability))


    def delete_availability(self, id_availability):
        """Delete an availability."""

        query = "DELETE FROM availability WHERE id_availability = ?"
        self.db.execute_query(query, (id_availability,))



    # END CRUD FOR availability #


# from bash: $ python -m src.logic.availability_manager (-m points "src" a module)
if __name__ == "__main__":
    am = AvailabilityManager()

    print(am.read_all_availabilities()) # it works!
    #am.create_availability(2, "2025-03-24", "2025-03-30", "Carnet A") # it works!
    #am.update_availability(5, 2, "2025-03-25", "2025-03-25", "Carnet A") # it works!
    #am.delete_availability(5) # it works!
    print(am.read_all_availabilities())



    am.db.close_connection()
