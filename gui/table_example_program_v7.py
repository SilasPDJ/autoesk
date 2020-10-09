from default.settings import SetPaths
from default.data_treatment import ExcelToData

import sys
import pandas as pd

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit, QSizePolicy, QPlainTextEdit

from whatsapp import PgdasWP
from smtp_project import PgDasmailSender, SendDividas, EmailExecutor
from pgdas_fiscal_oesk import PgdasAnyCompt
from pgdas_fiscal_oesk import DownloadGinfessGui
from whatsapp import PgdasWP

from pgdas_fiscal_oesk.main_excel_manager.main_excel_manager import SheetPathManager
from smtp_project.init_email.jsondate import JsonDateWithImprove
# only static methods from JsonDateWithDataImprove


class DisplaySheets(QWidget, SetPaths, ExcelToData):
    def __init__(self):
        """
        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        super().__init__()
        self.now_selection_json = 'clients_now_selection.json'

    def parse_sh_name(self, data_required=True):

        compt, excel_file_name = self.get_atual_compt_set(1, past_only=True)
        xls = pd.ExcelFile(excel_file_name)
        sheet_names = iter(xls.sheet_names)
        for e, sh in enumerate(sheet_names):
            # if e > 0:
            if data_required:
                yield xls.parse(sh, dtype=str)
            else:
                yield sh

    # Create tables
    def create_tables(self, table, dataframes, df_id):
        tw, df = table, list(dataframes)[df_id]
        # print(type(df))
        headers = df.columns.values
        headers = list(headers)
        # column_count = len(headers)
        n_rows = len(df.index)
        n_columns = len(df.columns)
        # PD

        tw.setRowCount(n_rows)
        tw.setColumnCount(n_columns)
        # GUI
        # tw.setItemDelegate()

        for i in range(tw.rowCount()):
            for j in range(tw.columnCount()):
                x = '{}'.format(df.iloc[i, j])
                tw.setItem(i, j, QTableWidgetItem(x))
        tw.setHorizontalHeaderLabels(headers)
        # tw.setItem(0, 0, QTableWidgetItem("Name"))

        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.itemSelectionChanged.connect(lambda: self.data_selection(table, df, df_id))

    def data_selection(self, table, df, df_id):
        rows = (idx.row() for idx in table.selectionModel().selectedRows())

        n_tot_rows = len(df.index)
        n_tot_columns = len(df.columns)
        headers = df.columns.values
        headers = list(headers)
        # print(df.columns.values)

        sh_name = list(self.parse_sh_name(False))[df_id]

        # print(dc_df, type(dc_df)

        ddict = {}
        for i in rows:
            ddict[i] = []
            for j in range(n_tot_columns):
                pass
                print(df.iloc[i, j], end='->')
                my_values_only = str(df.iloc[i, j]).strip()
                h_mvo = {headers[j]: my_values_only}
                ddict[i].append(h_mvo)
        print('\n', ddict)
        """
        print(sh_name)
        for r in rows:
            print(r)
            # print(df.title)
        """
        JsonDateWithImprove.dump_json(ddict, self.now_selection_json)


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

        # names = 'Declara Simples Nacional', ['Download Ginfess'], 'Editar Planilha Excel'
        # callbacks = PgDasmailSender, DownloadGinfessGui, SheetPathManager.save_after_changes

        names = 'Declara Simples Nacional', 'Editar Planilha Excel'
        callbacks = PgDasmailSender, SheetPathManager.save_after_changes
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
            self.add_el(QPushButton(bts_plans[e]), *el_grid, funcao=partial(self.load_tables, e), obj_name='bt_shnames')

        bts_b4mail, bts_callbacks = self.bts_b4mail()
        # bts_b4mail.append('Load Tables')
        # bts_callbacks.append(self.load_tables)

        for e, el_grid in enumerate(self.el_grid_setting(len(bts_b4mail), 0, mt=0, start_row=1)):
            # self.display_text_from_el(self.add_el(QPushButton('Simples NacionalA'), *el_grid), self.display, ed='clicked')

            self.add_el(QPushButton(bts_b4mail[e]), *el_grid, funcao=bts_callbacks[e])

        generator_unpacking = list(self.el_grid_setting(1, 0, start_row=len(bts_b4mail)+1))
        generator_only1 = generator_unpacking[0]
        a, b, c, d = generator_only1

        self.add_el(QPushButton('Download Ginfess'), a, b, c, d,
                    funcao=partial(DownloadGinfessGui, JsonDateWithImprove.load_json(self.now_selection_json))
                    )
        # self.load_tables()

        self.setCentralWidget(self.main_wid)

    def load_tables(self, table_id=None):
        if table_id is None:
            table_id = 0
        dfs = self.parse_sh_name()
        # ta dificl conseguir column values

        any_table = QTableWidget()
        self.create_tables(any_table, dfs, table_id)
        self.add_el(any_table, 1, 1, 12, 12)

    def add_el(self, el, row: int, col: int, rowspan: int, colspan: int, funcao=None, style=None, obj_name=None, **kwargs):
        """
        :param el: any PyQt5 element like button etc
        :param row: grid
        :param col: grid
        :param rowspan: grid
        :param colspan: grid
        :param funcao: any function (with no lambda)
        :param style: style
        :param obj_name:
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
        if obj_name is not None:
            el.setObjectName(obj_name)
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
            # lambda: [display.setPlainText(txt), print('double func')])
            el.clicked.connect(
                lambda: [display.setPlainText(txt)]
            )


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
#bt_shnames {
background-color: red;
}

QPushButton:hover, #bt_shnames:hover {
    background-color: lightblue;
}
QPushButton:pressed, #bt_shnames:pressed {
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
