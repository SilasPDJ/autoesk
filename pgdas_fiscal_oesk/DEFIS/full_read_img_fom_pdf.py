import os

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from default.webdriver_utilities import *
from default.interact import press_keys_b4, press_key_b4
from default.settings import SetPaths
from default.data_treatment import ExcelToData

from default.webdriver_utilities.pre_drivers import pgdas_driver


class Defis(WDShorcuts, SetPaths, ExcelToData):
    def __init__(self, compt_file=None):
        """
        :param compt_file: from GUI

        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        from default.webdriver_utilities.pre_drivers import pgdas_driver

        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual

        sh_names = ['DEFIS']
        if compt_file is None:
            compt_file = self.compt_and_filename()
            compt, excel_file_name = compt_file
        else:
            compt, excel_file_name = compt_file

        COMPT = compt = f"DEFIS_{self.y()}"
        # transcrevendo compt para que não seja 02/2021

        # excel_file_name = '/'.join(excel_file_name.split('/')[:-1])
        excel_file_name = os.path.dirname(excel_file_name)
        excel_file_name += f'/DEFIS-anual.xlsx'
        pdExcelFile = pd.ExcelFile(excel_file_name)

        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path

            msh = pdExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}

            msh = pdExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            self.after_READ = self.readnew_lista(READ, False)
            after_READ = self.after_READ

            for i, CNPJ in enumerate(after_READ['CNPJ']):
                # ####################### A INTELIGENCIA EXCEL ESTÁ SEM OS SEM MOVIMENTOS NO MOMENTO
                _cliente = after_READ['Razão Social'][i]
                _ja_declared = after_READ['Declarado'][i].upper().strip()
                _cod_sim = after_READ['Código Simples'][i]
                _cpf = after_READ['CPF'][i]
                _cert_or_login = after_READ['CERTORLOGIN'][i]

                # Dirfis exclusivos search
                _dirf_sch = after_READ['DIRF'][i]
                print(_dirf_sch)
                if _cliente == '':
                    break

                if _ja_declared not in ['S', 'OK', 'FORA']:
                    # ############################################################################################ ↓
                    # self.client_path = self._files_path_defis(_cliente, tup_path=(COMPT, excel_file_name))
                    if _dirf_sch == '-' or '-' in _dirf_sch or _dirf_sch.strip() == '':
                        pdf_dirf = False
                    else:
                        self.client_path = self._files_path_defis(_cliente, tup_path=(COMPT, excel_file_name))

                        pdf_dirf = self.os_walk__get_dirfs(_dirf_sch)
                        self.os_walk__get_dirfs(_dirf_sch)
                        __client_path = self.client_path
                        # print(pdf_dirf)
                        if pdf_dirf:
                            for img_file in self.transforma_pdf_em_img(pdf_dirf):
                                # input(__client_path)
                                dale = self.captcha_hacking(img_file)
                                with open(img_file.replace('jpg', 'txt'), 'w') as ftext:
                                    ftext.write(dale)



                    # self.driver = pgdas_driver(__client_path)
                    # driver = self.driver
                    # super().__init__(driver)


    def os_walk__get_dirfs(self, searched_client, searched='Comprovante de rendimento.pdf'):
        """
        :param searched_client: searched_client_path
        :param searched:
        :return:
        """
        INITIAL_PATH = r'I:\OESK_CONTABIL'
        ano_dirf = str(self.y())

        for (dirpath, dirnames, filenames) in os.walk(INITIAL_PATH):
            if ano_dirf in dirnames:
                # get last part of folder name ↓↓↓
                the_client = os.path.basename(os.path.normpath(dirpath))
                if the_client == searched_client:

                    for (dp2, dn2, fn2) in os.walk(dirpath):
                        if ano_dirf in dp2:
                            for dp3, dn3, fn3 in os.walk(dp2):
                                if 'DIRF' in dp3:
                                    for file in os.listdir(dp3):
                                        if file == searched:
                                            # full_file_path
                                            returned = dp3 + f'\\{file}'
                                            break
                                    else:
                                        # full_file_path
                                        returned = False
                                    # now_command = f'explorer {dn2}'
                                    return returned

    def os_walk__get_dirfs_path(self, searched_client=None):
        """
        :param searched_client: None or False => return all paths,
        :return:
        """
        clientes_path = {}

        INITIAL_PATH = r'I:\OESK_CONTABIL'
        ano_dirf = str(self.y())

        for (dirpath, dirnames, filenames) in os.walk(INITIAL_PATH):
            if ano_dirf in dirnames:
                # get last part of folder name ↓↓↓
                the_client = os.path.basename(os.path.normpath(dirpath))
                    # nome tem que ser exato

                for (dp2, dn2, fn2) in os.walk(dirpath):
                    if ano_dirf in dp2:
                        for dp3, dn3, fn3 in os.walk(dp2):
                            if 'DIRF' in dp3:
                                dirf_path = dp3
                                now_command = f'explorer {dp3}'
                                clientes_path[the_client] = dirf_path
                                # call(now_command)
        for klient, vdir in clientes_path.items():
            if klient == searched_client:
                return klient
            yield vdir

    def captcha_hacking(self, img_path):
        """
        :return:
        SbFConverter() -> class called

        Tremembé... rs
        """
        from pyperclip import paste
        # driver = self.driver

        class SbFConverter:
            """
            MUITO OBRIGADO, SENHOR

            # retorna copiada a imagem através do nome dela
            """

            def read(self, img_name):
                # self.convert_gray_scale(img_name)

                import pytesseract
                from PIL import Image
                pytesseract.pytesseract.tesseract_cmd = r"I:\NEVER\tesseract.exe"
                r = img_name
                text = pytesseract.image_to_string(r)
                return text

            def convert_gray_scale(self, img_name):
                img2 = img_name
                from PIL import Image
                # img = Image.open(img2).convert('LA')
                img = Image.open(img2)
                img.convert('RGB')
                img.save(img_name)

        # img = driver.find_element_by_id('div-img-captcha')
        # img_name = 'hacking.png'
        # img.screenshot(img_name)

        nm_img = img_path
        img_name = nm_img
        # VEIO DE ginfess_download
        version2 = SbFConverter()
        # version2.convert_gray_scale(nm_img)
        read = version2.read(nm_img)
        return read

    def transforma_pdf_em_img(self, file):
        import pdf2image

        pages = pdf2image.convert_from_path(file)
        for e_cont, page in enumerate(pages):
            dir_name = self.client_path
            # real = '\\'.join(os.path.realpath(__file__).split('\\')[:-1])
            fnamenow = f'{dir_name}\\pag_{e_cont+1}.jpg'
            page.save(fnamenow, 'JPEG')
            yield fnamenow

# input("\033[1;34mINPUT: FALTA LER O PDF AGORA, FAZENDO O SEU SCRAP\033[m")
Defis()
