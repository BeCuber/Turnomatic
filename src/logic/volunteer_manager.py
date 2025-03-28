from src.data.db_connector import DatabaseConnector

class VolunteerManager:
    def __init__(self, db: DatabaseConnector):
        self.db = db
    

    # CRUD FOR volunteers #

    def create_volunteer(self, name, lastname_1, lastname_2, driver):
        """Validate data and then create a new volunteer in database."""
        
        if not name or not lastname_1:
            raise ValueError("El nombre y el primer apellido son obligatorios.") #TODO aviso en ventana de error
        
        query = "INSERT INTO volunteer (name, lastname_1, lastname_2, driver) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (name, lastname_1, lastname_2, driver))
        

    def read_all_volunteers(self):
        """Get all volunteers in a dictionary"""
        raw_data = self.db.fetch_query("SELECT * FROM volunteer ORDER BY name")
        return [{
            "id_volunteer": v[0], 
            "name": v[1], 
            "lastname_1": v[2], 
            "lastname_2": v[3], 
            "driver": bool(v[4])
            } for v in raw_data]



    def update_volunteer(self, name, lastname_1, lastname_2, driver, id_volunteer):
        """Verifies volunteer exists before updating."""
        existing_volunteer = self.db.fetch_query("SELECT id_volunteer FROM volunteer WHERE id_volunteer = ?", (id_volunteer,))
        if not existing_volunteer:
            raise ValueError("El voluntario no existe.")  # TODO: Mostrar en ventana de error
                
        query = "UPDATE volunteer SET name=?, lastname_1=?, lastname_2=?, driver=? WHERE id_volunteer=?"
        self.db.execute_query(query, (name, lastname_1, lastname_2, driver, id_volunteer))


    def delete_volunteer(self, id_volunteer):
        """Delete a volunteer after confirm exists."""
        existing_volunteer = self.db.fetch_query("SELECT id_volunteer FROM volunteer WHERE id_volunteer = ?", (id_volunteer,))
        if not existing_volunteer:
            raise ValueError("El voluntario no existe.")  # TODO: Mostrar en ventana de error
        

        query = "DELETE FROM volunteer WHERE id_volunteer = ?"
        self.db.execute_query(query, (id_volunteer,))

    # END CRUD FOR volunteers #



    # SPECIFIC QUERYS

    def check_volunteers_in_date(self, date):
        """Check how many volunteers are available on a given day"""
        query = '''SELECT v.name, v.lastname_1, v.lastname_2, v.driver, a.date_init, a.date_end, a.comments
                FROM volunteer v
                JOIN availability a ON v.id_volunteer = a.id_volunteer
                WHERE ? BETWEEN a.date_init AND a.date_end'''
        
        raw_data = self.db.fetch_query(query, (date,))

        # Convertimos la lista de tuplas en una lista de diccionarios
        return [{
            "name": v[0], 
            "lastname_1": v[1], 
            "lastname_2": v[2], 
            "driver": bool(v[3]),  
            "date_init": v[4],  
            "date_end": v[5],  
            "comments": v[6]  
        } for v in raw_data]
    
   
    
    # FOR TESTING:
    def insert_sample_data(self):
        """Insert sample data to test."""
        sample_volunteers = [
            ("Alice", "Smith", "Brown", 1),
            ("Bob", "Johnson", "Davis", 0),
            ("Charlie", "Miller", "Wilson", 1),
        ]
        self.db.c.executemany("INSERT INTO volunteer (name, lastname_1, lastname_2, driver) VALUES (?, ?, ?, ?)", sample_volunteers)

        sample_availability = [
            (1, "2025-03-10", "2025-03-12", "Available for transport"),
            (1, "2025-03-20", "2025-03-22", ""),
            (1, "2025-03-25", "2025-03-30", ""),
            (2, "2025-03-15", "2025-03-17", "Only afternoons"),
            (2, "2025-03-20", "2025-03-30", "Only afternoons"),
            (3, "2025-03-05", "2025-03-25", ""),
        ]
        self.db.c.executemany("INSERT INTO availability (id_volunteer, date_init, date_end, comments) VALUES (?, ?, ?, ?)", sample_availability)

        self.db.conn.commit()


# from bash: $ python -m src.logic.volunteer_manager (-m points "src" a module)
if __name__ == "__main__":
    db = DatabaseConnector()
    vm = VolunteerManager(db)

    #print(vm.read_all_volunteers()) # it works!
    #vm.create_volunteer("Feliniberto", "McFalso", "Salvaje", 1) # it works!
    #vm.update_volunteer("Feliniberto", "McFalso", "Maullador", 1, 4) # it works!
    #vm.delete_volunteer(4) # it also works!
    #print(vm.read_all_volunteers())
    
    #volunteers = vm.read_all_volunteers()
    #print(volunteers)  # Para ver toda la lista

    # Verificar el tipo de v[2] en cada voluntario
    #for v in volunteers:
     #   print(f"Valor de v[2]: {v['driver']} (Tipo: {type(v['driver'])})")

    vm.insert_sample_data()
    

    vm.db.close_connection()