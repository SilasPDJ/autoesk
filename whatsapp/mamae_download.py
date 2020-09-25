from . import MainWP
from default.webdriver_utilities import Keys


class DownloadRotinaMamae(MainWP):

    def __init__(self, qtd_midias):
        from default.webdriver_utilities.pre_drivers import default_qrcode_driver
        """
        :param qtd_midias: qtd photos/videos download
        """
        where_to_download = self.mkdir_hoje('I', 'MAE')

        self.driver = default_qrcode_driver(where_to_download)
        driver = self.driver

        super().__init__(driver=driver)

        self.access_whatsapp_site()

        self.search_and_open('Mãe')
        self.download_midias_audiovisuais(qtd_midias)
        driver.implicitly_wait(7)
        self.quit_session()
