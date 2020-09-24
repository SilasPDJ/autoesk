from whatsapp import *


class DownloadRotinaMamae(MainWP):

    def __init__(self):
        where_to_download = self.mkdir_hoje('I', 'MAE')

        self.driver = default_qrcode_driver(where_to_download)
        driver = self.driver

        super().__init__(driver=driver)

        self.access_whatsapp_site()

        self.search_and_open('Mãe')
        self.download_midias_audiovisuais(25)

        self.quit_session()

        driver.implicitly_wait(7)

        abre_perfil = driver.find_element_by_class_name('m7liR')
        # abre_perfil.click()

        self.click_ac_elementors(abre_perfil)
        driver.implicitly_wait(12)

        self.click_elements_by_tt('Mídia, links e docs', tortil='text')

        videos_ic = driver.find_elements_by_class_name('_275OX')[0]
        self.click_ac_elementors(videos_ic, pause=2.5)
        # abre o primeiro vídeo da janela

        vai_ou_volta(1)
        # vou até o o mais antigo

        driver.find_elements_by_class_name('PVMjB')

        lengs = []
        cont = 0
        while True:
            cont += 1
            desabilitado = driver.find_elements_by_class_name('_2Pza8')
            lend = len(desabilitado)
            print(lend, '\n' if lend not in lengs else '', end='')
            lengs.append(lend if lend not in lengs else '')
            if len(desabilitado) == 0:
                break
            else:
                vai_ou_volta(0)
                # volto até o mais recente
                vai_ou_volta(1)
                # vou até o mais antigo
            if cont == 3:
                # pois provavelmente já carregou tudo
                break
        for n in range(qtd):
            baixar = self.contains_title('Baixar')
            self.click_ac_elementors(baixar)
            self.send_keys_anywhere(Keys.RIGHT)
            """acima e abaixo, dá na mesma"""
            # self.click_elements_anywhere('Baixar', tortil='title')
            sleep(1)

        print('TUDO BAIXADO, F7 para continuar')
        press_key_b4('f7')
        # SE BAIXAR HABILITADO -> PVMjB
        # SE BAIXAR DESABILITADO -> PVMjB _2Pza8

