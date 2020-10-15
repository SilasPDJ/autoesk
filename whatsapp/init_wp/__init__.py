from default.webdriver_utilities import WDShorcuts
from default.settings import SetPaths
from whatsapp.dialog_profile_path import profiles_main_folder
from default.webdriver_utilities import Options, WebDriverException, NoSuchElementException, Keys
from time import sleep

from default.webdriver_utilities import *
from default.interact import *
from smtp_project.init_email import JsonDateWithImprove


class MainWP(WDShorcuts, SetPaths):
    # eu sou a padrão
    def __init__(self, driver):
        """
        :param driver: None -> Recria padrão para armazenar perfis
        """

        self.padrao = profiles_main_folder()
        self.driver = driver
        if driver is not None:
            super().__init__(driver)
        else:
            self.recria_padrao()
            pass

        # depois eu vou fazer um json do for loop xD

    @classmethod
    def recria_padrao(cls):
        self = MainWP(None)

        print('\033[1;31m Parâmetro driver None, criando driver PADRÃO caso não exista em\033[m')

        driver = self.whatsapp_DRIVER(padrao=self.padrao)

        [(print(cont, 'ABORTE A QUALQUER MOEMNTO'), sleep(1)) for cont in range(10, 0, -1)]
        driver.get('https://web.whatsapp.com/')
        print('pressione enter após escanear')
        press_key_b4('enter')
        [(print(f'-> {i}'), sleep(1)) for i in range(10, -1, -1)]
        self.quit_session()
        print('Driver closed')

    def quit_session(self):
        try:
            self.driver.close()
            self.driver.quit()
        except WebDriverException:
            print('Não existe driver ativo')

    def access_whatsapp_site(self):
        driver = self.driver
        driver.get('https://web.whatsapp.com/')
        driver.implicitly_wait(20)
        while True:
            try:
                driver.find_element_by_tag_name('span')
                break
            except NoSuchElementException:
                print('Celular desconectado, vou dar refresh')
                driver.refresh()

    def full_copy_dir(self, src, dst, symlinks=False, ignore=None):
        """
        :param src: from
        :param dst: destiny
        :param symlinks: lnk files
        :param ignore: erros
        :return:
        """
        import os
        import shutil
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def search_and_open(self, contact):
        driver = self.driver
        driver.implicitly_wait(10)

        self.procura_contato(contact)
        if contact.isnumeric():
            self.send_keys_anywhere(Keys.DOWN)
            self.send_keys_anywhere(Keys.ENTER)
        else:
            self.abre_conversa(contact)

    def procura_contato(self, nome):
        """
        :param nome: Nome do contato
        :return:
        """
        driver = self.driver
        self.click_elements_by_tt('Procurar ou começar uma nova conversa')

        self.send_keys_anywhere('')
        driver.implicitly_wait('2.5')
        self.send_keys_anywhere(nome)
        driver.implicitly_wait(2.5)

    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        """
        labels = driver.find_elements_by_tag_name('label')
        labels[0].click()
        self.send_keys_anywhere(contato)
        """
        # procura inicial
        driver = self.driver
        conversa = driver.find_element_by_xpath(f"//span[@title = '{contato}']")
        self.click_ac_elementors(conversa)
        driver.implicitly_wait(2.5)

        # Entra na conversa

    def anexa_wp_files(self, *files):
        from selenium.webdriver.common.action_chains import ActionChains

        driver = self.driver
        driver.implicitly_wait(5)

        for file in files:
            self.click_ac_elementors(driver.find_element_by_css_selector("span[data-icon='clip']"))
            anx = driver.find_element_by_css_selector("input[type='file']")

            anx.send_keys(r'{}'.format(file))
            driver.implicitly_wait(10)
            envia = driver.find_element_by_css_selector("span[data-icon='send']")

            driver.implicitly_wait(10)
            ac = ActionChains(driver=driver)
            ac.move_to_element(envia)
            ac.click()
            ac.perform()
            sleep(3)

    def write_wp_msg(self, *mensagens):
        """
        :param mensagens: str or list
        :return: mensagens escrita no zap/wp/WhatsApp
        """
        def check_emojis(msg):
            # starta com : -> vira emoji
            if msg.startswith(':'):
                msg = msg.split(':')[:]
                msg = '\n:'.join(msg)
                msg += '\n'
            return msg

        self.click_elements_by_tt('Digite uma mensagem')
        for msg in mensagens:
            if isinstance(msg, list):
                for v in msg:
                    v = str(check_emojis(v))
                    self.send_keys_anywhere(v, pause=0.01)
                    self.send_keys_anywhere(Keys.ENTER)
            else:
                msg = str(check_emojis(msg))
                self.send_keys_anywhere(msg, pause=0.01)
                self.send_keys_anywhere(Keys.ENTER)

    def read_wp_inside_msg(self, in_or_out=0):
        """
        :param int in_or_out: select in (0) -> coming from contact,
                              out (1) -> me
        :return:
        """
        driver = self.driver
        driver.implicitly_wait(10)
        if in_or_out == 0:
            mensagens = driver.find_elements_by_class_name('message-in')
        elif in_or_out == 1:
            mensagens = driver.find_elements_by_class_name('message-out')
        else:
            raise IndexError
        insides = []
        for message in mensagens:
            insides = message.find_elements_by_tag_name('span')

        for ins in insides:
            try:
                print(ins.text)
            except AttributeError:
                input('insides is null')

            # [input(i.text) for i in insides]

        # return mensagens

    def procura_new_msg(self):
        # PROCURAR POR MENSAGENS NOVAS PELA class ZKn2B
        # ela é filha da m61XR'
        driver = self.driver
        driver.find_elements_by_class_name('ZKn2B')
        # notificação de mensagem nova

        mensagens = driver.find_elements_by_class_name('_2iq-U')

        [print(m.text) for m in mensagens]
        print('AINDA NÃO PROCURA procura_new_message')

    def get_contatos_nomes(self):
        driver = self.driver
        self.click_elements_by_tt('Nova conversa', tortil='title')
        driver.implicitly_wait(5)
        _only = driver.find_element_by_class_name('_2fpYo')
        contatos_nomes = _only.find_elements_by_css_selector('._3ko75._5h6Y_._3Whw5')
        for cont in contatos_nomes:
            print(cont.text)
        print('NADA CERTO, EM ANDAMENTO')

    def download_midias_audiovisuais(self, qtd):
        """
        :param qtd: n° / cont mais recente para mais antigo
        :return:
        """
        driver = self.driver

        def vai_ou_volta(vv):
            """
            :param vv: 0 -> volta
                       1 -> vai

            :return: usado p/ mídias p/ carregar.
            """

            for e in range(qtd - 1):
                # carrega midias
                driver.implicitly_wait(5)

                try:
                    driver.find_element_by_tag_name('video')
                    sl_t = 5
                except NoSuchElementException:
                    sl_t = 1
                    print('Sleep 1, imagem')

                if vv == 1:
                    # vai até o mais antigo
                    sleep(sl_t)
                    self.send_keys_anywhere(Keys.LEFT)
                elif vv == 0:
                    # volta até o mais recente
                    self.send_keys_anywhere(Keys.RIGHT)
                    sleep(sl_t)
                else:
                    print('\nINVÁLIDO!!')
                    raise IndexError

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

    def whatsapp_DRIVER(self, client=None, padrao=False):
        # ############################################## CUIDADO COM PATH em download X sessão
        """
        :param client: o CLIENTE atual
        :param padrao: \\ path with your QR code for creation only
        :return: o driver para fechar no loop
        """
        link = "Chromedriver/chromedriver.exe"
        chrome_options = Options()
        __padrao = profiles_main_folder()
        # mesma coisa que self.padrao

        if padrao:
            path = padrao
            profile_path = profiles_main_folder()
        else:
            if client is None:
                raise AttributeError
            path = self._files_path_v2(client)
            new_path = '\\'.join(__padrao.split('\\')[:-1])
            profile_path = f'{new_path}\\__PROFILES__\\{str(client)}'
            try:
                # input(profile_path)
                self.full_copy_dir(__padrao, profile_path)
            except FileExistsError:
                print(f'perfil ATUAL já existente, segue o baile, cliente {client}')

        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument(f"user-data-dir={profile_path}")
        # ele cria automático sem problemas...
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
            'profile.default_content_setting_values.automatic_downloads': 1

        })

        chromedriver = link

        driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

        # self.tags_wait('body', 'input', 'div')

        # sleep(5)
        return driver

    def mensagem(self, mensagem, time=7):
        """
        chamada em activate_driver_window
        """
        import tkinter as tk

        class ExampleApp(tk.Tk):
            def __init__(self):
                tk.Tk.__init__(self)
                tk.Label(text=mensagem, pady=10).pack()

                tk.Button(self, text="OK", fg='white', bg='black', command=self.destroy, activeforeground="black",
                          activebackground="green4", pady=10, width=10).pack()

                self.label = tk.Label(self, text="", width=10)
                self.label.pack()
                self.remaining = 0
                self.countdown(time)
                # self.after(time * 1000, lambda: self.destroy())

                self.geometry('500x250+1400+10')

            def countdown(self, remaining=None):
                if remaining is not None:
                    self.remaining = remaining

                if self.remaining <= 0:
                    self.label.configure(text="000000")
                    self.destroy()
                else:
                    self.label.configure(text="%d" % self.remaining)
                    self.remaining = self.remaining - 1
                    self.after(1000, self.countdown)
        print('Mensagem: ', mensagem)
        ExampleApp().mainloop()
