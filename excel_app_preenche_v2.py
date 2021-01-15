import win32com.client as win32
from pyperclip import paste
from itertools import count
import os

from default.settings import SetPaths


def first():
    xl = win32.gencache.EnsureDispatch('Excel.Application')
    xl.Visible = True
    ss = xl.Workbooks.Add()
    wb = ss.ActiveSheet
    ActiveSheet = wb
    ActiveSheet.Cells(5, 4).Select()


def npl(letra):
    # npl = numero_pra_letra
    letra = letra.upper()
    letras = tuple(range(97, 123))
    # letras = (chr(l).upper() for l in letras)
    # [] ou ()...
    # return [letras for l in letras if l == letra]
    letras = [chr(l).upper() for l in letras]
    default_letras = letras.copy()

    letters3cols = False
    # Se contem 3 colunas...
    for l1 in default_letras:
        for l2 in default_letras:
            letras.append(f'{l1}{l2}')
            try:
                return [letras.index(lett)+1 for lett in letras if lett == letra][0]
            except IndexError:
                letters3cols = True
                # Funciona, testado com AB. Procura até achar e retornar index
    if letters3cols:
        for l1 in default_letras:
            for l2 in default_letras:
                for l3 in default_letras:
                    letras.append(f'{l1}{l2}{l3}')
                    try:
                        return [letras.index(lett)+1 for lett in letras if lett == letra][0]
                    except IndexError:
                        pass
                    # Funciona, testado com AAA. Procura até achar e retornar index


def rowcalc(where:str, rowcont:int):
    wherenum = int(where[-2:]) + rowcont
    where = where[:-2]+str(wherenum)
    return where


def not_used_get_values_range(rng, filename):
    param1selection = None
    w3c = win32
    xlapp = w3c.Dispatch('Excel.Application')
    # xlwb = xlapp.Workbooks.Open('C:/_SIMPLES/MEXENDO.xlsx', True, True, None)
    # somente leitura
    wb = xlapp.Workbooks.Open(filename)
    AS = wb.ActiveSheet
    for cont, row in enumerate(AS.Range(rng)):
        # AS = wb.ActiveSheet
        """
        Estou num range... Estou selecionando e copiando/colando os valores dele
        row.Address
        legal
        """
        if cont == 1:
            param1selection = row.Address

        razao_social = row.Value
        if row.Value is not None:
            # print(row.Row)
            selection1_val2 = row.Address
            # print(selection1_val2)
        else:
            param2selection = row.Address

            razoes_sociais = AS.Range(f'{param1selection}:{rowcalc(param2selection, -1)}')
            # razoes_sociais.Select()
            valores = razoes_sociais.Copy()
            return paste()


# row.Value, row.Row, row.Column, row.Address


class VbaUtilities(SetPaths):
    # ainda não vou usar o próprio, vou usar o mexendo
    # filename = 'C:/_SIMPLES/MEXENDO.xlsx'
    DIZPEXCEL = win32.Dispatch('Excel.Application')
    DIZPEXCEL.Visible = True

    def __init__(self, filename):
        self.wb = self.DIZPEXCEL.Workbooks.Open(filename)
        self.AS = self.wb.ActiveSheet

    def horizontal_alignment(self, req: int):
        xlLeft, xlRight, xlCenter = -4131, -4152, -4108
        tup = xlLeft, xlCenter,  xlRight
        try:
            return tup[req]
        except IndexError:
            print('horzontal alignment retornado None')
            return None

    def atiby_name(self, name):
        worksheet_iss = self.DIZPEXCEL.Worksheets(name)
        worksheet_iss.Activate()

        self.AS = worksheet_iss
        # necessário pois outra é ativada...

    def get_filled_values(self, rng):
        AS = self.AS
        for row in AS.Range(rng):
            if row.Value is not None:
                # r_sociais.append(row.Value)
                yield row.Value, row.Address
            else:
                break

    def tres_valores(self, __client_path):
        from pgdas_fiscal_oesk.relacao_nfs import tres_valores_faturados
        my_new_3valores = tres_valores_faturados(__client_path)
        if my_new_3valores:

            TOTAL, ComRetencao, SemRetencao = ["".join(valor.values()) for valor in my_new_3valores]

            # tutti = [v for v in my_new_3valores[0].values()][0]

            tutti = TOTAL, ComRetencao, SemRetencao

            return tutti
        else:
            return None, None, None

    def trata_3valores_ydm(self, valor):
        return 'zerou' if valor == 0 or valor is None else valor


class YouDidMe(VbaUtilities):

    def __init__(self):
        super().__init__(filename='C:/_SIMPLES/MEXENDO.xlsx')

    def preenche_iss_valores(self):
        AS = self.AS
        xlapp = self.DIZPEXCEL

        self.atiby_name('G5_ISS')

        for (e, row_row) in zip(count(start=0, step=1), self.get_filled_values('A:A')):

            if e != 0:
                cell_value, cell_address = row_row
                cell_address = AS.Range(cell_address)

                cli_path = self._files_path_v2(cell_value)
                # self.__client_path = cli_path
                total, com_ret, sem_ret = self.tres_valores(cli_path)
                print(total, com_ret)

                cell_address.Offset(1, npl('F')).Value = self.trata_3valores_ydm(sem_ret)
                cell_address.Offset(1, npl('F')).Select()

                xlapp.ActiveCell.Offset(1, 2).Value = com_ret
                xlapp.ActiveCell.Offset(1, 2).Select()

                xlapp.ActiveCell.Offset(1, 2).Value = total if 0 != total is not None else 'zerou'
                xlapp.ActiveCell.Offset(1, 2).Select()

                # Tem que selecionar depois de jogar o value... Porque senão, não seleciona
                # pq? Eu não sei, beleza

                # AS.Cells(1, npl('P')).Value = 'Teste'

    def checka_declaracoes_e_valida(self):
        from time import sleep

        sheets = 'sem_mov', 'G5_ISS', 'G5_ICMS'

        for sheet in sheets:
            self.atiby_name(sheet)
            sleep(2)
            for (e, row_row) in zip(count(start=0, step=1), self.get_filled_values('A:A')):
                if e != 0:
                    cell_value, cell_address = row_row
                    cell_address = self.AS.Range(cell_address)

                    cli_path = self._files_path_v2(cell_value)

                    celE = cell_address.Offset(1, npl('E'))
                    celE.Select()
                    for file in os.listdir(cli_path):
                        if file.lower().endswith('.pdf') and file.upper().startswith('PGDASD'):
                            celE.Value = 'S'

                            celE.HorizontalAlignment = self.horizontal_alignment(1)
                        else:
                            pass
                            # celE.Value = 'OK'


ydm = YouDidMe()









