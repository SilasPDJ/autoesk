from default.settings import SetPaths
from default.data_treatment import ExcelToData

import sys
import pandas as pd

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
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


class MyTableWithIndex(QMainWindow, DisplaySheets, ):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('My Main Window At The Moment')
        self.main_wid = QWidget()
        self.grid = QGridLayout(self.main_wid)
        from pyautogui import size
        x, y = size()[0], size()[1]
        self.setFixedSize(x, y)
        self.display = self.add_el(QPlainTextEdit(), 0, 1, 2, 2)

        self.display.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.display.setDisabled(True)
        self.display_text_from_el(self.add_el(QPushButton('Simples Nacional'), 1, 0, 1, 1), self.display, ed='clicked')

        # btn = self.ad_el(QPushButton('Simples Nacional'), 1, 0, 1, 1, self.text_to_display(btn, self.display))
        # btn = self.ad_el(QPushButton('Simples Nacional'), 1, 1, 1, 1)
        # btn = self.ad_el(QPushButton('Simples Nacional'), 1, 0, 1, 1)

        self.add_table()
        self.create_table()

        self.add_el(self.tableWidget, 0, 2, 6, 6)

        self.setCentralWidget(self.main_wid)

    def add_table(self):
        bb = QTableWidget()

        for df in self.my_method():
            self.setStyleSheet('font-size: 12px;')
            print(df)

    # Create table
    def create_table(self):
        self.tableWidget = QTableWidget()

        # Row count
        self.tableWidget.setRowCount(4)

        # Column count
        self.tableWidget.setColumnCount(2)
        # ####################################### FAZER FOR LOOP NESSE 0 E 1 E ADICIONAR OS ELEMENTOS DO MEU PANDAS, EH ISTO
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Name"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("City"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Aloysius"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Indore"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Alan"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Bhopal"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Arnavi"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Mandsaur"))

        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

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
        txt = str(el.text())
        if ed == 'clicked':
            el.clicked.connect(
                lambda: display.setPlainText(txt))

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
