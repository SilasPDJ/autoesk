import pandas as pd

from time import sleep
from default.webdriver_utilities import *
from default.interact import *
from smtp_project.init_email import JsonDateWithImprove

from default.settings import SetPaths
from default.data_treatment import ExcelToData

from default.webdriver_utilities.pre_drivers import pgdas_driver

from .ginfess_download import DownloadGinfess
from .rotina_pgdas import PgdasAnyCompt
# outside
# cópia, de whatsapp consigo herdar a class
