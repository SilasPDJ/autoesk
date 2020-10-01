from default.settings.set_paths import SetPaths
from tkinter import filedialog
from tkinter import Tk
from tkinter import messagebox


class SheetPathManager:
    from default.settings import SetPaths
    import os
    compt_and_filename = SetPaths().compt_and_filename()

    def __init__(self, w_path_file):
        self.compt_and_filename = self.SetPaths().compt_and_filename()
        if w_path_file is not None:
            self.w_path_file = w_path_file
        "# static methods"

    def select_sheets_path_if_not_exists(self):
        root = Tk()
        root.withdraw()
        root = Tk()
        root.withdraw()

        way = None
        while way is None:
            way = filedialog.askdirectory(title='SELECIONE ONDE ESTÃO SUAS PLANILHAS')
            if len(way) <= 0:
                way = None
                resp = messagebox.askokcancel('ATENÇÃO!', message='Favor, selecione uma pasta ou clique em CANCELAR.')
                if not resp:
                    break
            else:
                wf = open(self.w_path_file, 'w')
                wf.write(way)
                root.quit()
                break

    def new_xlsxcompt_from_padrao_if_not_exists(self):
        """
        :return: CREATE XLSX FILE IF NOT EXISTS
        """
        compt, excel_file_name = self.compt_and_filename
        from pandas import read_excel
        plan = 'default_oesk'

        default_file = excel_file_name.replace('\\', '/')
        default_file = default_file.split('/')[:-1]
        default_file = '/'.join(default_file) + f'/{plan}.xlsx'

        try:
            read_excel(default_file)
            try:
                read_excel(excel_file_name)
            except FileNotFoundError:
                from shutil import copy2

                copy2(default_file, excel_file_name)

        except FileNotFoundError:
            raise FileNotFoundError(f'plan="{plan}" file não existente')

    @staticmethod
    def save_after_changes():
        from shutil import copy2
        import os
        self = SheetPathManager(None)
        compt, excel_file_name = self.compt_and_filename

        os.system(r'C:\_SIMPLES\MEXENDO.xlsx')

        copy2(r'C:\_SIMPLES\MEXENDO.xlsx', excel_file_name)
