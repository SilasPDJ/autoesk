from pgdas_fiscal_oesk import PgdasAnyCompt
from smtp_project import PgDasmailSender

from gui import main_app_design_file as design
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

Ui_MainWindow = design.Ui_MainWindow


class RedimensionarImagem(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        # self.btnEscolherArquivo.clicked.connect(self.abrir_imagem)
        self.BtSimples.clicked.connect(lambda: PgdasAnyCompt(1, True))

        self.BtMail.clicked.connect(PgDasmailSender)


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = RedimensionarImagem()
    app.show()
    qt.exec_()
