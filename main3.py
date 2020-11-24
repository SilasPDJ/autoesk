from google_drive import GDrive
from pgdas_fiscal_oesk import DownloadGinfessGui, PgdasAnyCompt
from whatsapp.pgdas_special_wp_sender import PgdasWP

from pgdas_fiscal_oesk.giss_online_pt10_variascompt import GissGui as GissGuiv2


file = 'pgdas_fiscal_oesk/data_clients_files/clients_now_selection.json'
GissGuiv2(file, 1, 0)
# um mes atrás, 0 anos atrás

# PastOnly
# optional arg
