from google_drive import GDrive
from pgdas_fiscal_oesk import DownloadGinfessGui, PgdasAnyCompt
from whatsapp.pgdas_special_wp_sender import PgdasWP


from whatsapp import DownloadRotinaMamae, PgdasWP, MainWP
from google_drive import GDrive
from smtp_project import PgDasmailSender, SendDividas, EmailExecutor
from whatsapp import PgdasWP

# PgdasAnyCompt(2, True)
from smtp_project.init_email.jsondate import JsonDateWithImprove
# DownloadGinfessGui(JsonDateWithImprove.load_json('pgdas_fiscal_oesk/data_clients_files/clients_now_selection.json'), compt_file=None)
# PgdasAnyCompt()

MainWP.recria_padrao()

# DownloadRotinaMamae(10)
# PastOnly
# optional arg
