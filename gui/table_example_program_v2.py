from default.settings import SetPaths
from default.data_treatment import ExcelToData

import sys
import pandas as pd

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit, QSizePolicy, QPlainTextEdit

from whatsapp import PgdasWP
from smtp_project import PgDasmailSender, SendDividas, EmailExecutor
from pgdas_fiscal_oesk import PgdasAnyCompt, DownloadGinfess
from whatsapp import PgdasWP

from pgdas_fiscal_oesk.main_excel_manager.main_excel_manager import SheetPathManager


class DisplaySheets(QWidget, SetPaths, ExcelToData):
    def __init__(self):
        """
        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        super().__init__()

    def parse_sh_name(self, data_required=True):

        compt, excel_file_name = self.get_atual_competencia(1, past_only=True)
        xls = pd.ExcelFile(excel_file_name)
        sheet_names = iter(xls.sheet_names)
        for e, sh in enumerate(sheet_names):
            # if e > 0:
            if data_required:
                yield xls.parse(sh, dtype=str)
            else:
                yield sh
    """
    def add_table(self):

        for df in self.parse_sh_name():
            self.setStyleSheet('font-size: 12px;')
            print(df)
    """

    # Create tables
    def create_tables(self, table, dataframe):
        # Row count
        # self.tableWidget.setRowCount(30)

        # Column count]
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
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.itemSelectionChanged.connect(lambda: self.index_for_data(table))

    def index_for_data(self, table):
        rows = (idx.row() for idx in table.selectionModel().selectedRows())
        for r in rows:
            print(r)


class TuplasTabelas:
    def el_grid_setting(self, row: int, col: int, rp=1, cp=1, mt=0, start_row=0, start_col=0):
        """
        :param row: till row
        :param col: till col
        :param rp: row_span
        :param cp: col_span
        :param start_row: ...
        :param start_col: ...

        :param mt: 0 -> line increment, 1 -> col increment, 2 -> both increment

        :return: generator with all equal sized for grid
        """
        if mt > 2:
            mt = 0

        range_row = row + start_row
        range_col = col + start_col

        from itertools import zip_longest
        if mt == 0:
            # line increment
            for r, c, rs, cs in zip_longest(range(start_row, range_row), f'{col}' * row,
                                            range(rp, rp + 1), range(cp, cp + 1), fillvalue=1):
                tup = int(r), int(c), int(rs), int(cs)
                # print(tup)
                yield tup
        elif mt == 1:
            # col increment
            for r, c, rs, cs in zip_longest(f'{row}' * col, range(start_col, range_col),
                                            range(rp, rp + 1), range(cp, cp + 1), fillvalue=1):
                tup = int(r), int(c), int(rs), int(cs)
                # print(tup)
                yield tup
        elif mt == 2:
            # both increment
            for r in range(0, row):
                for c in range(0, col):
                    # print('col')
                    for rs, cs in zip(range(rp, rp + 1), range(cp, cp + 1)):
                        tup = int(r), int(c), int(rs), int(cs)
                        yield tup

        # input()

    def bts_b4mail(self):
        # 'Declara Giss Online' -> ainda sem
        #  'Open Excel File' -> AINDA SEM
        names = 'Declara Simples Nacional', 'Download Ginfess', 'Editar Planilha Excel'
        callbacks = PgDasmailSender, DownloadGinfess, SheetPathManager.save_after_changes
        return list(names), list(callbacks)


class MainApp(QMainWindow, DisplaySheets, TuplasTabelas):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('My Main Window At The Moment')
        self.main_wid = QWidget()
        self.grid = QGridLayout(self.main_wid)
        from pyautogui import size
        x, y = size()[0], size()[1]
        self.resize(1200, 800)
        self.display = self.add_el(QPlainTextEdit(), 6, 2, 2, 2)
        self.display.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.display.setDisabled(True)
        from functools import partial
        bts_plans = list(self.parse_sh_name(data_required=False))
        for e, el_grid in enumerate(self.el_grid_setting(0, len(bts_plans), mt=1, start_col=1)):
            self.display_text_from_el(self.add_el(QPushButton(bts_plans[e]), *el_grid, style='background-color:green',
                                                  funcao=partial(self.load_tables, e)), self.display)

        bts_b4mail, bts_callbacks = self.bts_b4mail()
        # bts_b4mail.append('Load Tables')
        # bts_callbacks.append(self.load_tables)

        for e, el_grid in enumerate(self.el_grid_setting(len(bts_b4mail), 0, mt=0, start_row=1)):
            # self.display_text_from_el(self.add_el(QPushButton('Simples NacionalA'), *el_grid), self.display, ed='clicked')
            self.display_text_from_el(self.add_el(QPushButton(bts_b4mail[e]), *el_grid, funcao=bts_callbacks[e]), self.display)
        # btn = self.ad_el(QPushButton('Simples Nacional'), 1, 0, 1, 1, self.text_to_display(btn, self.display))
        # self.load_tables()

        self.setCentralWidget(self.main_wid)

    def load_tables(self, table_id=None):
        if table_id is None:
            table_id = 0
        dfs = list(self.parse_sh_name())
        any_table = QTableWidget()
        self.create_tables(any_table, dfs[table_id])
        self.add_el(any_table, 1, 1, 12, 12)

    def add_el(self, el, row: int, col: int, rowspan: int, colspan: int, funcao=None, style=None, **kwargs):
        """
        :param el: any PyQt5 element like button etc
        :param row: grid
        :param col: grid
        :param rowspan: grid
        :param colspan: grid
        :param funcao: any function (with no lambda)
        :param ed: event b4 connect
        :param style: style
        :param kwargs: set new property [idk if is working yet]
        :return:
        """
        self.grid.addWidget(el, row, col, rowspan, colspan)
        # only clickable functions
        if funcao is not None:
            el.clicked.connect(lambda: funcao())

        el.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        if style:
            el.setStyleSheet(style)
        if kwargs:
            for k, v in kwargs.items():
                el.setProperty(str(k), str(v))
                print(str(k), str(v))
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
                lambda: [display.setPlainText(txt), print('double func')])


style_sheet = '''
QWidget {
    background-color: white;
} 

QLabel {
    font: medium Ubuntu;
    font-size: 20px;
    color: #006325;     
}        
QPushButton {
    min-width:  70px;
    max-width:  120px;
    min-height: 70px;
    max-height: 120px;
    background-color: lightgreen;

    border-radius: 5px;        
    border-width: 1px;
    border-color: #ae32a0;
    border-style: solid;
}
QPushButton:hover {
    background-color: lightblue;
}
QPushButton:pressed {
    color: white;
    background-color: black;
}    

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    exe = MainApp()
    exe.show()
    app.exec_()
