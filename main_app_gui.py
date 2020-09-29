from pgdas_fiscal_oesk import DownloadGinfess, PgdasAnyCompt
from smtp_project import PgDasmailSender
from whatsapp.pgdas_special_wp_sender import PgdasWP

from gui import main_app_design_file as design
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

from PyQt5.QtWidgets import QMessageBox, QPushButton
Ui_MainWindow = design.Ui_MainWindow


class RedimensionarImagem(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        # self.btnEscolherArquivo.clicked.connect(self.abrir_imagem)
        if self.BtSimples.clicked.connect(
                lambda: self.ok_cancel_dialog('Atenção!!', 'Tem certeza que deseja declarar o simples?')) == QMessageBox.Ok:
            print('Ainda não consegui')

        self.BtSimples.clicked.connect(lambda: PgdasAnyCompt(1, True))

        # lambda = more args
        self.BtMail.clicked.connect(PgDasmailSender)
        self.BtWp.clicked.connect(PgdasWP)
        self.BtGinfess.clicked.connect(DownloadGinfess)

    def ok_cancel_dialog(self, title: str, msg: str):

        ok, cancel = QMessageBox.Ok, QMessageBox.Cancel
        # yes, no = QMessageBox.Yes, QMessageBox.No
        msg = QMessageBox.question(self, title, msg, ok | cancel)
        if msg == QMessageBox.Ok:
            return msg
        else:
            return msg

    def yes_no_dialog(self, title: str, msg: str):
        # ok, cancel = QMessageBox.Ok, QMessageBox.Cancel
        yes, no = QMessageBox.Yes, QMessageBox.No
        msg = QMessageBox.question(self, title, msg, yes | no)
        if msg == QMessageBox.Yes:
            return QMessageBox.Yes
        else:
            return QMessageBox.No

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = RedimensionarImagem()
    app.show()
    qt.exec_()
