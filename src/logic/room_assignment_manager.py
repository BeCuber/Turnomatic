from datetime import date

from src.data.db_connector import DatabaseConnector


class RoomManager:
    def __init__(self, db: DatabaseConnector):
        """"""
        self.db = db


    def get_volunteers_without_room(self, day: date):
        query = """
        SELECT
            a.id_availability,
            v.id_volunteer,
            v.name
        FROM availability a
        JOIN volunteer v ON v.id_volunteer = a.id_volunteer
        LEFT JOIN room_assignment ra
            ON ra.id_availability = a.id_availability
            AND DATE (ra.check_in) <= DATE(?)
            AND DATE (ra.check_out) >= DATE(?)
        WHERE
            DATE(a.date_init) <= DATE(?)
            AND DATE(a.date_end) >= DATE(?)
            AND a.confirmed = 1
            AND ra.id_assignment IS NULL;        
        """
        params = (day, day, day, day)
        return self.db.fetch_query_all(query, params)