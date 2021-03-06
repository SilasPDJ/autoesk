from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from default.webdriver_utilities import *
from default.interact import press_keys_b4, press_key_b4
from default.settings import SetPaths
from default.data_treatment import ExcelToData

from default.webdriver_utilities.pre_drivers import pgdas_driver


class ReadPdf(SetPaths, ExcelToData):

    def captcha_hacking(self, img_path):
        """
        :return:
        SbFConverter() -> class called

        Tremembé... rs
        """
        # driver = self.driver

        class SbFConverter:
            """
            MUITO OBRIGADO, SENHOR

            # retorna copiada a imagem através do nome dela
            """

            def __init__(self, img_name, path=''):
                from pyperclip import copy
                # self.convert_gray_scale(img_name)

                read = self.read(img_name)
                copy(read)

            def read(self, img_name):
                # self.convert_gray_scale(img_name)

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
                # img = Image.open(img2).convert('LA')
                img = Image.open(img2)
                img.convert('RGB')
                img.save(img_name)

        from pyautogui import hotkey
        from pyperclip import paste
        # img = driver.find_element_by_id('div-img-captcha')
        # img_name = 'hacking.png'
        # img.screenshot(img_name)

        nm_img = img_path
        # VEIO DE ginfess)_download
        SbFConverter(nm_img)

        continua = paste()
        return continua


    def transforma_pdf_em_img(self, file):
        import pdf2image

        pages = pdf2image.convert_from_path(file)
        for e_cont, page in enumerate(pages):
            dir_name = self.dir_name
            input(dir_name)
            # real = '\\'.join(os.path.realpath(__file__).split('\\')[:-1])
            page.save(f'{dir_name}\\out-{e_cont}.jpg', 'JPEG')


a = ReadPdf()
a.dir_name = r'I:\OESK_CONTABIL\Rosangela\2021\DIRF\img'
a.transforma_pdf_em_img('I:/OESK_CONTABIL/Rosangela/2021/DIRF/Comprovante de rendimento.pdf')
img = r'I:\OESK_CONTABIL\Rosangela\2021\DIRF\img\out-1.jpg'

# a.captcha_hacking(img)
