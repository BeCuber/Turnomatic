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
        fmt.setBackground(QColor("lightgreen") if confirmed else QColor("#E5E4B8"))

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
            # fmt.setBackground(QColor(self._get_color_for_count(count)))
            fmt.setBackground(QColor(self._get_color(count)))

            calendar.setDateTextFormat(current, fmt)
            current = current.addDays(1)


    def _get_color(self, count):
        if count == 0:
            return QColor("#FFFFFF")  # Blanco para 0 personas

        # Definir los colores clave en formato RGB
        color_start_rgb = QColor("#FFFFFF").getRgb()[:3]  # Blanco (R, G, B)
        color_end_rgb = QColor("#3FBF83").getRgb()[:3]  # El color para 10 personas (R, G, B)

        # El punto de anclaje para el color #3FBF83 es 10 personas
        max_interpolation_val = 10

        if 1 <= count <= max_interpolation_val:
            # Calcular el factor de interpolación
            # Si count es 1, factor es 0.1 (1/10)
            # Si count es 10, factor es 1.0 (10/10)
            t = count / max_interpolation_val

            # Interpolar linealmente cada componente de color (R, G, B)
            # new_component = start_component + t * (end_component - start_component)
            r = int(color_start_rgb[0] + t * (color_end_rgb[0] - color_start_rgb[0]))
            g = int(color_start_rgb[1] + t * (color_end_rgb[1] - color_start_rgb[1]))
            b = int(color_start_rgb[2] + t * (color_end_rgb[2] - color_start_rgb[2]))

            return QColor(r, g, b)
        elif count > max_interpolation_val:
            # Para valores mayores a 10, podemos seguir oscureciendo el color
            # Podemos definir un color final más oscuro para un valor máximo que esperes,
            # o simplemente ir oscureciendo progresivamente a partir del color de 10.
            # En este ejemplo, vamos a oscurecer gradualmente desde el color de 10.

            # Color de base para > 10 es el de 10 personas
            base_color_rgb = QColor("#3FBF83").getRgb()[:3]

            # Definir un color final oscuro para un valor arbitrario alto, por ejemplo, 20 o 30
            # Esto es para que el degradado no se extienda infinitamente con el mismo "ritmo"
            # y tenga un tope de oscurecimiento.
            # Aquí, definimos un color más oscuro como el "#1D8152" que tenías, o algo similar.
            color_dark_end_rgb = QColor("#1D8152").getRgb()[:3]  # Un verde más oscuro

            # Puedes ajustar este 'max_darkening_val' según el volumen máximo que esperes
            # o cómo quieras que se extienda el degradado más allá de 10.
            # Por ejemplo, si esperas un máximo de 20 personas, podrías poner 20 aquí.
            max_darkening_val = 20  # Ajusta este valor si esperas un volumen máximo diferente

            # Calculamos 't' en base a la diferencia entre 'count' y 'max_interpolation_val'
            # y el rango de oscurecimiento.
            if count >= max_darkening_val:
                # Si se supera el valor máximo de oscurecimiento, se mantiene el color más oscuro
                return QColor(color_dark_end_rgb[0], color_dark_end_rgb[1], color_dark_end_rgb[2])
            else:
                # Interpolación entre el color de 10 y el color_dark_end_rgb
                t_dark = (count - max_interpolation_val) / (max_darkening_val - max_interpolation_val)
                r = int(base_color_rgb[0] + t_dark * (color_dark_end_rgb[0] - base_color_rgb[0]))
                g = int(base_color_rgb[1] + t_dark * (color_dark_end_rgb[1] - base_color_rgb[1]))
                b = int(base_color_rgb[2] + t_dark * (color_dark_end_rgb[2] - base_color_rgb[2]))
                return QColor(r, g, b)
        else:
            # Por si acaso, para cualquier otro caso (aunque 'count' debería ser >= 0)
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