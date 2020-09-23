import pandas as pd

from time import sleep
from default.webdriver_utilities import WDShorcuts
# from smtp_project.init_email import JsonDateWithImprove
from whatsapp import default_qrcode_driver
from default.settings import SetPaths
# from default.data_treatment import ExcelToData

# agora sim, ------------> from default.webdriver_utilities import *


class GDrive(WDShorcuts, SetPaths):
    def __init__(self):
        where_to = self.mkdir_hoje('I', 'MAE')

        self.driver = default_qrcode_driver(where_to)
        driver = self.driver

        super().__init__(driver=driver)

        driver.get('https://drive.google.com/drive/my-drive')

    def test(self):
        print('teste')
