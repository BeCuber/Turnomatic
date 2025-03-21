from src.data.db_connector import DatabaseConnector


class AvailabilityManager():
    def __init__(self):
        self.db = DatabaseConnector

    
    # CRUD FOR availability #








    # END CRUD FOR availability #


# from bash: $ python -m src.logic.availability_manager (-m points "src" a module)
if __name__ == "__main__":
    am = AvailabilityManager()

    am.db.close_connection()
