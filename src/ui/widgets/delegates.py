from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit, QComboBox
from PyQt5.QtCore import Qt, QDate

class AvailabilityDelegate(QStyledItemDelegate):
    """"""
    def createEditor(self, parent, option, index):
        """"""
        col = index.column()
        if col in [1, 2]: # date_init, date_end
            editor = QDateEdit(parent)
            editor.setCalendarPopup(True)
            editor.setDisplayFormat("yyyy-MM-dd")
            return editor
        elif col == 3: # confirmed
            editor = QComboBox(parent)
            editor.addItems(["", "✅"])
            return editor
        return super().createEditor(parent, option, index)


    def setEditorData(self, editor, index):
        """"""
        value = index.model().data(index, Qt.EditRole)
        col =index.column()

        if col in [1, 2]: #date
            date = QDate.fromString(value, "yyyy-MM-dd")
            editor.setDate(date)
        elif col == 3: # confirmed
            editor.setCurrentText(value if value == "✅" else "")
        else:
            super().setEditorData(editor, index)


    def setModelData(self, editor, model, index):
        """"""
        col = index.column()
        if col in [1, 2]:
            model.setData(index, editor.date().toString("yyyy-MM-dd"), Qt.EditRole)
        elif col == 3:
            model.setData(index, editor.currentText(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)