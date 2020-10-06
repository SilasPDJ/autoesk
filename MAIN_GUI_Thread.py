import sys
import threading
import time
from PyQt5 import QtWidgets, QtGui, QtCore

from default.settings.grid_manager import TuplasTabelas
from default.settings import SetPaths
from default.data_treatment import ExcelToData

import sys
import pandas as pd
from functools import partial

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit, QSizePolicy, QPlainTextEdit

from whatsapp import PgdasWP
from smtp_project import PgDasmailSender, SendDividas, EmailExecutor
from pgdas_fiscal_oesk import PgdasAnyCompt
from pgdas_fiscal_oesk import DownloadGinfessGui

from pgdas_fiscal_oesk import GissGui
from whatsapp import PgdasWP

from pgdas_fiscal_oesk.main_excel_manager.main_excel_manager import SheetPathManager
from smtp_project.init_email.jsondate import JsonDateWithImprove
# only static methods from JsonDateWithDataImprove


class FunctionsManager(QtCore.QObject):
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def startislife(self, *args, max_threads=5):
        """
        :param args: must be functional (methods)
        :param max_threads: ...
        :return: threads
        """
        self.started.emit()
        for e, arg in enumerate(args):
            if e == max_threads:
                break
            # exec aprendido
            threading.Thread(target=arg, daemon=True).start()
        time.sleep(1)
        self.finished.emit()


class LoadingScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint
        )

        self.label_animation = QtWidgets.QLabel(self)
        self.movie = QtGui.QMovie("loading.gif")
        self.label_animation.setMovie(self.movie)

    def startAnimation(self):
        self.movie.start()
        self.show()
        QtCore.QTimer.singleShot(2 * 1000, self.stopAnimation)

    def stopAnimation(self):
        self.movie.stop()
        self.hide()


class MainDisplays(QWidget, SetPaths, ExcelToData):
    def __init__(self):
        """
        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        super().__init__()
        self.now_selection_json_f_name = 'pgdas_fiscal_oesk/data_clients_files/clients_now_selection.json'

        self.atual_compt_and_file = self.get_atual_competencia(1, past_only=True)
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
        jsonfile = JsonDateWithImprove.load_json(self.now_selection_json_f_name)
        if jsonfile:
            """# ###################################### checka se o json_file contém dados e se os dados são p/ GINFESS"""
            my_sh_name = self.sh_names_only[df_id]
            if df_id == 3:
                # GINFESS
                self.whenGinfessBt.setDisabled(False)
            else:
                self.whenGinfessBt.setDisabled(True)

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
                # print(df.iloc[i, j], end='->')
                my_values_only = str(df.iloc[i, j]).strip()
                h_mvo = {headers[j]: my_values_only}
                ddict[i].append(h_mvo)
        print('\n', ddict)

        JsonDateWithImprove.dump_json(ddict, self.now_selection_json_f_name)
        loadit = JsonDateWithImprove.load_json(self.now_selection_json_f_name)

        self.add_thread(self.whenGinfessBt, DownloadGinfessGui, loadit)
        self.add_thread(self.whenGissBt, GissGui, loadit)

    def add_thread(self, el, *action):
        """
        :param el: QPushButton, etc
        :param action: action etc
        # partial get all the args necessary
        :return:
        """
        # for arg in args:
        try:
            el.clicked.disconnect()
        except Exception as e:
            pass

        # b4 prosseguir
        action = partial(*action)
        self._manager.started.connect(self._loading_screen.startAnimation)
        self._manager.finished.connect(self._loading_screen.stopAnimation)
        # add_el.clicked.connect(lambda: self._manager.startislife(print('test')))
        el.clicked.connect(lambda: self._manager.startislife(action))
        self._manager.started.connect(self.hide)
        self._manager.finished.connect(self.show)

    def bts_b4mail(self):

        names = 'Declara Simples Nacional', 'Editar Planilha Excel'

        callbacks = lambda: PgdasAnyCompt(self.atual_compt_and_file), SheetPathManager.save_after_changes
        return list(names), list(callbacks)


class MainApp(MainDisplays, TuplasTabelas):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading Overlay without Selenium Problem")
        self.resize(1200, 800)
        self.center()

        v_box = QtWidgets.QVBoxLayout(self)
        # v_box.addStretch()
        self.grid_add = QtWidgets.QGridLayout()
        v_box.addLayout(self.grid_add)

        self.table_add = QtWidgets.QGridLayout()
        v_box.addLayout(self.table_add)

        self.v_box = v_box

        add_el = QtWidgets.QPushButton('add_el')
        self.add_elingrid(add_el, 0, 6, 1, 1)

        self._loading_screen = LoadingScreen()
        self._manager = FunctionsManager()
        """
        self.add_thread(add_el, partial(print, 'Seu perdão vai além dos céus...',
                                        '\nNem um monte é tão alto'
                                        '\n Nem um vale tão profundo'
                                        '\nComo o amor de nosso DEUS'))
        """
        # exec() é o eval que eu procurava
        self.load_tables(0)
        # para já começar estilizado, nice

        bts_plans = list(self.parse_sh_name(data_required=False))
        for e, el_grid in enumerate(self.el_grid_setting(0, len(bts_plans), mt=1, start_row=0, start_col=1)):
            sh_ui_name = bts_plans[e]
            sh_ui_nowbt = QPushButton(sh_ui_name)
            # new == sh_ui_nowbt
            new = self.add_elingrid(sh_ui_nowbt, *el_grid, obj_name='bt_shnames')

            new.clicked.connect(partial(self.load_tables, e))
            # self.add_thread(new, partial(self.load_tables, e))

        el = QPushButton('ISS Download Ginfess')
        generator_unpacking = list(self.el_grid_setting(1, 0, start_row=1))
        generator_only1 = generator_unpacking[0]
        a, b, c, d = generator_only1
        self.whenGinfessBt = QPushButton('ISS Download Ginfess')
        self.whenGinfessBt.setDisabled(True)
        self.whenGinfessBt = self.add_elingrid(self.whenGinfessBt, a, b, c, d)
        # self.add_thread(self.whenGinfessBt, DownloadGinfessGui, JsonDateWithImprove.load_json(self.now_selection_json_f_name))
        # being add in self.data_selection

        generator_unpacking = self.el_grid_setting(1, 0, start_row=2)
        generator_only1 = list(generator_unpacking)[0]
        self.whenGissBt = QPushButton('Encerra GISS ONLINE')
        self.whenGissBt.setDisabled(False)
        self.whenGissBt = self.add_elingrid(self.whenGissBt, *generator_only1)


    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_tables(self, table_id=None):
        from PyQt5.QtWidgets import QTableWidget
        if table_id is None:
            table_id = 0
        dfs = self.parse_sh_name()

        # ta dificl conseguir column values

        any_table = QTableWidget()
        self.create_tables(any_table, dfs, table_id)
        self.v_box.addWidget(any_table)
        self.add_elingrid(any_table, 1, 1, 12, 12)

    def add_elingrid(self, el, row: int, col: int, rowspan: int, colspan: int, style=None, obj_name=None, **kwargs):
        """
        :param el: any PyQt5 element like button etc
        :param row: grid
        :param col: grid
        :param rowspan: grid
        :param colspan: grid
        :param style: style
        :param obj_name:
        :param kwargs: set new property [idk if is working yet]
        :return:
        """
        self.grid_add.addWidget(el, row, col, rowspan, colspan)
        # only clickable functions
        # no clicked anymore
        # el.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        if style:
            el.setStyleSheet(style)
        if kwargs:
            for k, v in kwargs.items():

                el.setProperty(str(k), str(v))
                # print(str(k), str(v))
        if obj_name is not None:
            el.setObjectName(obj_name)

        return el


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
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    exe = MainApp()
    exe.show()
    app.exec_()
