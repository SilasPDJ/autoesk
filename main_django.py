from google_drive import GDrive
from pgdas_fiscal_oesk import DownloadGinfessGui, PgdasAnyCompt
from whatsapp.pgdas_special_wp_sender import PgdasWP
from smtp_project.send_pgdasmail import PgDasmailSender

import os
import sys

from pgdas_fiscal_oesk.giss_online_pt10_variascompt import GissGui as GissGuiv2
from pgdas_fiscal_oesk.giss_online_pt9 import GissGui


HERE = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])

file = '\\pgdas_fiscal_oesk\\data_clients_files\\clients_now_selection.json'
# necessário para acessar externamente
file = HERE + file


def giss_online():
    # GissGuiv2(file, '102007')
    # GissGuiv2(file)
    GissGui(file)


def download_ginfess():
    print('Download ginfess main django')
    DownloadGinfessGui(file)
    print('Download ginfess completado...')
    # Por enquanto só faz download usando o file, tenho que dar um jeito de modificar o arquivo...


def pgdas_gerador():
    PgdasAnyCompt()


def pgdas_emails():
    pass
    # PgDasmailSender(file)


def save_after_changes():
    from default.settings import SetPaths
    # self._this_compt_and_file = self.set_get_compt_file(1, past_only=True)
    __this_compt_and_file = SetPaths().set_get_compt_file(1, past_only=True, open_excel=True)
    # novo argumento open_excel True abre o excel...


def preenche_iss_valores():
    # TENHO QUE IMPORTAR SÓ DURANTE A CHAMADA ESSE EAP SE NÃO ELE ABRE EXCEL...
    import excel_app_preenche as eap
    ydm = eap.YouDidMe()
    ydm.preenche_iss_valores()
    save_after_changes()


if __name__ == '__main__':
    globals()[sys.argv[1]]()

