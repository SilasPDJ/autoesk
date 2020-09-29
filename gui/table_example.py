from default.settings import SetPaths
from default.data_treatment import ExcelToData

import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QPushButton, QItemDelegate, QVBoxLayout
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


class Finally:
    def __init__(self):
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
                self.resize(1200, 800)

                mainLayout = QVBoxLayout()

                self.table = TableWidget(DFEditor.df)
                mainLayout.addWidget(self.table)

                button_print = QPushButton('Display DF')
                button_print.setStyleSheet('font-size: 16px')
                button_print.clicked.connect(self.print_DF_Values)
                mainLayout.addWidget(button_print)

                button_export = QPushButton('Export to CSV file')
                button_export.setStyleSheet('font-size: 16px')
                button_export.clicked.connect(self.export_to_csv)
                mainLayout.addWidget(button_export)

                self.setLayout(mainLayout)

            def print_DF_Values(self):
                print(self.table.df)

            def export_to_csv(self):
                self.table.df.to_csv('Data export.csv', index=False)
                print('CSV file exported.')

        if __name__ == '__main__':
            app = QApplication(sys.argv)

            demo = DFEditor()
            demo.show()

            sys.exit(app.exec_())
Finally()