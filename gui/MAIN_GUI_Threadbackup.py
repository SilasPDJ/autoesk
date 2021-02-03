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
from smtp_project import PgDasmailSender, SendDividas
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
        self._this_compt_and_file = self.get_atual_compt_set(1, past_only=True)

        self.sh_names_only = list(self.parse_sh_name(self._this_compt_and_file, False))

    # Create tables
    def create_tables(self, table, dataframes, df_id):


        table.clearSelection()
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
                x = x.strip()
                tw.setItem(i, j, QTableWidgetItem(x))

        tw.setHorizontalHeaderLabels(headers)
        # tw.setItem(0, 0, QTableWidgetItem("Name"))
        table.setSelectionBehavior(QAbstractItemView.SelectRows)

        table.itemSelectionChanged.connect(lambda: self.data_selection(table, df, df_id))

    def wexplorer(self):
        """
        :return:
        """
        json_file = JsonDateWithImprove.load_json(self.now_selection_json_f_name)
        from subprocess import Popen
        # Popen(r'explorer "C:\path\of\folder"')
        for eid in json_file.keys():
            after_json = self.readnew_lista_v_atual(json_file[eid])

            custom_values = [v.values() for v in json_file[eid]]
            # print(custom_values[0])
            _cliente = ''.join(custom_values[0])
            # input(_cliente)
            op_path = self._files_path_v3(_cliente)
            Popen(f'explorer "{op_path}"')
            # exec(b)

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
        # J -> ROWS, I-> COLOUNS

        for i in rows:
            ddict[i] = []
            for j in range(n_tot_columns):
                # print(df.iloc[i, j], end='->')
                my_values_only = str(df.iloc[i, j]).strip()
                h_mvo = {headers[j]: my_values_only}
                ddict[i].append(h_mvo)

            ddict[i].append({'spreadsheet': my_sh_name})
        # print('\n', ddict)

        JsonDateWithImprove.dump_json(ddict, self.now_selection_json_f_name)
        self.rotines_update()

    def _gui_cb_set_compt(self, new):
        """
        :param new: from signal [str]
        :return:
        """
        print('whatever', new)

        self._this_compt_and_file = list(self._this_compt_and_file)
        compt, filetc = self._this_compt_and_file
        filetc = filetc.replace(compt, str(new))
        compt = new
        self._this_compt_and_file = compt, filetc
        # '08-2020' está em '08-2020.xlsx'

        self.rotines_update()

    def rotines_update(self):
        loadit = JsonDateWithImprove.load_json(self.now_selection_json_f_name)
        self.add_thread(self.whenGinfessBt, DownloadGinfessGui, loadit, self._this_compt_and_file)
        self.add_thread(self.whenGissBt, GissGui, loadit)
        self.add_thread(self.whenMailSenderBt, PgDasmailSender, loadit, self._this_compt_and_file)

        self.add_thread(self.whenSimplesNacionalBt, PgdasAnyCompt, self._this_compt_and_file)
        # sem o json file

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
        except (TypeError, UnboundLocalError)as e:
            pass

        # b4 prosseguir
        action = partial(*action)
        self._manager.started.connect(self._loading_screen.startAnimation)
        self._manager.finished.connect(self._loading_screen.stopAnimation)
        # add_el.clicked.connect(lambda: self._manager.startislife(print('test')))
        el.clicked.connect(lambda: self._manager.startislife(action))
        self._manager.started.connect(self.hide)
        self._manager.finished.connect(self.show)


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

        self.any_table = QTableWidget()

        self._loading_screen = LoadingScreen()
        self._manager = FunctionsManager()
        # exec() é o eval que eu procurava
        self.load_tables(0)
        # para já começar estilizado, nice

        bts_plans = list(self.parse_sh_name(self._this_compt_and_file, data_required=False))
        for e, el_grid in enumerate(self.el_grid_setting(0, len(bts_plans), mt=1, start_row=0, start_col=1)):
            sh_ui_name = bts_plans[e]
            sh_ui_nowbt = QPushButton(sh_ui_name)
            # new == sh_ui_nowbt
            new = self.add_elingrid(sh_ui_nowbt, *el_grid, obj_name='bt_shnames')

            new.clicked.connect(partial(self.load_tables, e))

        generator_unpacking = self.el_grid_setting(1, 0, start_row=0)
        generator_only1 = list(generator_unpacking)[0]
        self.whenChangeComptCB = QtWidgets.QComboBox()
        for i in range(1, 5):
            compt, file = self.get_atual_compt_set(i, past_only=True)
            self.whenChangeComptCB.addItem(compt)
        self.whenChangeComptCB.activated[str].connect(self._gui_cb_set_compt)
        self.whenChangeComptCB = self.add_elingrid(self.whenChangeComptCB, *generator_only1, obj_name='bt_edit_plan')


        generator_unpacking = self.el_grid_setting(1, 0, start_row=1)
        generator_only1 = list(generator_unpacking)[0]
        self.whenExcelEditBt = QPushButton('Editar Planilha Excel')
        # self.whenExcelEditBt.setDisabled(False)
        self.whenExcelEditBt = self.add_elingrid(self.whenExcelEditBt, *generator_only1, obj_name='bt_edit_plan')
        self.add_thread(self.whenExcelEditBt, SheetPathManager.save_after_changes)

        generator_unpacking = self.el_grid_setting(1, 0, start_row=2)
        generator_only1 = list(generator_unpacking)[0]
        self.whenGissBt = QPushButton('Encerra GISS ONLINE')
        # self.whenGissBt.setDisabled(False)
        self.whenGissBt = self.add_elingrid(self.whenGissBt, *generator_only1)

        generator_unpacking = list(self.el_grid_setting(1, 0, start_row=3))
        generator_only1 = generator_unpacking[0]
        a, b, c, d = generator_only1
        self.whenGinfessBt = QPushButton('ISS Download Ginfess')
        self.whenGinfessBt.setDisabled(True)
        self.whenGinfessBt = self.add_elingrid(self.whenGinfessBt, a, b, c, d)
        #

        generator_unpacking = self.el_grid_setting(1, 0, start_row=4)
        generator_only1 = list(generator_unpacking)[0]
        self.whenSimplesNacionalBt = QPushButton('Todos Simples Nacional')
        # self.whenGissBt.setDisabled(False)
        self.whenSimplesNacionalBt = self.add_elingrid(self.whenSimplesNacionalBt, *generator_only1, obj_name='btSimplesNacional')
        """este add_thread abaixo está em rotines_update também"""
        self.add_thread(self.whenSimplesNacionalBt, PgdasAnyCompt, self._this_compt_and_file)
        #

        generator_unpacking = self.el_grid_setting(1, 0, start_row=5)
        generator_only1 = list(generator_unpacking)[0]
        self.whenMailSenderBt = QPushButton('ISS emails')
        self.whenMailSenderBt = self.add_elingrid(self.whenMailSenderBt, *generator_only1)
        # add_thread in data_selection

        generator_unpacking = self.el_grid_setting(1, 0, start_row=6)
        generator_only1 = list(generator_unpacking)[0]
        self.whenExplorerBt = QPushButton('Abre Pasta Explorer')
        self.whenExplorerBt = self.add_elingrid(self.whenExplorerBt, *generator_only1)
        self.add_thread(self.whenExplorerBt, lambda: self.wexplorer())

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_tables(self, table_id=None):
        from PyQt5.QtWidgets import QTableWidget
        if table_id is None:
            table_id = 0
        dfs = self.parse_sh_name(self._this_compt_and_file)

        # ta dificl conseguir column values

        any_table = self.any_table
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

#bt_edit_plan{
background-color: green;
}
#bt_edit_plan:hover{
background-color: gray;
}
#btSimplesNacional{
background-color: orange;
}


QPushButton:hover, #bt_shnames:hover, #btSimplesNacional:hover {
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
