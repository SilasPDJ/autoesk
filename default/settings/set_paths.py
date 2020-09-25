from .now import Now


class SetPaths(Now):
    # Now não está tanto em uso,

    def __get_atual_competencia_file(self):
        return 'get_atual_competencia.txt'

    def files_get_anexos(self, client, file_type='pdf', year=True, upload=False):
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

        compt, excel_file_name = self.compt_and_filename()
        path = self._files_path_v2(client, year=year)

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

    def compt_and_filename(self):
        """
        :return: already set compt and file_names; COMPT e file_names já programados antes vindos de um arquivo
        ##########################################################################
        """

        # compt, excel_file_name = 'biri', 'biri'
        try:
            with open(self.__get_atual_competencia_file(), 'r') as f:
                compt, excel_file_name = f.read().splitlines()

        except FileNotFoundError:
            input('\033[1;31mINPUT line 138 file not existence\033[m')
        finally:
            return compt, excel_file_name

    def __read_with_titlePATH(self, n=-1):
        """
        # not in use here

        :param int n:
        :return:
        """
        f = open('with_titlePATH.txt', 'r')
        a = f.read()
        a = a.split('/')
        if n != 0:
            a = a[:n]
        else:
            a = a[:]
        a = '/'.join(a)
        f.close()
        return a

    def get_atual_competencia(self, m_cont=-1, y_cont=-1, past_only=True, file_type='xlsx'):
        """
        :param int m_cont: quantos meses para trás? (0 atual)
        :param int y_cont: quantos anos para trás?
        :param str file_type:
        :param bool past_only: True -> somente passado (multiplica por -1), False: não faz multiplicação
        :return: competencia & excel_path

        # responsivo, retorna também o caminho e a competencia para a variável PATH de self._files_path_v2

        """
        if m_cont > 0 and past_only:
            m_cont *= -1

        from datetime import datetime as dt
        path = self.__read_with_titlePATH(0)

        mes_atual = dt.now().month

        month = dt.now().month + m_cont
        year = dt.now().year

        if mes_atual < month:
            year -= y_cont
            print('\0331[1;31mNÃO É UM ERRO, a competência é maior do que o mês atual. '
                  f'Logo, vou considerar como sendo ano passado: {year}\033[m')

            # Se a competência for do mês 12

        compt = f'{month:02d}-{year}'
        excel_file_path_updated = r'{}/{}.{}'.format(path, compt, file_type)

        with open(self.__get_atual_competencia_file(), 'w') as f:
            for line in [compt, excel_file_path_updated]:
                f.write(line + '\n')

        return compt, excel_file_path_updated

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
        return returned

    def _files_path_v2(self, pasta_client, year=True):
        """
        :param pasta_client: client_name
        :param year: True -> folder contains year, False -> folder DOES NOT contain year
        :return:
        """
        import os
        compt, excel_file_name = self.compt_and_filename()

        ano = [compt.split(v)[-1] for v in compt if not v.isdigit()]
        ano = ano[0]

        possible_folders = ['G5', 'passa_valor', 'sem_mov', '_Dívidas']
        # preciso melhorar, deixar mais responsivo talvez, porém, ele já tá contando com dívidas e responsivo com anos

        PATH = '/'.join(excel_file_name.split('/')[:-2])
        pasta_client = pasta_client.strip()
        volta = os.getcwd()
        for folder in possible_folders:
            try:
                os.chdir(PATH)
                os.chdir(r'{}'.format(folder))
                if year:
                    os.chdir(r'{}/{}/{}'.format(pasta_client, ano, compt))
                else:
                    os.chdir(r'{}/{}'.format(pasta_client, compt))
                # print('inside _path loop')
                break
            except FileNotFoundError:
                pass

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

    def certif_feito(self, client_name):
        """
        certificado de que está feito
        :param client_name: nome da pasta antes de chegar à competência, vai passar por _files_path_v2
        :return: caminho+ nome_arquivo
        """
        nome_arquivo = f'{client_name}.png'

        try:
            save_path = self._files_path_v2(client_name)
            save = r'{}\\SimplesNacionalDeclarado-{}'.format(save_path, nome_arquivo)
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
        from zipfile import ZipFile
        chdir(full_path)
        ls = listdir()
        for file in ls:
            print('Descompactando, ZIPs e excluíndo-os')
            if file.endswith('.zip'):
                zf = ZipFile(file, mode='r')
                zf.extractall()
                zf.close()
                sleep(5)
                if rm_zip:
                    remove(file)
