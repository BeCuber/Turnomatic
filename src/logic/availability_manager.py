# from PyQt5.QtCore.QUrl import query

from src.data.db_connector import DatabaseConnector
from datetime import datetime, timedelta # para merge


class AvailabilityManager:
    def __init__(self, db: DatabaseConnector):
        self.db = db


    def validate_availability(self, id_volunteer, date_init, date_end, exclude_this_id=None):
        """Validate dates"""

        if not date_init or not date_end:
            raise ValueError("Las fechas de inicio y fin son obligatorias.")

        if date_end < date_init:
            raise ValueError("La fecha de finalización no puede ser anterior a la de inicio.")

        overlapped = self.db.fetch_query_all("""
            SELECT * FROM availability 
            WHERE id_volunteer = ?
            AND date_end >= ?
            AND date_init <= ?
            AND (id_availability != ? OR ? IS NULL)
        """, (id_volunteer, date_init, date_end, exclude_this_id, exclude_this_id))

        if overlapped:
            raise ValueError("Ya existe una disponibilidad que solapa con las fechas seleccionadas.")


    def create_availability(self, id_volunteer, date_init, date_end, comments, confirmed):
        """Validate data and then create a new availability."""

        existing_volunteer = self.db.fetch_query_one(
            "SELECT id_volunteer FROM volunteer WHERE id_volunteer = ?", 
            (id_volunteer,)
        )
        if not existing_volunteer:
            raise ValueError("El voluntario no existe.")

        self.validate_availability(id_volunteer, date_init, date_end)

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


    def get_id_volunteer_from_id_availability(self, id_availability):
        """"""
        query = "SELECT id_volunteer FROM availability WHERE id_availability = ?"
        return self.db.fetch_query_one(query, (id_availability,))[0]
    

    def get_availability_by_id(self, id_availability):
        """"""
        query="SELECT * from availability WHERE id_availability = ?"
        return self.db.fetch_query_one(query, (id_availability,))


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
        return bool(result[0]) if result else False


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


    def merge_periods(self, id_volunteer, confirmed, changed_id_availability):
        """
        Try to merge the changed period with its contiguous periods
        """
        # periods son todos los periodos de un id_volunteer y un mismo confirmed
        periods = self.get_confirmed_availability_by_id_volunteer(id_volunteer, confirmed)
        if not periods or len(periods) < 2: # Si no hay dos, no hay nada que juntar
            return  # Nothing to merge

        # Get current availability and its index
        index, current_period = self._get_current_availability(periods, changed_id_availability)
        id_current, start_current, end_current, comment_current = current_period
        start_current_date = datetime.strptime(start_current, "%Y-%m-%d").date()
        end_current_date = datetime.strptime(end_current, "%Y-%m-%d").date()

        # intentar fusionar con el anterior
        if index > 0:  # Si es el primero, no tiene anterior
            previous = periods[index - 1]
            id_previous, start_previous, end_previous, comment_previous = previous
            start_previous_date = datetime.strptime(start_previous, "%Y-%m-%d").date()
            end_previous_date = datetime.strptime(end_previous, "%Y-%m-%d").date()

            # si fecha fin anterior + 1 dia = fecha inicio current
            if end_previous_date + timedelta(days=1) == start_current_date:
                new_start = start_previous  # no hace falta usar date porque se guarda en bd con valor string
                new_end = end_current
                new_comment = self._merge_comments(previous, current_period)
                # delete old id,s. Delete must happen before create to not create an availability with same date
                self.delete_availability(id_previous)
                self.delete_availability(id_current)
                # create new one
                self.create_availability(id_volunteer, new_start, new_end, new_comment, confirmed) # Create new register
                changed_id_availability = self.db.get_last_inserted_id()


        # periods may have changed so the index, we call them again:
        periods = self.get_confirmed_availability_by_id_volunteer(id_volunteer, confirmed)
        if not periods or len(periods) < 2: # Si no hay dos, no hay nada que juntar
            return  # Nothing to merge

        index, current_period = self._get_current_availability(periods, changed_id_availability)
        id_current, start_current, end_current, comment_current = current_period
        start_current_date = datetime.strptime(start_current, "%Y-%m-%d").date()
        end_current_date = datetime.strptime(end_current, "%Y-%m-%d").date()

        # intenta fusionar con el siguiente
        if index < len(periods) - 1: # si es el último, no tiene un siguiente
            nxt_period = periods[index + 1]
            id_nxt, start_nxt, end_nxt, comment_nxt = nxt_period
            start_nxt_date = datetime.strptime(start_nxt, "%Y-%m-%d").date()
            end_nxt_date = datetime.strptime(end_nxt, "%Y-%m-%d").date()

            # si fecha fin current + 1 = start_nxt
            if end_current_date + timedelta(days=1) == start_nxt_date:
                new_start = start_current
                new_end = end_nxt
                new_comment = self._merge_comments(current_period, nxt_period)

                self.delete_availability(id_current)
                self.delete_availability(id_nxt)

                self.create_availability(id_volunteer, new_start, new_end, new_comment, confirmed)

                changed_id_availability = self.db.get_last_inserted_id()

    def _merge_comments(self, period1, period2):  # period1 period2 to compare instead only comments
        if not period1[3] and not period2[3]:
            return ""
        elif period1[3] == period2[3]:
            return period1[3]
        elif not period1[3] and period2[3]:
            return period2[3]
        elif period1[3] and not period2[3]:
            return period1[3]
        else:
            return f"({period1[1]} - {period1[2]}): {period1[3]} || ({period2[1]} - {period2[2]}): {period2[3]}"

    def _get_current_availability(self, periods, changed_id_availability):
        """Creates an index and returns where is the changed availability"""
        for i in range(len(periods)):
            id_availability = periods[i][0] # The first value of the tuple is id_availability
            if id_availability == changed_id_availability:
                return i, periods[i]
        return None


    def get_date_min(self):
        """"""
        query = "SELECT MIN(date_init) FROM availability"
        result = self.db.fetch_query_one(query)
        return result[0] # 2025-04-22 <= format str


    def get_date_max(self):
        """"""
        query = "SELECT MAX(date_end) FROM availability"
        result = self.db.fetch_query_one(query)
        return result[0] # 2025-09-03 <= format str


    def get_all_confirmed_availabilities(self):
        """"""
        raw_data = self.db.fetch_query_all("SELECT * FROM availability WHERE confirmed = 1")
        return [{
            "id": v[0],
            "id_volunteer": v[1],
            "date_init": v[2],
            "date_end": v[3],
            "comments": v[4],
            "confirmed": bool(v[5])
            } for v in raw_data]




# from bash: $ python -m src.logic.availability_manager (-m points "src" a module)
if __name__ == "__main__":
    db = DatabaseConnector()
    am = AvailabilityManager(db)

    # am.create_availability(1, "2025-05-14", "2025-05-14", "test", 0)

    # print(db.get_last_inserted_id())

    # print(am.get_availability_by_id_volunteer(1))
    # print(am.get_availability_by_id(60))

    print(am.get_date_min())
    print(am.get_date_max())
    print(am.read_all_availabilities())


    am.db.close_connection()
