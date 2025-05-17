from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QTableWidget, QAbstractItemView

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
        calendar.setFocus()
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("lightgreen") if confirmed else QColor("yellow"))

        start = datetime.strptime(date_init, "%Y-%m-%d").date()
        end = datetime.strptime(date_end, "%Y-%m-%d").date()

        current = start
        while current <= end:
            qdate = QDate(current.year, current.month, current.day) # Creates QDate object
            calendar.setDateTextFormat(qdate, fmt) # setDateTextFormat expects QDate, not date
            current += timedelta(days=1)


    def on_calendar_availability_clicked(self, date: QDate, availability_table: QTableWidget):
        """"""
        for row in range(availability_table.rowCount()):
            date_init_item = availability_table.item(row, 1)
            date_end_item = availability_table.item(row, 2)

            date_init = QDate.fromString(date_init_item.text(), "yyyy-MM-dd")
            date_end = QDate.fromString(date_end_item.text(), "yyyy-MM-dd")

            if date_init <= date <= date_end:
                availability_table.selectRow(row)
                availability_table.scrollToItem(date_init_item)
                return

        availability_table.clearSelection()
