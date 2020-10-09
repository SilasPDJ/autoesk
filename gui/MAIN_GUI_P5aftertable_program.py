from default.settings import SetPaths
from default.data_treatment import ExcelToData

import sys
import pandas as pd
import threading
import time

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit, QSizePolicy, QPlainTextEdit

from whatsapp import PgdasWP
from smtp_project import PgDasmailSender, SendDividas, EmailExecutor
from pgdas_fiscal_oesk import PgdasAnyCompt
from pgdas_fiscal_oesk import DownloadGinfessGui
from whatsapp import PgdasWP

from PyQt5 import QtCore, QtGui
from default.settings.grid_manager import TuplasTabelas

from pgdas_fiscal_oesk.main_excel_manager.main_excel_manager import SheetPathManager
from smtp_project.init_email.jsondate import JsonDateWithImprove
# only static methods from JsonDateWithDataImprove

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


class CallManger:
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def start(self, arg):
        self.started.emit()
        threading.Thread(target=arg, daemon=True).start()

        time.sleep(1)
        self.finished.emit()


class DisplaySheets(QWidget, SetPaths, ExcelToData):
    def __init__(self):
        """
        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        super().__init__()
        self.now_selection_json_f_name = 'clients_now_selection.json'

        self.atual_compt_and_file = self.get_atual_compt_set(1, past_only=True)
        self.sh_names_only = list(self.parse_sh_name(False))

    def parse_sh_name(self, data_required=True):

        compt, excel_file_name = self.atual_compt_and_file
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
        table.itemSelectionChanged.connect(lambda: [self.data_selection(table, df, df_id), self.check_json_af_tb_change(table, df, df_id)])

    def check_json_af_tb_change(self, table, df, df_id):
        print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        jsonfile = JsonDateWithImprove.load_json(self.now_selection_json_f_name)
        if jsonfile:
            """# ###################################### checka se o json_file contém dados e se os dados são p/ GINFESS"""
            my_sh_name = self.sh_names_only[df_id]
            if df_id == 3:
                # GINFESS
                self.whenGinfessBt.setDisabled(False)

    def data_selection(self, table, df, df_id):
        rows = (idx.row() for idx in table.selectionModel().selectedRows())
        my_sh_name = self.sh_names_only[df_id]
        """WITH the def above, check common args"""

        n_tot_rows = len(df.index)
        n_tot_columns = len(df.columns)
        headers = df.columns.values
        headers = list(headers)
        # print(df.columns.values)

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
        JsonDateWithImprove.dump_json(ddict, self.now_selection_json_f_name)

    def bts_b4mail(self):

        names = 'Declara Simples Nacional', 'Editar Planilha Excel'

        callbacks = lambda: PgdasAnyCompt(self.atual_compt_and_file), SheetPathManager.save_after_changes
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
            sh_ui_name = bts_plans[e]
            sh_ui_nowbt = QPushButton(sh_ui_name)
            new = self.add_el(sh_ui_nowbt, *el_grid, funcao=partial(self.load_tables, e), obj_name='bt_shnames')
            # new.clicked.connect(lambda: self.whenGinfessBt.setDisabled(True))

        bts_b4mail, bts_callbacks = self.bts_b4mail()
        for e, el_grid in enumerate(self.el_grid_setting(len(bts_b4mail), 0, mt=0, start_row=1)):
            # self.display_text_from_el(self.add_el(QPushButton('Simples NacionalA'), *el_grid), self.display, ed='clicked')
            self.add_el(QPushButton(bts_b4mail[e]), *el_grid, funcao=bts_callbacks[e])

        generator_unpacking = list(self.el_grid_setting(1, 0, start_row=len(bts_b4mail)+1))
        generator_only1 = generator_unpacking[0]
        a, b, c, d = generator_only1
        self.whenGinfessBt = QPushButton('ISS Download Ginfess')
        self.whenGinfessBt.setDisabled(True)
        self.whenGinfessBt = self.add_el(self.whenGinfessBt, a, b, c, d,
                                         funcao=self.whenginfessbt_call_funcs
                                         )

        self.setCentralWidget(self.main_wid)

    def whenginfessbt_call_funcs(self):
        from functools import partial
        # carrega a tabela se eu clicar em ISS ginfess
        self.load_tables(2)
        DownloadGinfessGui(JsonDateWithImprove.load_json(self.now_selection_json_f_name))

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

    # unused
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

