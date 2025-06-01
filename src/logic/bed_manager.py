from src.data.db_connector import DatabaseConnector
from datetime import datetime, timedelta # para merge

from src.logic.availability_manager import AvailabilityManager
from src.logic.volunteer_manager import VolunteerManager


class BedManager:
    def __init__(self, db: DatabaseConnector):
        """"""
        self.db = db


    def count_beds_assinged_per_day(self, date):
        """"""
        query = "SELECT COUNT (*) FROM bed_assignment WHERE date = ?"
        return self.db.fetch_query_one(query, (date,))[0]


    def count_confirmed_volunteers_per_day(self, date):
        """"""
        query = '''SELECT COUNT (*) 
                FROM availability 
                WHERE confirmed=1 and ? BETWEEN date_init AND date_end'''
        return self.db.fetch_query_one(query, (date,))[0]


    def assing_bed(self, id_availability: int):
        """"""
        # Get availability
        availability = self.db.fetch_query_one(
            "SELECT id_volunteer, date_init, date_end, confirmed FROM availability WHERE id_availability = ?",
            (id_availability,)
        )

        if not availability:
            raise ValueError("La disponibilidad no existe.")

        id_volunteer, date_init, date_end, confirmed = availability

        if not confirmed:
            return # Do nothing if it is not confirmed

        start_date = datetime.strptime(date_init, "%Y-%m-%d").date()
        end_date = datetime.strptime(date_end, "%Y-%m-%d").date()

        # Insert a row per day
        for i in range((end_date - start_date).days):
            day = start_date + timedelta(days=i)

            # Check if there is available bed
            count_bed = self.count_beds_assinged_per_day(day.strftime("%Y-%m-%d"))
            if count_bed >= 10:
                raise ValueError(f"No hay camas disponibles el día {day}.")

            self.db.execute_query(
                "INSERT INTO bed_assignment (id_availability, id_volunteer, date) VALUES (?, ?, ?)",
                (id_availability, id_volunteer, day.strftime("%Y-%m-%d"))
            )


    def remove_bed_assignment(self, id_availability: int):
        """"""
        self.db.execute_query(
            "DELETE FROM bed_assignment WHERE id_availability = ?",
            (id_availability,)
        )


    def update_bed_assignment(self, id_availability: int):
        """"""
        self.remove_bed_assignment(id_availability)
        self.assing_bed(id_availability)



    # def toggle_bed_assignment(self, id_availability: int, date: str):
    #     """"""
    #     existing = self.db.fetch_query_one(
    #         "SELECT id_bed FROM bed_assignment WHERE id_availability = ? AND date = ?",
    #         (id_availability, date)
    #     )
    #     if existing:
    #         self.remove_bed_assignment(id_availability, date)
    #     else:
    #         self.assing_bed(id_availability, date)

    # ONLY FOR DEVELPMENT
    def populate_initial_bed_assignments(self):
        """
        Carga inicial de la tabla bed_assignment con los datos confirmados de availability.
        """
        cursor = self.db.conn.cursor()
        try:
            # Buscar todas las disponibilidades confirmadas
            cursor.execute('''
                SELECT id_availability, id_volunteer, date_init, date_end
                FROM availability
                WHERE confirmed = 1
            ''')
            rows = cursor.fetchall()

            for id_availability, id_volunteer, date_init_str, date_end_str in rows:
                date_init = datetime.strptime(date_init_str, "%Y-%m-%d").date()
                date_end = datetime.strptime(date_end_str, "%Y-%m-%d").date()

                for n in range((date_end - date_init).days):
                    day = date_init + timedelta(days=n)
                    day_str = day.strftime("%Y-%m-%d")

                    # Comprobar si ya hay menos de 10 camas ocupadas ese día
                    cursor.execute('''
                        SELECT COUNT(*) FROM bed_assignment WHERE date = ?
                    ''', (day_str,))
                    (count,) = cursor.fetchone()

                    if count >= 10:
                        print(f"⚠️ Día {day_str}: 10 camas ya ocupadas. Saltando.")
                        continue

                    # Insertar asignación si hay cupo
                    cursor.execute('''
                        INSERT INTO bed_assignment (id_availability, id_volunteer, date)
                        VALUES (?, ?, ?)
                    ''', (id_availability, id_volunteer, day_str))

            self.db.conn.commit()
            print("✅ Asignaciones de cama iniciales completadas.")
        finally:
            cursor.close()


if __name__ == "__main__":
    pass
