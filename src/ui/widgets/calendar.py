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


    def set_heatmap(self, calendar: QCalendarWidget):
        """Set background on calendar counting volunteers each day"""

        # Get min and max dates
        date_min = QDate.fromString(self.am.get_date_min(), "yyyy-MM-dd")
        date_max = QDate.fromString(self.am.get_date_max(), "yyyy-MM-dd")

        # Get all availabilities
        # availabilites = self.am.read_all_availabilities()
        availabilites = self.am.get_all_confirmed_availabilities()

        #Count volunteer per day
        counts = self._count_volunteer_per_day(availabilites)

        # Clean previous colors on calendar
        calendar.setDateTextFormat(QDate(), QTextCharFormat()) # Reset

        # Look over days on rank
        current = date_min
        while current <= date_max:
            date_str = current.toString("yyyy-MM-dd")
            count = counts.get(date_str, 0)

            fmt = QTextCharFormat()
            fmt.setBackground(QColor(self._get_color_for_count(count)))

            calendar.setDateTextFormat(current, fmt)
            current = current.addDays(1)


    def _get_color_for_count(self, count):
        if count == 0:
            return QColor("#FFFFFF")
        elif 1<= count <= 3:
            return QColor("#E2FFF1")
        elif 4<= count <= 6:
            return QColor("#C2F8DE")
        elif 7<= count <= 8:
            return QColor("#8DF3C3")
        elif 9<= count <= 10:
            return QColor("#3FBF83")
        else:
            return QColor("#1D8152")

    def _count_volunteer_per_day(self, availabilities):
        """La función espera read_all_availabilities()"""
        counts = {} # dict

        for row in availabilities:
            start = QDate.fromString(row["date_init"], "yyyy-MM-dd")
            end = QDate.fromString(row["date_end"], "yyyy-MM-dd")
            current = start

            while current <= end:
                date_str = current.toString("yyyy-MM-dd")

                # Si la fecha no existe aún en el dict, se inicializa en 0
                if date_str not in counts:
                    counts[date_str] = 0

                # Se suma 1 en el valor de ese dia
                counts[date_str] += 1

                current = current.addDays(1)

        return counts