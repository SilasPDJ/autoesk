class ExcelToData:
    def le_excel_each_one(self, msh):
        # msh = sheet_name inside sheet file
        dict_written = {}
        for en, header in enumerate(msh.columns):
            title = msh[header].name

            dict_written[title] = []
            # dicionário sh_name tem o  dicionário title que tem a lista com os valores, muito bom

            """
            try:
                list_written[title] = []
            except KeyError:
                ...
            """
            r_soc = msh[header].values
            # if title == "Razão Social":
            for name in r_soc:
                dict_written[title].append(name)
        return dict_written

    def readnew_lista(self, READ, print_values=False):
        """ TRANSFORMO EM DICIONÁRIO, CONTINUAR"""
        get_all = {}
        new_lista = []
        for k, lista in READ.items():
            for v in lista:
                v = str(v)
                v = v.replace(u'\xa0', u' ')
                v = v.strip()
                if str(v) == 'nan':
                    v = ''
                new_lista.append(v)
            get_all[k] = new_lista[:]
            new_lista.clear()
        if print_values:
            for k, v in get_all.items():
                print(f'\033[1;32m{k}')
                for vv in v:
                    print(f'\033[m{vv}')
        return get_all

    def trata_money_excel(self, faturado):
        try:
            faturado = f'{float(faturado):,.2f}'
        except ValueError:
            print('Já é string')
        finally:
            faturado = faturado.lower().strip()
            if 'nan' in faturado or 'zerou' in faturado:
                faturado = 'SEM VALOR DECLARADO'
                return faturado
            faturado = faturado.replace('.', 'v')
            faturado = faturado.replace(',', '.')
            faturado = faturado.replace('v', ',')
            return faturado

    @staticmethod
    def any_to_str(*args):
        for v in args:
            yield "".join(v)

