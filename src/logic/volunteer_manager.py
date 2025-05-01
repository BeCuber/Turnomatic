# from PyQt5.QtCore.QUrl import query

from src.data.db_connector import DatabaseConnector

class VolunteerManager:
    def __init__(self, db: DatabaseConnector):
        self.db = db
    

    def create_volunteer(self, name, lastname_1, lastname_2, driver, id_card, email, phone, birthdate, position, exp4x4, assembly, medication, medication_description, allergy, allergy_description, contact_person):
        """Validate data and then create a new volunteer in database."""
        
        if not name or not lastname_1 or not id_card:
            raise ValueError("Nombre, primer apellido e ID son obligatorios.") #TODO aviso en ventana de error
        
        query = "INSERT INTO volunteer (name, lastname_1, lastname_2, driver, id_card, email, phone, birthdate, position, exp4x4, assembly, medication, medication_description, allergy, allergy_description, contact_person) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.db.execute_query(query, (name, lastname_1, lastname_2, driver, id_card, email, phone, birthdate, position, exp4x4, assembly, medication, medication_description, allergy, allergy_description, contact_person))
        
        return self.db.c.lastrowid  # ← Aquí devolvemos el nuevo ID


    def read_all_volunteers(self):
        """Get all volunteers in a dictionary"""
        raw_data = self.db.fetch_query_all("SELECT * FROM volunteer ORDER BY name")
        return [{
            "id_volunteer": v[0],
            "name": v[1],
            "lastname_1": v[2],
            "lastname_2": v[3] or '',
            "driver": bool(v[4]),
            "id_card": v[5] or '',
            "email": v[6] or '',
            "phone": v[7] or '',
            "birthdate": v[8],
            "position": v[9],
            "exp4x4": bool(v[10]),
            "assembly": v[11],
            "medication": bool(v[12]),
            "medication_description": v[13] or '',
            "allergy": bool(v[14]),
            "allergy_description": v[15] or '',
            "contact_person": v[16] or ''
            } for v in raw_data]
    

    def get_volunteer_by_id(self, volunteer_id):
        """Get a volunteer from his id."""
        query = "SELECT * FROM volunteer WHERE id_volunteer = ?"
        result = self.db.fetch_query_one(query, (volunteer_id,))

        if not result:
            return None  # Si no hay datos, devolver None

        v = result

        # Mapear columnas manualmente
        return {
            "id_volunteer": v[0],
            "name": v[1],
            "lastname_1": v[2],
            "lastname_2": v[3] or '',
            "driver": bool(v[4]),
            "id_card": v[5] or '',
            "email": v[6] or '',
            "phone": v[7] or '',
            "birthdate": v[8],
            "position": v[9],
            "exp4x4": bool(v[10]),
            "assembly": v[11],
            "medication": bool(v[12]),
            "medication_description": v[13] or '',
            "allergy": bool(v[14]),
            "allergy_description": v[15] or '',
            "contact_person": v[16] or ''
        }


    def update_volunteer_name(self, id_volunteer, field_name, new_value):
        """"""

        query = f"UPDATE volunteer SET {field_name} = ? WHERE id_volunteer = ?"
        self.db.execute_query(query, (new_value, id_volunteer))


    def update_volunteer(self, name, lastname_1, lastname_2, driver, id_card, email, phone, birthdate, position, exp4x4, assembly, medication, medication_description, allergy, allergy_description, contact_person, id_volunteer):
        """Verifies volunteer exists before updating."""
        existing_volunteer = self.db.fetch_query_one("SELECT id_volunteer FROM volunteer WHERE id_volunteer = ?", (id_volunteer,))
        if not existing_volunteer:
            raise ValueError("El voluntario no existe.")  # TODO: Mostrar en ventana de error

        query = "UPDATE volunteer SET name=?, lastname_1=?, lastname_2=?, driver=?, id_card=?, email=?, phone=?, birthdate=?, position=?, exp4x4=?, assembly=?, medication=?, medication_description=?, allergy=?, allergy_description=?, contact_person=? WHERE id_volunteer=?"
        self.db.execute_query(query, (name, lastname_1, lastname_2, driver, id_card, email, phone, birthdate, position, exp4x4, assembly, medication, medication_description, allergy, allergy_description, contact_person, id_volunteer))


    def update_volunteer_data(self, id_volunteer, driver, id_card, email, phone, birthdate, position, exp4x4, assembly, medication, medication_description, allergy, allergy_description, contact_person):
        """"""

        query = "UPDATE volunteer SET driver=?, id_card=?, email=?, phone=?, birthdate=?, position=?, exp4x4=?, assembly=?, medication=?, medication_description=?, allergy=?, allergy_description=?, contact_person=? WHERE id_volunteer=?"
        self.db.execute_query(query, (driver, id_card, email, phone, birthdate, position, exp4x4, assembly, medication, medication_description, allergy, allergy_description, contact_person, id_volunteer))


    def update_volunteer_text_data(self, id_volunteer, id_card, email, phone, birthdate, medication_description, allergy_description, contact_person):
        """borrar despues de las pruebas TODO"""

        query = "UPDATE volunteer SET id_card=?, email=?, phone=?, birthdate=?, medication_description=?, allergy_description=?, contact_person=? WHERE id_volunteer=?"
        self.db.execute_query(query, (id_card, email, phone, birthdate, medication_description, allergy_description, contact_person, id_volunteer))


    def update_volunteer_combobox_data(self, id_volunteer, position, assembly):
        """"""
        query = "UPDATE volunteer SET position=?, assembly=? WHERE id_volunteer=?"
        self.db.execute_query(query, (position, assembly, id_volunteer))


    def update_volunteer_radiobtn_data(self, id_volunteer, driver, exp4x4, medication, allergy):
        """"""
        query = "UPDATE volunteer SET driver=?, exp4x4=?, medication=?, allergy=? WHERE id_volunteer=?"
        self.db.execute_query(query, (driver, exp4x4, medication, allergy, id_volunteer))


    def delete_volunteer(self, id_volunteer):
        """Delete a volunteer after confirm exists."""
        existing_volunteer = self.db.fetch_query_one("SELECT id_volunteer FROM volunteer WHERE id_volunteer = ?", (id_volunteer,))
        if not existing_volunteer:
            raise ValueError("El voluntario no existe.")  # TODO: Mostrar en ventana de error
        

        query = "DELETE FROM volunteer WHERE id_volunteer = ?"
        self.db.execute_query(query, (id_volunteer,))


    def check_volunteers_in_date(self, date, confirmed):
        """Check how many volunteers are available on a given day"""
        query = '''SELECT v.id_volunteer ,v.name, v.lastname_1, v.lastname_2, v.driver, a.date_init, a.date_end, a.comments
                FROM volunteer v
                JOIN availability a ON v.id_volunteer = a.id_volunteer
                WHERE ? BETWEEN a.date_init AND a.date_end
                AND a.confirmed = ?'''
        
        raw_data = self.db.fetch_query_all(query, (date, confirmed))

        # Convertimos la lista de tuplas en una lista de diccionarios
        return [{
            "id_volunteer": v[0],
            "name": v[1], 
            "lastname_1": v[2], 
            "lastname_2": v[3], 
            "driver": bool(v[4]),  
            "date_init": v[5],  
            "date_end": v[6],  
            "comments": v[7]  
        } for v in raw_data]
    

    
    # FOR TESTING:
    def insert_sample_data(self):
        """Insert sample data to test."""
        sample_volunteers = [
            ("Belentxu", "Lentxu", "Lentxu", 1, "123456789A", "belentxu@example.com", "123456987",
            "1986-12-30", 2, 1, 536, 1, "Antidepresivos", 1, "Plátanos", "Pablín"),
            
            ("Martica", "Súper", "Maja", 1, "123456789B", "matica@example.com", "623456937",
            "1990-07-22", 3, 1, 98, 0, "", 0, "", "Fernando El Bribón"),
            
            ("Fernando", "El", "Bribón", 1, "123456789C", "fernando@example.com", "629456987",
            "1978-02-05", 2, 1, 98, 0, "", 0, "", "Martica Súper Maja"),
        ]

        self.db.c.executemany(
            """INSERT INTO volunteer (
                name, lastname_1, lastname_2, driver, id_card, email, phone, birthdate, 
                position, exp4x4, assembly, medication, medication_description, 
                allergy, allergy_description, contact_person
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
            sample_volunteers
        )

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

        self.db.c.executemany(
            "INSERT INTO availability (id_volunteer, date_init, date_end, comments) VALUES (?, ?, ?, ?)", 
            sample_availability
        )
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

    
    # 🚨 Eliminar completamente la tabla y sus datos previos
    #vm.db.c.execute("DROP TABLE IF EXISTS volunteer")  # 🔥 Borra la tabla si existe
    #vm.db.c.execute("DROP TABLE IF EXISTS availability")  # 🔥 Borra la tabla availability también

    # 🛠️ Vuelve a crear la base de datos desde DatabaseConnector
    #db = DatabaseConnector()  # Esto recreará las tablas automáticamente

    # 📝 Insertar nuevos datos de prueba
    #vm = VolunteerManager(db)
    #vm.db.execute_query("DELETE FROM volunteer")
    #vm.db.execute_query("DELETE FROM availability")
    #vm.insert_sample_data()
    vm.update_volunteer("Martica", "Súper", "Maja", 1, "123456789B", "matica@example.com", "623456937",
            "1990-07-22", 3, 1, 99, 0, "", 0, "", "Fernando El Bribón", 2)
    vm.update_volunteer("Fernando", "El", "Bribón", 1, "123456789C", "fernando@example.com", "629456987",
            "1978-02-05", 2, 1, 99, 0, "", 0, "", "Martica Súper Maja", 3)
    
    # Cerrar conexión con la BD
    vm.db.close_connection()