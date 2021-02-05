from .now import Now


class SetPaths(Now):
    # the class Now IS NOT large

    def __get_atual_competencia_file(self):
        import os

        f = '\\get_atual_competencia.txt'
        dir_only = os.path.dirname(__file__)
        project_dir = '\\'.join(dir_only.split('\\')[:-2])
        # Contar de trás pra frente, pois vai que um dia eu coloque ele num diretorio raiz

        tot = project_dir + f
        return tot

    def files_get_anexos(self, client, file_type='pdf', upload=False):
        """
        :param client: nome da pasta onde estão os arquivos organizados por data dd-mm-yyyy
        :param year: True -> folder contains year, False -> folder DOES NOT contain year
        :param file_type: file annexed type
        :param upload: False -> email it! True: upload it!
        :return: pdf_files or whatever

        # _files_path
        """
        import os
        from email.mime.application import MIMEApplication

        # compt, excel_file_name = self.compt_and_filename()
        compt_and_file = self.compt_and_filename()
        path = self._files_path_v3(client, wexplorer_tup=compt_and_file)
        # print(path, '\nPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATH', year)
        volta = os.getcwd()

        os.chdir(path)

        list_returned = os.listdir()
        pdf_files = list()

        for fname in list_returned:
            if fname.lower().endswith(f'.{file_type}'):
                if not upload:
                    file_opened = MIMEApplication(open(fname, 'rb').read())
                    file_opened.add_header('Content-Disposition', 'attachment', filename=fname)
                    pdf_files.append(file_opened)
                else:
                    pdf_files.append(f'{os.getcwd()}\\{fname}')
        os.chdir(volta)
        print(os.getcwd())
        return pdf_files

    def files_get_anexos_v2(self, client, file_type='pdf', wexplorer_tup=None, upload=False):
        """
        :param client: nome da pasta onde estão os arquivos organizados por data dd-mm-yyyy
        :param file_type: file annexed type
        :param wexplorer_tup: ... ctrl+F me
        :param upload: False -> email it! True: upload it!
        :return: pdf_files or whatever

        # _files_path
        """
        import os
        from email.mime.application import MIMEApplication

        # compt, excel_file_name = self.compt_and_filename()
        if wexplorer_tup is None:
            compt_and_file_anexos = self.compt_and_filename()
        else:
            compt_and_file_anexos = wexplorer_tup
        path = self._files_path_v3(client, wexplorer_tup=compt_and_file_anexos)
        # print(path, '\nPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATH', year)
        volta = os.getcwd()

        os.chdir(path)

        list_returned = os.listdir()
        pdf_files = list()

        for fname in list_returned:
            if fname.lower().endswith(f'.{file_type}'):
                if upload:
                    file_opened = MIMEApplication(open(fname, 'rb').read())
                    file_opened.add_header('Content-Disposition', 'attachment', filename=fname)
                    pdf_files.append(file_opened)
                else:
                    pdf_files.append(f'{os.getcwd()}\\{fname}')
        os.chdir(volta)
        print(os.getcwd())
        return pdf_files

    def compt_and_filename(self):
        """
        :return: already set compt and file_names; COMPT e file_names já programados antes vindos de um arquivo
        ##########################################################################
        """
        from time import sleep
        # compt, excel_file_name = 'biri', 'biri'
        try:
            sleep(1)
            with open(self.__get_atual_competencia_file(), 'r') as f:
                compt, excel_file_name = f.read().splitlines()

        except FileNotFoundError:
            # raise FileNotFoundError('\033[1;31mfile not existence\033[m')

            return self.set_get_compt_file(m_cont=-1)
        else:
            return compt, excel_file_name

    def file_wtp_only1(self):
        import os
        filepath = os.path.realpath(__file__)
        os.path.join('\\'.join(filepath.split('\\')[:-1]))
        file_with_name = 'with_titlePATH.txt'
        try:
            f = open(f'{file_with_name}', 'r')
            a = f.read()
            a = a.split('/')
            a = '/'.join(a)
            returned = a
            f.close()
        except FileNotFoundError:
            FileExistsError('WITH TITLE PATH NOT EXISTENTE ')
            returned = self.select_sheets_path_if_not_exists()

        return returned

    def select_sheets_path_if_not_exists(self):
        from tkinter import Tk, filedialog, messagebox
        root = Tk()
        root.withdraw()
        root = Tk()
        root.withdraw()

        file_with_name = 'with_titlePATH.txt'
        # sh_management = SheetPathManager(file_with_name)

        way = None
        while way is None:
            way = filedialog.askdirectory(title='SELECIONE ONDE ESTÃO SUAS PLANILHAS')
            if len(way) <= 0:
                way = None
                resp = messagebox.askokcancel('ATENÇÃO!', message='Favor, selecione uma pasta ou clique em CANCELAR.')
                if not resp:
                    break
            else:
                wf = open(file_with_name, 'w')
                wf.write(way)
                root.quit()
                return way

    def set_get_compt_file(self=None, m_cont=0, y_cont=0, past_only=True, file_type='xlsx', open_excel=False):
        """
        :param int m_cont: quantos meses para trás? (0 atual)
        :param int y_cont: quantos anos para trás?  (0 atual)
                :param bool past_only: True -> somente passado (multiplica por -1), False: não faz multiplicação
        :param any file_type: None -> (((DOES NOTHING))) update self.__get_atual_competencia_file
        :param open_excel: if True => OPENS EXCEL FILE
        :return: competencia & excel_path

        # responsivo, retorna também o caminho e a competencia para a variável PATH de self._files_path_v2

        """
        compt = self.get_compt_only(m_cont, y_cont, past_only)

        path = self.file_wtp_only1()

        # é o mesmo do de cima, mas to tentando
        if file_type:
            excel_file_path_updated = r'{}/{}.{}'.format(path, compt, file_type)
            with open(self.__get_atual_competencia_file(), 'w') as f:
                for line in [compt, excel_file_path_updated]:
                    # print(compt)
                    f.write(line + '\n')
            if open_excel:
                from pgdas_fiscal_oesk.main_excel_manager.main_excel_manager import SheetPathManager
                spm = SheetPathManager()
                spm.new_xlsxcompt_from_padrao_if_not_exists((compt, excel_file_path_updated))
                spm.save_after_changes((compt, excel_file_path_updated))

            return compt, excel_file_path_updated
        return compt

    def get_compt_only(self, m_cont=-1, y_cont=0, past_only=True, sep='-'):
        from datetime import datetime as dt
        from datetime import date, timedelta
        from dateutil.relativedelta import relativedelta

        month = dt.now().month
        year = dt.now().year

        now_date = date(year, month, 1)

        if past_only:
            m_cont = m_cont * (-1) if m_cont > 0 else m_cont
            y_cont = y_cont * (-1) if y_cont > 0 else y_cont
            # force to be negative

        now_date = now_date + relativedelta(months=m_cont)
        now_date = now_date + relativedelta(years=y_cont)
        month, year = now_date.month, now_date.year
        compt = f'{month:02d}{sep}{year}'
        return compt

    # @staticmethod
    def get_last_business_day_of_month(self, month=None, year=None):

        from calendar import monthrange
        from datetime import datetime
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year

        init = monthrange(year, month)
        ultimo_day = init[1]
        business_date = datetime(year, month, ultimo_day)

        weekday = business_date.weekday()
        while weekday > 4:
            now_day = business_date.day
            business_date = business_date.replace(day=now_day - 1)
            weekday = business_date.weekday()
        returned = business_date.day

        returned -= 1 if month == 12 else returned
        return returned

    def first_and_last_day_compt(self, sep='/'):
        """
        ELE JÁ PEGA O ANTERIOR MAIS PROX

        # É necessario o will_be pois antes dele é botado ao contrário
        # tipo: 20200430
        # ano 2020, mes 04, dia 30... (exemplo)
        :return: ÚLTIMO DIA DO MES
        """
        from datetime import date, timedelta
        from dateutil.relativedelta import relativedelta

        compt, file_name = self.compt_and_filename()
        mes, ano = compt.split('-') if '-' in compt else '/'
        mes, ano = int(mes), int(ano)

        #  - timedelta(days=1)
        # + relativedelta(months=1)

        last_now = date(ano, mes, 1) + relativedelta(months=1)
        last_now -= timedelta(days=1)
        first_now = date(ano, mes, 1)

        z, a = last_now, first_now
        br1st = f'{a.day:02d}{sep}{a.month:02d}{sep}{a.year}'
        brlast = f'{z.day:02d}{sep}{z.month:02d}{sep}{z.year}'
        print(br1st, brlast)
        return br1st, brlast

    def _files_path_v3(self, pasta_client, wexplorer_tup=None):
        """
        :param pasta_client: client_name
        :param year: True -> folder contains year, False -> folder DOES NOT contain year
        :param wexplorer_tup: the tuple containing the self.compt_and_file_name()
        :return: salva_path (save_path)
        """
        import os
        if wexplorer_tup is None:
            compt, excel_file_name = self.compt_and_filename()
        else:
            compt, excel_file_name = wexplorer_tup
        ano = [compt.split(v)[-1] for v in compt if not v.isdigit()]
        ano = ano[0]

        possible_folders = ['_Dívidas']
        # preciso melhorar, deixar mais responsivo talvez, porém, ele já tá contando com dívidas e responsivo com anos

        PATH = '/'.join(excel_file_name.split('/')[:-2])
        pasta_client = pasta_client.strip()
        volta = os.getcwd()

        for acp in [PATH, ano, compt, pasta_client]:
            try:
                os.chdir(acp)
            except FileNotFoundError:
                os.mkdir(acp)
                os.chdir(acp)

        salva_path = os.getcwd()
        # print(salva_path)
        os.chdir(volta)
        return salva_path

    def mkdir_hoje(self, und_disco, relative_path=None):
        """
        :param und_disco: A, B, C, D, E, F, G, H, I, J, K ... ETC
        :param relative_path: path/b_path/c_path
        :return: folder de hoje criado com o caminho relativo sem ficar sobreposto
        """

        date_folder = f'{self.hj()}-{self.m():02d}-{self.y()}'
        if len(und_disco) > 1:
            print('Digite somente a letra da unidade de disco')
            raise AttributeError
        if relative_path is not None:
            if '/' == relative_path[0] or '/' == relative_path[-1]:
                print('Não use "/" nem "\\" em path[0] or path[-1]')
                raise AttributeError
            res = self.__new_path_set(f'{und_disco}:/{relative_path}/{date_folder}')
        else:
            res = self.__new_path_set(f'{und_disco}:/{date_folder}')
        return res

    def move_file(self, where_from, destiny):
        """
        :param where_from: where the files come from
        :param destiny: where they're going to
        :return: File moved from a place[where_from] to another[destiny]
        """
        from shutil import move
        move(where_from, destiny)

    def __new_path_set(self, path=''):
        """
        :param path: default path atual (downloads)
        :return: Se caminho não criado, ele cria

        # até agora chamado somente por mkdir_hoje

        """

        import os
        volta = os.getcwd()

        if '/' in path:
            spliter = '/'
        elif '\\' in path:
            spliter = '\\'
        else:
            spliter = ''
            print(path)
            raise AttributeError
        try:
            und_disco = path.split('/')[0]
        except (IndexError, AttributeError) as e:
            raise e
        else:
            os.chdir(und_disco)

        pnow = os.getcwd()[:-1]
        for folder in path.split(spliter)[1:]:
            pnow = f'{pnow}/{folder}'

            if not os.path.exists(pnow):
                os.mkdir(folder)
            os.chdir(folder)
            # print('NOTHING went wrong')

        os.chdir(volta)

        return path

    def certif_feito(self, save_path, add=''):
        """
        certificado de que está feito
        :param save_path: nome da pasta vinda de _files_path_v2
        :param add: um adicional no nome do arquivo
        :return: caminho+ nome_arquivo jpeg
        """
        client_name = save_path[save_path.index('-')-2: save_path.index('-')+2]
        type_arquivo = 'png'
        try:
            save = r'{}\\{}-SimplesNacionalDeclarado.{}'.format(save_path, add, type_arquivo)
            print(save, '---------> SAVE')
            return save
        except FileNotFoundError:
            print('NÃO CONSEGUI RETORNAR SAVE')

    def unzipe_file(self, full_path, rm_zip=True):

        """
        :param full_path: caminho
        :param rm_zip: True -> remove zip, False, não remove
        :return: arquivo extraído e excluído o zip.
        Ele faz isso com todos os zip
        """
        from time import sleep
        from os import chdir, remove, listdir
        from zipfile import ZipFile, BadZipFile
        chdir(full_path)
        ls = listdir()
        for file in ls:
            print('Descompactando, ZIPs e excluíndo-os')
            if file.endswith('.zip'):
                try:
                    zf = ZipFile(file, mode='r')
                    zf.extractall()
                    zf.close()
                except BadZipFile:
                    print('Não deszipei')
                finally:
                    if rm_zip:
                        sleep(5)
                        remove(file)
