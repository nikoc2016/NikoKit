from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin


class NQWidgetTable(NQMixin, QTableWidget):
    def __init__(self, *args, **kwargs):
        super(NQWidgetTable, self).__init__(*args, **kwargs)

        # Table
        self.top_headers = []
        self.left_headers = []
        self.table_data = []

    def set_data(self):
        # Where you define your render logic, use _set_data if necessary
        pass

    def _set_data_rows(self, top_headers, left_headers, table_data):
        self.top_headers = top_headers[:]
        self.left_headers = left_headers[:]
        self.table_data = table_data[:]

        self.init_table()

        for row_idx, data_row in enumerate(self.table_data):
            for col_idx, cell_data in enumerate(data_row):
                value, color = cell_data
                value = str(value)
                new_table_widget_data = QTableWidgetItem(value)
                new_table_widget_data.setForeground(QBrush(QColor(color)))
                self.setItem(row_idx, col_idx, new_table_widget_data)

        self.stretch_table()

    def _set_data_columns(self, top_headers, left_headers, table_data):
        self.top_headers = top_headers[:]
        self.left_headers = left_headers[:]
        self.table_data = table_data[:]

        self.init_table()

        for col_idx, data_col in enumerate(self.table_data):
            for row_idx, cell_data in enumerate(data_col):
                value, color = cell_data
                value = str(value)
                new_table_widget_data = QTableWidgetItem(value)
                new_table_widget_data.setForeground(QBrush(QColor(color)))
                self.setItem(row_idx, col_idx, new_table_widget_data)

        self.stretch_table()

    def init_table(self):
        self.setRowCount(len(self.left_headers))
        self.setColumnCount(len(self.top_headers))
        self.setHorizontalHeaderLabels(self.top_headers)
        self.setVerticalHeaderLabels(self.left_headers)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def stretch_table(self):
        header = self.horizontalHeader()

        header.setSectionResizeMode(QHeaderView.Interactive)
        self.resizeColumnsToContents()
