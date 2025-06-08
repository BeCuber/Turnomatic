from PyQt5.QtGui import QTextCharFormat, QColor, QPalette
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QTableWidget, QAbstractItemView, QTableView

from src.data.db_connector import DatabaseConnector
from src.logic.availability_manager import AvailabilityManager
from datetime import datetime, timedelta


class CalendarManager:
    def __init__(self, parent: QWidget, db: DatabaseConnector):
        self.parent = parent
        self.am = AvailabilityManager(db)

        self.theme = "light"

        # self.calendar_widget = None

        # self.main_window = self.parent.parent
        # self.main_window.theme_changed.connect(lambda: self.display_calendar(self.calendar_widget))


    def display_calendar(self, calendar: QCalendarWidget, theme:str):
        self.theme = theme
        self._apply_weekend_theme(calendar)

    # def display_calendar(self, calendar: QCalendarWidget):
    #     self._apply_weekend_theme(calendar)

    # def update_calendar_style(self, calendar: QCalendarWidget, theme:str):
    #     self._apply_weekend_theme(calendar, theme)

    def update_individual_calendar_style(self, calendar: QCalendarWidget, new_theme:str):
        self.theme = new_theme
        self._apply_weekend_theme(calendar)




    def update_heatmap_style(self, calendar: QCalendarWidget, new_theme:str):
        self.theme = new_theme
        self._apply_weekend_theme(calendar)
        self.set_heatmap(calendar)


    def clear_calendar(self, calendar: QCalendarWidget):
        """"""
        calendar.setDateTextFormat(QDate(), QTextCharFormat())


    def update_calendar_with_availability(self, calendar: QCalendarWidget, date_init: str, date_end: str, confirmed):
        """"""
        # self.theme
        calendar.setFocus()
        fmt = QTextCharFormat()

        if self.theme == "light":
            fmt.setBackground(QColor("#90EE90") if confirmed else QColor("#E6DAB8"))
        elif self.theme == "dark":
            fmt.setBackground(QColor("#4CB093") if confirmed else QColor("#B0964C"))
        else:
            # Por si acaso
            fmt.setBackground(QColor("#FFFFFF"))


        start = datetime.strptime(date_init, "%Y-%m-%d").date()
        end = datetime.strptime(date_end, "%Y-%m-%d").date()

        current = start
        while current <= end:
            qdate = QDate(current.year, current.month, current.day) # Creates QDate object
            calendar.setDateTextFormat(qdate, fmt) # setDateTextFormat expects QDate, not date
            current += timedelta(days=1)

        calendar.update()


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
            fmt.setBackground(QColor(self._get_color(count)))

            calendar.setDateTextFormat(current, fmt)
            current = current.addDays(1)

    def _get_color(self, count):
        """"""
        if self.theme == "light":
            # Lógica para el tema claro (la que ya tenías)
            if count == 0:
                return QColor("#FFFFFF")  # Blanco para 0 personas

            color_start_rgb = QColor("#FFFFFF").getRgb()[:3]  # Blanco
            color_end_rgb = QColor("#3FBF83").getRgb()[:3]  # El verde para 10 personas
            max_interpolation_val = 10

            if 1 <= count <= max_interpolation_val:
                t = count / max_interpolation_val
                r = int(color_start_rgb[0] + t * (color_end_rgb[0] - color_start_rgb[0]))
                g = int(color_start_rgb[1] + t * (color_end_rgb[1] - color_start_rgb[1]))
                b = int(color_start_rgb[2] + t * (color_end_rgb[2] - color_start_rgb[2]))
                return QColor(r, g, b)
            elif count > max_interpolation_val:
                base_color_rgb = QColor("#3FBF83").getRgb()[:3]
                color_dark_end_rgb = QColor("#1D8152").getRgb()[:3]  # Un verde más oscuro para >10
                max_darkening_val = 20  # Ajusta según tu volumen máximo esperado

                if count >= max_darkening_val:
                    return QColor(color_dark_end_rgb[0], color_dark_end_rgb[1], color_dark_end_rgb[2])
                else:
                    t_dark = (count - max_interpolation_val) / (max_darkening_val - max_interpolation_val)
                    r = int(base_color_rgb[0] + t_dark * (color_dark_end_rgb[0] - base_color_rgb[0]))
                    g = int(base_color_rgb[1] + t_dark * (color_dark_end_rgb[1] - base_color_rgb[1]))
                    b = int(base_color_rgb[2] + t_dark * (color_dark_end_rgb[2] - base_color_rgb[2]))
                    return QColor(r, g, b)
            else:
                return QColor("#FFFFFF")  # Fallback

        elif self.theme == "dark":

            color_start_rgb_dark = QColor("#2e2e2e").getRgb()[:3]  # Un verde muy oscuro

            color_end_rgb_dark = QColor("#3FBF83").getRgb()[:3]  #  o #90EE90

            max_interpolation_val = 10  # El mismo punto de anclaje

            if count == 0:
                return QColor(color_start_rgb_dark[0], color_start_rgb_dark[1], color_start_rgb_dark[2])

            if 1 <= count <= max_interpolation_val:
                t = count / max_interpolation_val
                r = int(color_start_rgb_dark[0] + t * (color_end_rgb_dark[0] - color_start_rgb_dark[0]))
                g = int(color_start_rgb_dark[1] + t * (color_end_rgb_dark[1] - color_start_rgb_dark[1]))
                b = int(color_start_rgb_dark[2] + t * (color_end_rgb_dark[2] - color_start_rgb_dark[2]))
                return QColor(r, g, b)
            elif count > max_interpolation_val:
                # Para valores mayores a 10,  seguir aclarando hasta un tope.
                # Color de base para > 10 es el de 10 personas (el color_end_rgb_dark)
                base_color_rgb_dark = QColor("#3FBF83").getRgb()[:3]
                # Color final para un valor muy alto (e.g., 20)
                color_very_light_end_rgb_dark = QColor("#CCFFCC").getRgb()[:3]  # Un verde pastel muy claro, casi blanco

                max_lightening_val = 20  # Ajusta volumen máximo esperado

                if count >= max_lightening_val:
                    return QColor(color_very_light_end_rgb_dark[0], color_very_light_end_rgb_dark[1],
                                  color_very_light_end_rgb_dark[2])
                else:
                    t_light = (count - max_interpolation_val) / (max_lightening_val - max_interpolation_val)
                    r = int(
                        base_color_rgb_dark[0] + t_light * (color_very_light_end_rgb_dark[0] - base_color_rgb_dark[0]))
                    g = int(
                        base_color_rgb_dark[1] + t_light * (color_very_light_end_rgb_dark[1] - base_color_rgb_dark[1]))
                    b = int(
                        base_color_rgb_dark[2] + t_light * (color_very_light_end_rgb_dark[2] - base_color_rgb_dark[2]))
                    return QColor(r, g, b)
            else:
                return QColor(color_start_rgb_dark[0], color_start_rgb_dark[1],
                              color_start_rgb_dark[2])  # Fallback para dark
        else:
            # Fallback si el tema no es reconocido
            return QColor("#FFFFFF")


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


    def _apply_weekend_theme(self, calendar: QCalendarWidget):
        """
            Apply custom text formats to the days in the QCalendarWidget,
            especially for weekends.
        """
        if not calendar:
            return

        weekend_format = QTextCharFormat()

        if self.theme == "dark":
            # weekend_color = QColor("#ff9900") # naranja para fines de semana
            # weekend_color = QColor("#A34CB0") # morado oscuro para fines de semana
            weekend_color = QColor("#AD72B3") # naranja para fines de semana
        else:
            weekend_color = QColor("#EB3945")

        weekend_format.setForeground(weekend_color)

        calendar.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        calendar.setWeekdayTextFormat(Qt.Sunday, weekend_format)

        calendar.update()
