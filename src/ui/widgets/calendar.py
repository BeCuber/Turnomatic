from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QCalendarWidget

from src.data.db_connector import DatabaseConnector
from src.logic.availability_manager import AvailabilityManager
from datetime import datetime, timedelta


class CalendarManager:
    def __init__(self, parent: QWidget, db: DatabaseConnector):
        self.parent = parent
        self.am = AvailabilityManager(db)


    def clear_calendar(self, calendar: QCalendarWidget):
        """"""
        calendar.setDateTextFormat(QDate(), QTextCharFormat())

    def update_calendar_with_availability(self, calendar: QCalendarWidget, date_init: str, date_end: str, confirmed):
        """"""
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("lightgreen") if confirmed else QColor("yellow"))

        start = datetime.strptime(date_init, "%Y-%m-%d").date()
        end = datetime.strptime(date_end, "%Y-%m-%d").date()

        current = start
        while current <= end:
            qdate = QDate(current.year, current.month, current.day) # Creates QDate object
            calendar.setDateTextFormat(qdate, fmt) # setDateTextFormat expects QDate, not date
            current += timedelta(days=1)
