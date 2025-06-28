from collections import defaultdict
from datetime import date, timedelta, datetime

from src.data.db_connector import DatabaseConnector


class RoomManager:
    def __init__(self, db: DatabaseConnector):
        """"""
        self.db = db


    def get_all_rooms(self):
        """Returns a dict: {id_room: room_name, capacity}"""
        query = "SELECT * FROM rooms ORDER BY id_room ASC;"
        result = self.db.fetch_query_all(query)
        return {row[0]: (row[1], row[2]) for row in result}


    def get_enabled_rooms_for_day(self, day: date):
        """{id_room: room_name, capacity}"""
        query = """
            SELECT r.id_room, r.room_name, r.capacity
            FROM rooms r
            JOIN room_schedule rs ON r.id_room = rs.id_room
            WHERE DATE(rs.check_in) <= DATE(?)
            AND DATE(rs.check_out) >= DATE(?)
            ORDER BY r.id_room
            """

        params = (day.isoformat(), day.isoformat())
        rows = self.db.fetch_query_all(query, params)

        return {row[0]: (row[1], row[2]) for row in rows}


    def update_room_name(self, id_room: int, new_name:str):
        """"""
        query = "UPDATE rooms SET room_name = ? WHERE id_room = ?;"
        params = (new_name, id_room)
        self.db.execute_query(query, params)


    def update_room_capacity(self, id_room: int, new_capacity: int):
        """"""
        query = "UPDATE rooms SET capacity = ? WHERE id_room = ?"
        params = (new_capacity, id_room)
        self.db.execute_query(query, params)


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


    def get_volunteers_rooms_for_day(self, day: date):
        """"""
        query = """
                SELECT ra.id_room, v.id_volunteer, v.name, ra.id_assignment
                FROM room_assignment ra
                JOIN availability a ON ra.id_availability = a.id_availability
                JOIN volunteer v ON a.id_volunteer = v.id_volunteer
                WHERE DATE(?) BETWEEN DATE(ra.check_in) AND DATE(ra.check_out)
                ORDER BY ra.id_room;
            """
        rows = self.db.fetch_query_all(query, (day.isoformat(),))

        result = {}
        for id_room, id_volunteer, volunteer_name, id_assignment in rows:
            if id_room not in result:
                result[id_room] = []
            result[id_room].append((id_volunteer, volunteer_name, id_assignment))

        return result


    def get_all_data_for_week(self, start_date: date, days: int = 8):
        """"""
        query = """
                SELECT 
                    r.id_room,
                    r.room_name,
                    r.capacity,
                    v.id_volunteer,
                    v.name,
                    ra.id_assignment,
                    a.id_availability
                FROM room_schedule rs
                JOIN rooms r ON r.id_room = rs.id_room
                LEFT JOIN room_assignment ra 
                    ON r.id_room = ra.id_room 
                    AND DATE(?) BETWEEN DATE(ra.check_in) AND DATE(ra.check_out)
                LEFT JOIN availability a 
                    ON ra.id_availability = a.id_availability
                LEFT JOIN volunteer v 
                    ON a.id_volunteer = v.id_volunteer
                WHERE DATE(?) BETWEEN DATE(rs.check_in) AND DATE(rs.check_out)
            """
        result = {}
        for i in range(days):
            day = start_date + timedelta(days=i)
            rows = self.db.fetch_query_all(query, (day.isoformat(), day.isoformat()))

            room_data = {}
            for id_room, room_name, capacity, id_volunteer, name, id_assignment, id_availability in rows:
                if id_room not in room_data: # this attrib are needed just once in the dict
                    room_data[id_room] = {
                        "room_name": room_name,
                        "capacity": capacity,
                        "volunteers": []
                    }

                if id_volunteer is not None: # None is not needed : (2, "02", 1, None, None, None, None)
                    room_data[id_room]["volunteers"].append(
                        (id_volunteer, name, id_assignment, id_availability)
                    )

            result[day] = dict(room_data)

        return result


    def get_dates_from_availability(self, id_availability: int):
        """"""
        query="SELECT date_init, date_end FROM availability WHERE id_availability=?;"
        params = (id_availability,)
        return self.db.fetch_query_one(query, params)


    def create_room_assignment(self, id_room, id_availability, check_in, check_out):
        """"""
        query = """INSERT INTO room_assignment (id_room, id_availability, check_in, check_out) VALUES (?,?,?,?)"""
        self.db.execute_query(query,(id_room, id_availability, check_in, check_out))




if __name__ == "__main__":
    db = DatabaseConnector()
    rm = RoomManager(db)

    # print(f"get_all_rooms: {rm.get_all_rooms()}")
    today = date.today()
    # print(f"get_enabled_rooms_for_day: {rm.get_enabled_rooms_for_day(today)}")

    days_since_sunday = (today.weekday() + 1) % 7
    previous_sunday = today - timedelta(days=days_since_sunday)

    dicty = rm.get_all_data_for_week(previous_sunday)

    # print(f"get_all_data_for_week: {dicty}")
    # for i in range(0, 10):
    # print(f"key = today : {dicty[today]}")
    dia = date(2025, 6, 28)
    print(f"dicty: {dicty}")
    # rooms_dict_for_day = dicty[today]
    print(f"key = day dicty[dia] : {dicty[today]}") #TODO necesito esta para room_card
    # print(rooms_dict_for_day)
    # print(f"rooms_dict_for_day = {rooms_dict_for_day}")
    # print(f"dicty[dia].values() : {dicty[dia].values()}") # solo vale para dicts
    print(f"dicty[dia][1] : {dicty[dia][1]}") # solo vale para dicts #TODO necesito esta para individual
    # print(f"dicty[dia][1] : {rooms_dict_for_day[1]}")
    # volunteers = rooms_dict_for_day[1]["volunteers"]
    # print(volunteers)

    # print(f"room name 1 for day: {dicty[dia][1]["room_name"]}, capacity: {dicty[dia][1]["capacity"]}, volunteers: {dicty[dia][1]["volunteers"]}")
    # print(f"El día {dia} hay disponibles {len(dicty[dia])} habitaciones.")
    # print(f"room name 2 for day: {dicty[dia][2]["room_name"]}, capacity: {dicty[dia][2]["capacity"]}, volunteers: {dicty[dia][1]["volunteers"]}")
    # total_voluntarios = sum(len(info["volunteers"]) for info in dicty[dia].values())
    # print(f"Total de voluntarios el {dia}: {total_voluntarios}")

    # print(f"keys = today / id_room = 1: {dicty[today][1]}")
    # print(f"lenght (8 days): {len(dicty)}")
    # print(f"claves de dict: {dicty.keys()}")
    # print(f"valores de dict: {dicty.values()}")
    # print(f"items de dict: {dicty.items()}")

    #
    # for i in rooms_dict_for_day:
    #     print(rooms_dict_for_day[i])
    # for i in rooms_dict_for_day:
    # print(f"{rooms_dict_for_day.keys()}")
    # list = rooms_dict_for_day.keys()
    # print(list)
    # print(list[0])
    day = date(2025, 6, 22)
    discty = rm.get_volunteers_without_room(day)
    print(discty)

    rm.db.close_connection()
