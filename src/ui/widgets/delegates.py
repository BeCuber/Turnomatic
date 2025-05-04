from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit, QCheckBox
from PyQt5.QtCore import Qt, QDate

class AvailabilityDelegate(QStyledItemDelegate):
    """
        Delegate for custom cell editors in the availability table.
        - Uses a QDateEdit for date columns.
        - Uses checkboxes directly in QTableWidgetItem for the confirmed column.
    """


    def createEditor(self, parent, option, index):
        """Create appropriate editor widget depending on column."""
        col = index.column()
        if col in [1, 2]: # date_init, date_end
            editor = QDateEdit(parent)
            editor.setCalendarPopup(True)
            editor.setDisplayFormat("yyyy-MM-dd")
            return editor
        return super().createEditor(parent, option, index)


    def setEditorData(self, editor, index):
        """Set editor widget with current cell data."""
        value = index.model().data(index, Qt.EditRole)
        col =index.column()

        if col in [1, 2]: #date
            date = QDate.fromString(value, "yyyy-MM-dd")
            if date.isValid(): # Y si isValid == False? ¿Manejo error?
                editor.setDate(date)
        else:
            super().setEditorData(editor, index)


    def setModelData(self, editor, model, index):
        """Update model with data from the editor widget."""
        col = index.column()
        if col in [1, 2]:
            model.setData(index, editor.date().toString("yyyy-MM-dd"), Qt.EditRole)

        else:
            super().setModelData(editor, model, index)


    # def updateEditorGeometry(self, editor, option, index):
    #     """Set the geometry of the editor widget."""
    #     editor.setGeometry(option.rect)