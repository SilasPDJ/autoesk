def tres_valores_faturados(path, excel_type='xlsx'):
    import os

    def pandas(filepath):

        def treatment(lis):
            key, value = '', ''
            for ll in lis[0]:
                ll = str(ll)
                if ll != 'nan':
                    try:
                        if ll == '0':
                            value = '0'
                        if float(ll):
                            value = ll

                    except ValueError:
                         if '.' not in ll:
                            key = ll
            return {f'{key}': value}

        # panda dream

        print(filepath)
        import pandas as pd
        df = pd.read_excel(filepath, dtype=str)

        tot, ret, n_r = df[-3:-2].values.tolist(), df[-2:-1].values.tolist(), df[-1:].values.tolist()
        tot, ret, n_r = treatment(tot), treatment(ret), treatment(n_r)

        returned = tot, ret, n_r
        print(returned)
        # print(df._slice(slice(4, 5)))
        # print()
        # print(df._slice(slice(0, 2)))
        # print(df._slice(slice(0, 2), 1))
        return returned

    volta = os.getcwd()
    excel_path = False
    try:
        os.chdir(path)
        dirs = os.listdir()
        for file in dirs:
            # print(file)
            if file.endswith(excel_type):
                if file.startswith('relação_notas_canceladas'):
                    print('relação_notas_canceladas starts with')
                excel_path = os.getcwd()
                excel_path += f'\\{file}'
        if excel_path:
            will_return = pandas(excel_path)
            print(will_return)
        else:
            will_return = False

        os.chdir(volta)
        return will_return

    except (IndexError, MemoryError):
        print(f'\033[1;33m'
              f'Deve ser o Daniel ou o Murilo, corrigir o GINFESS_download. Ler whatsapp\033[m'
              f'\n: {path}')
        print('Almeida sempre tem movimento<-')
        return False


def TresValoresFaturados_GUI(client=''):
    def _path(pasta_client):
        folders = ['G5', 'passa_valor', 'sem_mov']
        """
        :param pasta_client: client_name
        :param place_to_save: G5, sem_mov etc
        :return:
        """
        import os
        from datetime import datetime as dt
        ano = dt.now().year
        mes = dt.now().month
        competencia = f'{mes-1:02d}-{ano}'
        volta = os.getcwd()
        try:
            file = open('with_titlePATH.txt', 'r')
        except FileNotFoundError:
            file = open('../with_titlePATH.txt', 'r')
        PATH = file.read()
        # input(PATH)

        for folder in folders:
            try:
                os.chdir(PATH)
                os.chdir(r'../{}'.format(folder))
                os.chdir(r'{}/{}/{}'.format(pasta_client, ano, competencia))
                # print('inside _path loop', folder)
                break
            except FileNotFoundError:
                pass
        dirs = os.listdir()
        # [print(f'\033[1;31m{d}\033[m') for d in dirs]

        r = False
        for file in dirs:
            # print(file)

            if file.endswith('.xlsx') or file.endswith('.xls'):

                salva_path = os.getcwd()
                salva_path += f'\\{file}'
                os.chdir(volta)
                return salva_path

        os.chdir(volta)
        return r

    def pandas(path_xlsx):

        def treatment(lis):
            key, value = '', ''
            for ll in lis[0]:
                ll = str(ll)
                if ll != 'nan':
                    try:
                        if ll == '0':
                            value = '0'
                        if float(ll):
                            value = ll

                    except ValueError:
                         if '.' not in ll:
                            key = ll
            return {f'{key}': value}

        # panda dream
        # print(path)
        import pandas as pd
        df = pd.read_excel(path_xlsx, dtype=str)

        tot, ret, n_r = df[-3:-2].values.tolist(), df[-2:-1].values.tolist(), df[-1:].values.tolist()
        tot, ret, n_r = treatment(tot), treatment(ret), treatment(n_r)

        returned = tot, ret, n_r
        # print(returned)
        # print(df._slice(slice(4, 5)))
        # print()
        # print(df._slice(slice(0, 2)))
        # print(df._slice(slice(0, 2), 1))
        return returned

    path = _path(client)
    if not path:
        return False
    else:
        try:
            will_return = pandas(path)
            # input(will_return)
            return will_return
        except (IndexError, MemoryError):
            print(f'\033[1;33m'
                  f'Deve ser o Daniel ou o Murilo, corrigir o GINFESS_download. Ler whatsapp\033[m'
                  f'\nclient: {client}')
            print('Almeida sempre tem movimento<-')


# c = 'Cyclo Aguas do Brasil LTDA'
# a = 'Almeida Rocha Gerenciamento Administrativo LTDA'
# d = 'Daniel Roberto Rodrigues Nantes Santos Hoffen Consultoria em Tecnologia da Informacao'
# Main(d)