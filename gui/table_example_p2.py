from default.settings import SetPaths
from default.data_treatment import ExcelToData

import sys
import pandas as pd

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QItemDelegate, QVBoxLayout, QAbstractItemView, QGridLayout

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit, QSizePolicy

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator


class DisplaySheets(QWidget, SetPaths, ExcelToData):
    def __init__(self, meses_atras, past_only=True):
        """
        :param meses_atras: custom = -1 // 1 month ago
        :param past_only: True -> only past,  False-> past and future active

        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        super().__init__()

        sh_names = 'sem_mov', 'G5_ISS', 'G5_ICMS'
        compt, excel_file_name = self.get_atual_competencia(meses_atras, past_only=past_only)
        xls = pd.ExcelFile(excel_file_name)
        sheet_names = iter(xls.sheet_names)

        for e, sh in enumerate(sheet_names):
            df1 = xls.parse(sh, dtype=str)
            if e > 0:
                # input(df1)
                a = df1.to_csv()


class MyTableWithIndex(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('My Main Window At The Moment')
        self.main_wid = QWidget()
        self.grid = QGridLayout(self.main_wid)
        self.setFixedSize(800, 600)
        self.display = self.add_el(QLineEdit(), 0, 0, 1, 1)

        self.display.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.display.setDisabled(True)
        self.display_text_from_el(self.add_el(QPushButton('Simples Nacional'), 1, 0, 1, 1), self.display)

        # btn = self.ad_el(QPushButton('Simples Nacional'), 1, 0, 1, 1, self.text_to_display(btn, self.display))
        # btn = self.ad_el(QPushButton('Simples Nacional'), 1, 1, 1, 1)
        # btn = self.ad_el(QPushButton('Simples Nacional'), 1, 0, 1, 1)
        self.add_el(QPushButton('adasdsa'), 2, 0, 1, 1, print('test'), ed='clicked')
        self.setCentralWidget(self.main_wid)

        class FloatDelegate(QItemDelegate):
            def __init__(self, parent=None):
                super().__init__()

            def createEditor(self, parent, option, index):
                editor = QLineEdit(parent)
                editor.setValidator(QDoubleValidator())
                return editor

        class TableWidget(QTableWidget):
            def __init__(self, df):
                super().__init__()
                self.df = df
                self.setStyleSheet('font-size: 12px;')

                # set table dimension
                nRows, nColumns = self.df.shape
                self.setColumnCount(nColumns)
                self.setRowCount(nRows)

                self.setHorizontalHeaderLabels(self.df.head())
                self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                self.setItemDelegateForColumn(1, FloatDelegate())

                # data insertion
                for i in range(self.rowCount()):
                    for j in range(self.columnCount()):
                        self.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))

                self.cellChanged[int, int].connect(self.updateDF)

            def updateDF(self, row, column):
                text = self.item(row, column).text()
                self.df.iloc[row, column] = text

        class DFEditor(QWidget):
            data = {
                'Col X': list('ABCD'),
                'col Y': [10, 20, 30, 40]
            }

            # df = pd.DataFrame(data)

            df = pd.read_excel(SetPaths().get_atual_competencia()[1], sheet_name='G5_ISS')

            def __init__(self):
                super().__init__()
                self.resize(1150, 720)

                mainLayout = QVBoxLayout()


                self.table = TableWidget(DFEditor.df)
                self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.table.itemSelectionChanged.connect(self.index_for_data)
                mainLayout.addWidget(self.table)
                self.setLayout(mainLayout)

            def bt1(self):
                pass

            def bt2_export_to_csv(self):
                self.table.df.to_csv('Data export.csv', index=False)
                print('CSV file exported.')

            def index_for_data(self):
                rows = (idx.row() for idx in self.table.selectionModel().selectedRows())
                # tanto faz () or [], () ocupa menos espaço
                for r in rows:
                    print(r)

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

        if ed == 'clicked':
            el.clicked.connect(
                lambda: display.setText(

                    display.text() + el.text()
                )
            )

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
