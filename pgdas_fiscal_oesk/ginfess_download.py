
from pgdas_fiscal_oesk import WDShorcuts, SetPaths, ExcelToData, Keys
from pgdas_fiscal_oesk import NoSuchElementException, ElementClickInterceptedException, NoAlertPresentException
from default.webdriver_utilities.pre_drivers import ginfess_driver


class DownloadGinfess(WDShorcuts, SetPaths, ExcelToData):
    import pyautogui
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    def __init__(self):
        import pandas as pd
        sh_names = ['G5_ISS']
        compt, excel_file_name = self.get_atual_competencia(1)

        lugar_salvar = ''
        for sh_name in sh_names:
            mshExcelFile = pd.ExcelFile(excel_file_name)

            msh = mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = mshExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            self.after_READ = self.readnew_lista(READ, False)
            after_READ = self.after_READ
            # input(len(after_READ['CNPJ']))

            from os import getcwd, chdir
            volta = getcwd()

            # if ISS in sh:
            for i, valor in enumerate(after_READ['CNPJ']):
                _cnpj = after_READ['CNPJ'][i]
                _ginfess_cod = after_READ['Ginfess Cód'][i]
                _ja_imported = after_READ['g5 import'][i].lower()
                _city = after_READ['CITy'][i]
                # _valor = after_READ['Valor'][i]
                _cliente = after_READ['Razão Social'][i]
                print('~' * 60)
                print(f"""Cliente atual: {_cliente}, 
    com o CNPJ:{_cnpj}; código GINFESS: {_ginfess_cod} -> 
    MUNICÍPIO: {_city}""")
                print('~' * 60)
                client_path = self._files_path_v2(_cliente)
                self.client_path = client_path

                # Checa se já existe certificado
                chdir(volta)
                if _ginfess_cod.lower() == 'não há':
                    # removi o ja_imported
                    print(f'\033[1;31m o cliente {_cliente} não possui notas\n...(muito bom) O certificado anula o _ja_imported...\033[m')
                elif self.check_done(client_path, '.png'):
                    # Checka o certificado ginfess, somente

                    # if city in 'ABC':
                    self.driver = ginfess_driver(self.client_path)
                    super().__init__(self.driver)
                    driver = self.driver

                    id_url = self.id_url(_city)
                    self.driver.get(id_url)
                    #for
                    if _city in ['A', 'B', 'C']:
                        # links das cidades

                        # driver.maximize_window()
                        # #######################################################
                        self.ABC_ginfess(_cnpj, _ginfess_cod, _city)
                        # #######################################################

                        try:
                            # Find existent tags
                            driver.implicitly_wait(5)
                            self.tags_wait('table', 'tbody', 'tr', 'td')

                            print('printscreen aqui')

                            self.download(_cliente)
                            driver.implicitly_wait(5)

                            self.cexcel_from_html_above_v1(_cliente, self.ginfess_table_valores_html_code())
                        except IndexError:
                            print('~' * 30)
                            print('não emitiu nenhuma nota'.upper())
                            print('~' * 30)

                        driver.save_screenshot(self.certif_feito(self.client_path))
                        # coloquei tudo no dele

                    elif _city.upper() == 'TREM':
                        driver.implicity_wait(5)

                        def tag_with_text(tag, searched):
                            td_tag = driver.find_element_by_xpath(f"//{tag}[contains(text(),'{searched.rstrip()}')]")
                            return td_tag

                        zero_um = _ginfess_cod.split('//')

                        self.tags_wait('html')
                        self.tags_wait('body')
                        while True:
                            driver.implicity_wait(5)
                            self.captcha_hacking()
                            ccm = driver.find_element_by_id('ccm')
                            ##
                            ##
                            ccm.send_keys(zero_um[0])
                            self.send_keys_anywhere(Keys.TAB)
                            print(zero_um, 'senha')
                            self.send_keys_anywhere(zero_um[1])

                            self.send_keys_anywhere(Keys.TAB)
                            self.pyautogui.hotkey('ctrl', 'v')
                            driver.implicity_wait(.5)

                            self.send_keys_anywhere(Keys.TAB)
                            self.send_keys_anywhere(Keys.ENTER)
                            if 'login.php' in driver.current_url:
                                driver.refresh()
                                driver.implicity_wait(6)
                            else:
                                break
                        print('break')
                        driver.implicity_wait(4)
                        tag_with_text('td', 'Movimento ').click()

                        for i in range(2):
                            self.send_keys_anywhere(Keys.TAB)
                            self.send_keys_anywhere(Keys.ENTER)
                            if i == 1:
                                driver.find_element_by_id('main').click()
                                break
                            driver.implicity_wait(.25)
                        self.send_keys_anywhere(Keys.TAB)
                        self.send_keys_anywhere(Keys.ENTER)
                        self.send_keys_anywhere(Keys.UP)
                        self.send_keys_anywhere(Keys.ENTER)
                        for i in range(2):
                            self.send_keys_anywhere(Keys.TAB)
                        self.send_keys_anywhere(Keys.ENTER)
                        driver.implicity_wait(3)

                        url = '/'.join(driver.current_url.split('/')[:-1])
                        # separa_url embutido, falta o login_pass

                        # driver.get(f'{url}/dmm/_menu.php')
                        """kk"""
                        driver.get(f'{url}/nfe/nfe_historico_exportacao.php')
                        driver.implicity_wait(3)
                        self.tags_wait('html')
                        self.tags_wait('body')

                        driver.implicity_wait(2)
                        driver.find_element_by_id('todos').click()
                        driver.find_element_by_id('btnExportar').click()
                        driver.switch_to.alert.accept()
                        self.download(_city)

                        path_zip = client_path
                        print(f'path_zip-> {path_zip}')
                        self.unzipe_file(path_zip)

                        driver.save_screenshot(self.certif_feito(self.client_path))
                        # coloquei tudo no deli
                    driver.close()

    def id_url(self, city):
        """
        :param city: Retorna o URL com os links distintos
        :return:
        """
        # id_url = read_excel.id_url(city)
        cities = "Trem", "A", "B", "C", "SP"
        urls = 'https://tremembe.sigiss.com.br/tremembe/contribuinte/login.php', \
               'https://santoandre.ginfes.com.br/', 'https://nfse.isssbc.com.br/', 'https://saocaetano.ginfes.com.br/', \
               'https://nfe.prefeitura.sp.gov.br/login.aspx'
        ind = cities.index(city)
        print(city)
        return urls[ind]

    def ABC_ginfess(self, __cnpj, __senha, city):

        driver = self.driver

        def label_with_text(searched):
            label = driver.find_element_by_xpath(f"//label[contains(text(),'{searched.rstrip()}')]")
            return label

        def button_with_text(searched):
            bt = driver.find_element_by_xpath(f"//button[contains(text(),'{searched.rstrip()}')]")
            return bt

        def a_with_text(searched):
            link_tag = driver.find_element_by_xpath(f"//a[contains(text(),'{searched.rstrip()}')]")
            return link_tag

        def wait_main_tags():
            self.tags_wait('body', 'div', 'table')

        wait_main_tags()
        """ ~~~~~~~~~~~~~~~~~~~~~~ GLÓRIA A DEUS ~~~~~~~~~~~~~~~~~~"""
        name_c = 'gwt-DialogBox'

        self.del_dialog_box(name_c)

        wait_main_tags()
        self.tags_wait('img')
        driver.implicitly_wait(10)

        try:
            try:
                button_with_text('OK').click()
            except (NoSuchElementException, ElementClickInterceptedException):
                pass
            driver.find_element_by_xpath('//img[@src="imgs/001.gif"]').click()
        except (NoSuchElementException, ElementClickInterceptedException):
            pass
        name_c = 'x-window-dlg', 'ext-el-mask', 'x-shadow'
        try:
            for name in name_c:
                try:
                    self.del_dialog_box(name)
                except NoSuchElementException:
                    print('Except dentro do except e no for, [linha 310]')
                    ...
                driver.implicitly_wait(5)
            button_with_text('OK').click()
        except (NoSuchElementException, ElementClickInterceptedException):
            print('Sem janela possivel, linha 246')
            # driver.execute_script('window.alert("Não foi possível prosseguir")')

        driver.implicitly_wait(5)
        """ ~~~~~~~~~~~~~~~~~~~~~~ GLÓRIA A DEUS ~~~~~~~~~~~~~~~~~~"""

        # print('mandando teclas...')
        label_with_text("CNPJ:").click()
        self.send_keys_anywhere(__cnpj)
        passwd = driver.find_element_by_xpath("//input[@type='password']")

        self.tags_wait('body', 'img')
        passwd.clear()
        passwd.send_keys(__senha)
        button_with_text("Entrar").click()

        # tratando atualiza dados
        driver.implicitly_wait(15)
        try:
            wait_main_tags()
            button_with_text('X').click()
            button_with_text('X').click()
            print('CLICADO, X. Linha 263')
        except (NoSuchElementException, ElementClickInterceptedException):
            print('Tentando atualizar os dados')

        a_with_text("Consultar").click()

        print('Waiting main tags')
        wait_main_tags()

        period = label_with_text('Período')
        period.click()
        driver.implicitly_wait(5)
        de = label_with_text('De:')
        de.click()
        self.send_keys_anywhere(Keys.BACKSPACE, 10)
        write = self.date_for_ginfess(0) # data inicial

        self.send_keys_anywhere(write)
        self.send_keys_anywhere(Keys.TAB)

        write = self.date_for_ginfess(1)  # data inicial
        self.send_keys_anywhere(write)

        button_with_text("Consultar").click()
        wait_main_tags()
        driver.implicitly_wait(10)

    def date_for_ginfess(self, tildelta=0):
        """
        :param tildelta: quantidade de dias a retroceder acima de 0

        # 0 -> primeiro dia do mês
        # 1 -> último dia do mês

        #  date for ginfess
        # Chamada por ABC_ginfess_somente
        """
        from datetime import datetime as dt
        from datetime import date as date
        from datetime import timedelta as timedelta
        ano = dt.now().year
        mes = dt.now().month

        # mes = 3

        if tildelta == 0:
            # se for o PRIMEIRO dia do mês...
            mes -= 1
        else:
            ...

        lastnow = date(ano, mes, 1) - timedelta(days=tildelta)
        returned = str(lastnow).replace('-', '')
        # print(ano, mes)
        will_be = ''
        for i in range(len(returned) - 1, -0, -2):
            # print(returned[i-1], end='')
            will_be += returned[i - 1]

            i2 = i + 1
            # print(returned[i2-1], end='')
            will_be += returned[i2 - 1]

        final = ''
        for e, complement in enumerate(will_be):
            # 01052020
            if e in (2, 4):
                final += '/'
            final += complement

        will_be = final
        return will_be

    def download(self, city):
        """
        :city:
        :return:
        """
        driver = self.driver

        if city.strip().lower() not in ('trem', 'sp'):
            try:
                downloada_xml = driver.find_element_by_xpath('//img[@src="imgs/download.png"]')
                downloada_xml.click()

            except NoSuchElementException:
                print('NÃO CONSEGUI FAZER DOWNLOAD...')
        else:
            if driver.current_url.lower() in 'sigiss':
                pass

    def ginfess_table_valores_html_code(self):
        """
        :return: (html_cod): código dele se existe a class ytb-text, scrap_it
        """
        driver = self.driver

        max_value_needed = driver.find_elements_by_class_name('ytb-text')
        max_value_needed = max_value_needed[1].text[-1]
        print(max_value_needed)
        self.tags_wait('input', 'body')

        cont_export = 1

        xml_pages = driver.find_element_by_xpath('//input[@class="x-tbar-page-number"]')
        driver.implicitly_wait(5)
        number_in_pages = xml_pages.get_attribute('value')

        html_cod = """           
                    <style>/*.detalheNota:after{background: red; content: 'cancelada';}*/
                    .notaCancelada{
                    background: red
                    }
                    </style>
                   """.strip()
        pasta_a_salvar = 'G5'

        for i in range(10):
            print(number_in_pages)
            xml_pages.send_keys(Keys.BACKSPACE)
            xml_pages.send_keys(cont_export)

            xml_pages.send_keys(Keys.ENTER)
            driver.implicitly_wait(5)
            print('CALMA...')
            cont_export += 1
            number_in_pages = xml_pages.get_attribute('value')

            # // div[ @ id = 'a'] // a[ @class ='click']

            wanted_wanted = driver.find_elements_by_xpath("//div[contains(@class, 'x-grid3-row')]")
            print(wanted_wanted[0].text)
            # table = wanted_wanted

            for w in wanted_wanted:
                # w.click()
                print(w.text)
                html_cod += w.get_attribute('innerHTML')
                # sleep(2)
            # XML_to_excel.ginfess_scrap()
            if int(cont_export) == int(max_value_needed) + 1:
                break
            print('breakou')

            print('~~~~~~~~')
        return html_cod
        # de.send_keys(Keys.TAB)

    def cexcel_from_html_above_v1(self, cliente, html_codigo):
        # # DEPOIS JUNTAR ELA COM GINFESS_SCRAP
        import os
        import pyautogui as pygui
        from pyperclip import paste, copy
        from .retornot import RetidosNorRetidos, RnrSo1
        from .ginfess_scrap import cria_site_v1
        from time import sleep
        """
         :param cliente: nome do cliente vindo do loop
         :param competencia: vindo do GINFESS_download na linha 37
         :param site_cria: (lugar_salvar)
         :return: return_full_path for with_titlePATH.txt
         """
        if self.client_path is not None:
            client_path = self.client_path
        else:
            client_path = self._files_path_v2(cliente)
        driver = self.driver

        qtd_nf = driver.find_element_by_class_name('x-paging-info')
        qtd_text = qtd_nf.text
        proc = qtd_text.index('of')
        pal = qtd_text[proc:].split()
        qtd_text = pal[1]
        prossigo = cria_site_v1(html_codigo, qtd_text)
        _prossigo = prossigo[0]
        len_tables = prossigo[1]
        # input(f'{prossigo}, {len_tables}, {_prossigo}')
        sleep(5)
        from openpyxl import Workbook
        if _prossigo:
            arq = f'relação_notas_canceladas-{cliente}.xlsx'
            x, y = pygui.position()
            arq = f'{client_path}/{arq}' if '/' in client_path else f'{client_path}\\{arq}'
            # not really necessary, but i want to
            try:
                wb = Workbook()
                sh_name = client_path.split('/')[-1] if '\\' not in client_path else client_path.split('\\')[-1]
                ws1 = wb.create_sheet(sh_name)
                wb.remove(wb['Sheet'])
                wb.save(arq)
            except FileExistsError:
                pass

            finally:
                # ########## ABRINDO EXCEL ####### #
                program = arq.split('_')[-1]
                """~~~~"""
                os.startfile(arq)
                """~~~~"""
                sleep(12)

                allin = pygui.getAllWindows()
                for e, l in enumerate(allin):
                    if program in l.title.lower():
                        l.restore()
                        l.activate()
                        l.maximize()

                # ########## ABRINDO #########
                sleep(6)
                if len_tables > 1:
                    RetidosNorRetidos()
                # input('RETIDOS N RETIDOS')
                    pygui.hotkey('alt', 'f4')
                    sleep(5)
                    pygui.hotkey('enter')
                # from RETIDOS_N_RETIDOS import save_after_changes
                else:
                    RnrSo1()
                    print(f'Testado, len tables = {len_tables}')

    def check_done(self, save_path, file_type):
        """
        :param save_path: lugar que checka tipo de arquivo
        :param file_type: extension
        :return:
        """
        from os import listdir

        for file in listdir(save_path):
            print(file)
            if file.endswith(file_type):
                print('CERTIFICADO EXISTENTE, NÃO PROSSEGUE')
                return False

        print('\033[1;35mPROSSEGUE\033[m')
        return True

    def captcha_hacking(self):
        """
        :param driver:
        :return:
        SbFConverter() -> class called

        Tremembé... rs
        """
        driver = self.driver
        class SbFConverter:
            """
            MUITO OBRIGADO, SENHOR

            # retorna copiada a imagem através do nome dela
            """

            def __init__(self, img_name, path=''):
                from pyperclip import copy
                self.convert_gray_scale(img_name)

                read = self.read(img_name)
                copy(read)

            def read(self, img_name):
                self.convert_gray_scale(img_name)

                import pytesseract
                from PIL import Image
                pytesseract.pytesseract.tesseract_cmd = r"I:\NEVER\tesseract.exe"
                r = img_name
                text = pytesseract.image_to_string(r)
                print(text)
                return text

            def convert_gray_scale(self, img_name):
                img2 = img_name
                from PIL import Image
                img = Image.open(img2).convert('LA')
                img.save(img_name)

        from pyautogui import hotkey
        from pyperclip import paste
        img = driver.find_element_by_id('div-img-captcha')
        img_name = 'hacking.png'
        img.screenshot(img_name)
        SbFConverter(img_name)

        continua = paste()
        if not str(continua).isnumeric():
            driver.get(driver.current_url)