from pgdas_fiscal_oesk import DownloadGinfess, PgdasAnyCompt
from smtp_project import PgDasmailSender
from whatsapp.pgdas_special_wp_sender import PgdasWP

from gui import main_app_design_file as design
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

from PyQt5.QtWidgets import QMessageBox, QPushButton
Ui_MainWindow = design.Ui_MainWindow


class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        # self.btnEscolherArquivo.clicked.connect(self.abrir_imagem)
        self.BtSimples.clicked.connect(
                lambda: self.BtSimples.clicked.connect(lambda: PgdasAnyCompt(1, True))
                if self.ok_cancel_dialog('Atenção!!', 'Tem certeza que deseja declarar o simples?') else QMessageBox.information(self, 'Cancelado!', 'Cancelado!'))

        # lambda = more args
        self.BtMail.clicked.connect(PgDasmailSender)
        self.BtWp.clicked.connect(PgdasWP)
        self.BtGinfess.clicked.connect(DownloadGinfess)

    def ok_cancel_dialog(self, title: str, msg: str):
        ok, cancel = QMessageBox.Ok, QMessageBox.Cancel
        # yes, no = QMessageBox.Yes, QMessageBox.No
        msg = QMessageBox.question(self, title, msg, ok | cancel)
        if msg == QMessageBox.Ok:
            return True
        return False

    def yes_no_dialog(self, title: str, msg: str):
        # ok, cancel = QMessageBox.Ok, QMessageBox.Cancel
        yes, no = QMessageBox.Yes, QMessageBox.No
        msg = QMessageBox.question(self, title, msg, yes | no)
        if msg == QMessageBox.Yes:
            return True
        return False


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = MainApp()
    app.show()
    qt.exec_()
