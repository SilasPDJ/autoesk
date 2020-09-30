from default.settings import SetPaths
from default.data_treatment import ExcelToData

import sys
import pandas as pd

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QTableView
from PyQt5.QtWidgets import QItemDelegate, QVBoxLayout, QAbstractItemView, QGridLayout

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit, QSizePolicy, QPlainTextEdit

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator


class DisplaySheets(QWidget, SetPaths, ExcelToData):
    def __init__(self):
        """
        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        super().__init__()

    def my_method(self):

        compt, excel_file_name = self.get_atual_competencia(1, past_only=True)
        xls = pd.ExcelFile(excel_file_name)
        sheet_names = iter(xls.sheet_names)
        for e, sh in enumerate(sheet_names):
            if e > 0:
                yield xls.parse(sh, dtype=str)


class MyTableWithIndex(QMainWindow, DisplaySheets):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('My Main Window At The Moment')
        self.main_wid = QWidget()
        self.grid = QGridLayout(self.main_wid)
        from pyautogui import size
        x, y = size()[0], size()[1]
        self.resize(1200, 800)
        self.display = self.add_el(QPlainTextEdit(), 6, 0, 2, 2)
        test = 1, 0, 1, 1
        self.display.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.display.setDisabled(True)
        self.display_text_from_el(self.add_el(QPushButton('Simples NacionalA'), *test), self.display, ed='clicked')
        self.display_text_from_el(self.add_el(QPushButton('Simples NacionalB'), 2, 0, 1, 1), self.display, ed='clicked')
        self.display_text_from_el(self.add_el(QPushButton('Simples NacionalC'), 3, 0, 1, 1), self.display, ed='clicked')
        self.display_text_from_el(self.add_el(QPushButton('Simples NacionalD'), 4, 0, 1, 1), self.display, ed='clicked')
        self.display_text_from_el(self.add_el(QPushButton('Simples NacionalE'), 5, 0, 1, 1), self.display, ed='clicked')


        # btn = self.ad_el(QPushButton('Simples Nacional'), 1, 0, 1, 1, self.text_to_display(btn, self.display))
        # btn = self.ad_el(QPushButton('Simples Nacional'), 1, 1, 1, 1)

        # self.tableWidget = QTableWidget()
        # self.create_tables(self.my_method())

        dfs = list(self.my_method())

        iss_t = QTableWidget()
        self.create_tables(iss_t, dfs[1])
        self.add_el(iss_t, 0, 1, 3, 3)

        icms_t = QTableWidget()
        self.create_tables(icms_t, dfs[3])
        self.add_el(icms_t, 3, 4, 3, 3)

        self.setCentralWidget(self.main_wid)

    def add_table(self):

        for df in self.my_method():
            self.setStyleSheet('font-size: 12px;')
            print(df)

    # Create tables
    def create_tables(self, table, dataframe):
        # Row count
        # self.tableWidget.setRowCount(30)

        # Column count]
        self.tableWidget = table

        self.tableWidget.setColumnCount(15)
        # ####################################### FAZER FOR LOOP NESSE 0 E 1 E ADICIONAR OS ELEMENTOS DO MEU PANDAS, EH ISTO
        # for e, df in enumerate(dataframe):
        tw, df = table, dataframe
        dc_df = df.to_dict
        n_rows = len(df.index)
        n_columns = len(df.columns)
        tw.setRowCount(n_rows)
        tw.setColumnCount(n_columns)
        # tw.setItemDelegate()

        for i in range(tw.rowCount()):
            for j in range(tw.columnCount()):
                x = '{}'.format(df.iloc[i, j])
                tw.setItem(i, j, QTableWidgetItem(x))

        # tw.setItem(0, 0, QTableWidgetItem("Name"))
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.tableWidget.itemSelectionChanged.connect(lambda: self.index_for_data(self.tableWidget))


    def add_el(self, el, row, col, rowspan, colspan, funcao=None, ed=None, style=None):
        """
        :param el: any PyQt5 element like button etc
        :param row: grid
        :param col: grid
        :param rowspan: grid
        :param colspan: grid
        :param funcao: any function (with no lambda)
        :param ed: event b4 connect
        :param style:
        :return:
        """
        self.grid.addWidget(el, row, col, rowspan, colspan)
        if ed == 'clicked':
            el.clicked.connect(lambda: funcao)

        el.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        if style:
            el.setStyleSheet(style)
        return el

    def display_text_from_el(self, el, display, ed='clicked'):
        """
        :param el: ELEMENT
        :param display: WHERE IS IT DISPLAYED
        :param ed: ELEMENT DIRECTION/EVENT
        :return:
        """
        txt = str(el.text())
        if ed == 'clicked':
            el.clicked.connect(
                lambda: display.setPlainText(txt))

    def index_for_data(self, table):
        rows = (idx.row() for idx in table.selectionModel().selectedRows())
        # tanto faz () or [], () ocupa menos espaço
        for r in rows:
            print(r)

    """
    if __name__ == '__main__':
        app = QApplication(sys.argv)

        demo = DFEditor()
        demo.show()

        sys.exit(app.exec_())
    """


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    calc = MyTableWithIndex()
    calc.show()
    qt.exec_()
