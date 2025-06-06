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
        print(f"CalendarManager update_calendar_with_availability attr:{self.theme}")
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
            # Lógica para el tema oscuro: de oscuro a claro
            # Color base oscuro para 0 personas (un verde muy oscuro o casi negro verdoso)
            # Asegúrate de que este color sea distinto del fondo general del calendario si es posible,
            # o que el QSS del calendario maneje su propio fondo oscuro.

            # Puedes usar el color de fondo general de tu app en modo oscuro para los días sin volumen,
            # o un color ligeramente más oscuro para un pequeño "pozo" visual.
            # Vamos a usar un verde muy oscuro como punto de partida.

            # color_start_rgb_dark = QColor("#224433").getRgb()[:3]  # Un verde muy oscuro, casi negro
            color_start_rgb_dark = QColor("#2e2e2e").getRgb()[:3]  # Un verde muy oscuro, casi negro

            # El color final claro para 10 personas (un verde más brillante)
            # Podríamos usar el mismo #3FBF83 que es tu "verde brillante" si quieres
            # o un tono similar pero que contraste bien con el texto blanco.

            # color_end_rgb_dark = QColor("#76FF7A").getRgb()[:3]  # Un verde muy claro (similar a un neón suave) o #90EE90 si quieres usar el mismo que antes
            color_end_rgb_dark = QColor("#3FBF83").getRgb()[:3]  # Un verde muy claro (similar a un neón suave) o #90EE90 si quieres usar el mismo que antes

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
                # Para valores mayores a 10, podemos seguir aclarando hasta un tope.
                # Podrías ir hacia un blanco verdoso si quieres un impacto mayor.

                # Color de base para > 10 es el de 10 personas (el color_end_rgb_dark)
                # base_color_rgb_dark = QColor("#76FF7A").getRgb()[:3]  # O el que hayas usado para count=10
                base_color_rgb_dark = QColor("#3FBF83").getRgb()[:3]  # O el que hayas usado para count=10

                # Color final para un valor muy alto (e.g., 20)
                color_very_light_end_rgb_dark = QColor("#CCFFCC").getRgb()[:3]  # Un verde pastel muy claro, casi blanco

                max_lightening_val = 20  # Ajusta según tu volumen máximo esperado

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

        # if count == 0:
        #     return QColor("#FFFFFF")  # Blanco para 0 personas
        #
        # # Definir los colores clave en formato RGB
        # color_start_rgb = QColor("#FFFFFF").getRgb()[:3]  # Blanco (R, G, B)
        # color_end_rgb = QColor("#3FBF83").getRgb()[:3]  # El color para 10 personas (R, G, B)
        #
        # # El punto de anclaje para el color #3FBF83 es 10 personas
        # max_interpolation_val = 10
        #
        # if 1 <= count <= max_interpolation_val:
        #     # Calcular el factor de interpolación
        #     # Si count es 1, factor es 0.1 (1/10)
        #     # Si count es 10, factor es 1.0 (10/10)
        #     t = count / max_interpolation_val
        #
        #     # Interpolar linealmente cada componente de color (R, G, B)
        #     # new_component = start_component + t * (end_component - start_component)
        #     r = int(color_start_rgb[0] + t * (color_end_rgb[0] - color_start_rgb[0]))
        #     g = int(color_start_rgb[1] + t * (color_end_rgb[1] - color_start_rgb[1]))
        #     b = int(color_start_rgb[2] + t * (color_end_rgb[2] - color_start_rgb[2]))
        #
        #     return QColor(r, g, b)
        # elif count > max_interpolation_val:
        #     # Para valores mayores a 10, podemos seguir oscureciendo el color
        #     # Podemos definir un color final más oscuro para un valor máximo que esperes,
        #     # o simplemente ir oscureciendo progresivamente a partir del color de 10.
        #     # En este ejemplo, vamos a oscurecer gradualmente desde el color de 10.
        #
        #     # Color de base para > 10 es el de 10 personas
        #     base_color_rgb = QColor("#3FBF83").getRgb()[:3]
        #
        #     # Definir un color final oscuro para un valor arbitrario alto, por ejemplo, 20 o 30
        #     # Esto es para que el degradado no se extienda infinitamente con el mismo "ritmo"
        #     # y tenga un tope de oscurecimiento.
        #     # Aquí, definimos un color más oscuro como el "#1D8152" que tenías, o algo similar.
        #     color_dark_end_rgb = QColor("#1D8152").getRgb()[:3]  # Un verde más oscuro
        #
        #     # Puedes ajustar este 'max_darkening_val' según el volumen máximo que esperes
        #     # o cómo quieras que se extienda el degradado más allá de 10.
        #     # Por ejemplo, si esperas un máximo de 20 personas, podrías poner 20 aquí.
        #     max_darkening_val = 20  # Ajusta este valor si esperas un volumen máximo diferente
        #
        #     # Calculamos 't' en base a la diferencia entre 'count' y 'max_interpolation_val'
        #     # y el rango de oscurecimiento.
        #     if count >= max_darkening_val:
        #         # Si se supera el valor máximo de oscurecimiento, se mantiene el color más oscuro
        #         return QColor(color_dark_end_rgb[0], color_dark_end_rgb[1], color_dark_end_rgb[2])
        #     else:
        #         # Interpolación entre el color de 10 y el color_dark_end_rgb
        #         t_dark = (count - max_interpolation_val) / (max_darkening_val - max_interpolation_val)
        #         r = int(base_color_rgb[0] + t_dark * (color_dark_end_rgb[0] - base_color_rgb[0]))
        #         g = int(base_color_rgb[1] + t_dark * (color_dark_end_rgb[1] - base_color_rgb[1]))
        #         b = int(base_color_rgb[2] + t_dark * (color_dark_end_rgb[2] - base_color_rgb[2]))
        #         return QColor(r, g, b)
        # else:
        #     # Por si acaso, para cualquier otro caso (aunque 'count' debería ser >= 0)
        #     return QColor("#FFFFFF")

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


        print(f"CalendarManager theme attr:{self.theme}")

        calendar.update()
