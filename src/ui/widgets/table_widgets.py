from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QCalendarWidget, QWidget, QAbstractItemView, QLabel, \
    QMessageBox
from src.data.db_connector import DatabaseConnector
from src.logic.volunteer_manager import VolunteerManager
from src.logic.availability_manager import AvailabilityManager
from src.ui.widgets.delegates import AvailabilityDelegate
from src.ui.widgets.calendar import CalendarManager


class TableWidgetManager:

    def __init__(self, parent: QWidget, db: DatabaseConnector, calendar_manager: CalendarManager):
        """Initialize tables manager."""

        self.parent = parent
        self.vm = VolunteerManager(db)
        self.am = AvailabilityManager(db)
        self.calendar_manager = calendar_manager

    def add_empty_row(self, table:QTableWidget):
        """Add an empty row to create new registers"""
        row_idx = table.rowCount()
        table.insertRow(row_idx)
        

    # TABLES FOR volunteer_page #

    def define_all_volunteers_table(self, volunteer_table: QTableWidget):

        self.volunteer_table = volunteer_table

        # Add a hidden column at beginning for ID
        volunteer_table.insertColumn(0)
        volunteer_table.setColumnHidden(0, True)

        # Load volunteer list
        volunteer_table.blockSignals(True) # Avoid errors by triggering cellChanged
        self.load_all_volunteers(volunteer_table)
        volunteer_table.blockSignals(False) # Let edit the table

        volunteer_table.cellChanged.connect(self.update_volunteer_name)


    def load_all_volunteers(self, volunteer_table: QTableWidget):
        
        volunteers = self.vm.read_all_volunteers()

        volunteer_table.setRowCount(0)

        for row_idx, v in enumerate(volunteers):
            volunteer_table.insertRow(row_idx)
            volunteer_table.setItem(row_idx, 0, QTableWidgetItem(str(v["id_volunteer"])))
            volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["name"]))
            volunteer_table.setItem(row_idx, 2, QTableWidgetItem(v["lastname_1"]))  
            volunteer_table.setItem(row_idx, 3, QTableWidgetItem(v["lastname_2"]))


    def update_volunteer_name(self, row, col):
        """Update database when edit a cell."""

        volunteer_table = self.volunteer_table  # Saved on define_all_volunteers_table()

        # Get ID volunteer selected
        id_volunteer = volunteer_table.item(row, 0).text()

        new_value = volunteer_table.item(row, col).text()

        # Map columns with database names
        column_mapping = {
            1: "name",
            2: "lastname_1",
            3: "lastname_2"
        }

        if col in column_mapping:
            field_name = column_mapping[col]

            self.vm.update_volunteer_name(id_volunteer, field_name, new_value)

        volunteer_data = self.vm.get_volunteer_by_id(id_volunteer)
        self.label_volunteer = self.parent.findChild(QLabel, "labelNameVolunteer")
        self.label_volunteer.setText(f"{volunteer_data['name']} {volunteer_data['lastname_1']}")


    def define_availability_table(self, availability_table: QTableWidget, calendar: QCalendarWidget):
        """Configure availability table for edit and connect signals."""
        self.availability_table = availability_table  # Guardamos la tabla como atributo
        self._updating_table = False # control Flag
        # Asegura de que la primera columna (ID) está oculta
        availability_table.insertColumn(0)
        availability_table.setColumnHidden(0, True)

        availability_table.setItemDelegate(AvailabilityDelegate()) # delegate

        # Conectar para guardar cambios en la base de datos
        availability_table.cellChanged.connect(lambda row, col: self.update_availability(row, col, calendar))


    def display_individual_availability_data_table(self, id_volunteer, availability_table: QTableWidget, calendar: QCalendarWidget):
        """
            Populate the availability table with data for a given volunteer.

            Parameters:
                id_volunteer (int): The volunteer's ID.
                availability_table (QTableWidget): The table widget to populate.
                calendar (QCalendarWidget): availability calendar
        """

        self._updating_table = True # control flag
        # availability_table.blockSignals(True) # Avoid errors by triggering cellChanged

        self.calendar_manager.clear_calendar(calendar)


        availability_table.clearContents()
        availability_table.setRowCount(0) # reset number of rows

        availability = self.am.get_availability_by_id_volunteer(id_volunteer)

        for row_idx, v in enumerate(availability):
            availability_table.insertRow(row_idx)

            # ID column (hidden in UI)
            availability_table.setItem(row_idx, 0, QTableWidgetItem(str(v["id_availability"])))

            # Date columns
            availability_table.setItem(row_idx, 1, QTableWidgetItem(v["date_init"]))
            availability_table.setItem(row_idx, 2, QTableWidgetItem(v["date_end"]))

            # Confirmed column as checkbox
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            checkbox_item.setCheckState(Qt.Checked if v["confirmed"] else Qt.Unchecked)
            availability_table.setItem(row_idx, 3, checkbox_item)

            # Comments column
            comment_item = QTableWidgetItem(v["comments"] if v["comments"] else "")
            comment_item.setFlags(comment_item.flags() | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            availability_table.setItem(row_idx, 4, comment_item)

            self.calendar_manager.update_calendar_with_availability(calendar, v["date_init"], v["date_end"], v["confirmed"])

        # availability_table.blockSignals(False) # Let edit the table
        self._updating_table = False


    def update_availability(self, row: int, col: int, calendar: QCalendarWidget):
        """
            Update the availability database record based on user edits in the table.

            Parameters:
                row (int): The edited row index.
                col (int): The edited column index.
                calendar: availability calendar.
        """

        if self._updating_table:
            return  # Evita recursión o interferencias

        availability_table = self.availability_table

        try:
            id_item = availability_table.item(row, 0)
            if not id_item:
                return

            id_availability = int(id_item.text())
            id_volunteer = self.am.get_id_volunteer_from_id_availability(id_availability)

            date_init_item = availability_table.item(row, 1)
            date_end_item = availability_table.item(row, 2)
            confirmed_item = availability_table.item(row, 3)
            comments_item = availability_table.item(row, 4)

            if not date_init_item or not date_end_item:
                return  # Incompleto

            date_init = date_init_item.text()
            date_end = date_end_item.text()
            confirmed = confirmed_item.checkState() == Qt.Checked if confirmed_item else False
            comments = comments_item.text() if comments_item else ""

            # Validar fechas si cambiaron
            if col in (1, 2):
                try:
                    self.am.validate_availability(id_volunteer, date_init, date_end, id_availability)
                except ValueError as e:
                    QMessageBox.warning(None, "Error de validación", str(e))
                    self._updating_table = True
                    self.display_individual_availability_data_table(id_volunteer, availability_table, calendar)
                    self._updating_table = False
                    return

            # Actualizar
            self.am.update_availability(
                id_availability=id_availability,
                id_volunteer=id_volunteer,
                date_init=date_init,
                date_end=date_end,
                comments=comments,
                confirmed=confirmed
            )

            # Fusionar si procede y refrescar
            self._updating_table = True
            self.am.merge_periods(id_volunteer, confirmed, id_availability)
            self.display_individual_availability_data_table(id_volunteer, availability_table, calendar)
            self._updating_table = False

        except Exception as e:
            QMessageBox.critical(None, "Error inesperado", f"Ocurrió un error: {str(e)}")


    def on_availability_clicked(self, availability_table: QTableWidget, calendar: QCalendarWidget):
        """"""
        selected_item = availability_table.selectedItems()
        if not selected_item:
            return

        row = selected_item[0].row()
        date_init_item = availability_table.item(row, 1)

        if date_init_item:
            date_init = QDate.fromString(date_init_item.text(), "yyyy-MM-dd")
            if date_init.isValid():
                calendar.setSelectedDate(date_init)
                calendar.showSelectedDate()



    # TABLES FOR calendar_page #

    def define_available_volunteer_list(self, volunteer_table: QTableWidget):
        
        # Add a hidden column at beginning for ID
        volunteer_table.insertColumn(0)
        volunteer_table.setColumnHidden(0, True)
        # Avoid editing on list
        volunteer_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        # Select entire row
        volunteer_table.setSelectionBehavior(QAbstractItemView.SelectRows)


    def update_confirmed_volunteer_list(self, calendar:QCalendarWidget, volunteer_table: QTableWidget, confirmed):
        """Get selected date and update the volunteer list."""
        date_selected = calendar.selectedDate().toString("yyyy-MM-dd") 
        volunteers = self.vm.check_volunteers_in_date(date_selected, confirmed)

        # Clean table before update
        volunteer_table.setRowCount(0)

        # Load data on table
        for row_idx, v in enumerate(volunteers):
            volunteer_table.insertRow(row_idx)
            volunteer_table.setItem(row_idx, 0, QTableWidgetItem(str(v["id_volunteer"])))
            volunteer_table.setItem(row_idx, 1, QTableWidgetItem(v["name"]))  
            volunteer_table.setItem(row_idx, 2, QTableWidgetItem(v["lastname_1"]))  
            volunteer_table.setItem(row_idx, 3, QTableWidgetItem("🚑" if v["driver"] else ""))

