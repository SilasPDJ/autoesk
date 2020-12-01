import pandas as pd
from default import ExcelToData
from default.settings.set_paths import SetPaths


def parse_sh_name(excel_file_name, data_required=True):
    """
    :param tup: compt and excel_file_name from self._atual_compt_and_file
    :param data_required: data_Required
    :return:
    """

    xls = pd.ExcelFile(excel_file_name)
    sheet_names = iter(xls.sheet_names)
    for e, sh in enumerate(sheet_names):
        # if e > 0:
        if data_required:
            yield xls.parse(sh, dtype=str), sh
        else:
            yield sh


set_paths = SetPaths()
compt_atual, file_name = set_paths.compt_and_filename()

dados = parse_sh_name(file_name)


def parse_searched(searched_sh_nome, *searched_headers):
    for plan_gen, sh_nome in dados:
        searched = dict()
        if sh_nome == searched_sh_nome:
            for __header, __valores in plan_gen.to_dict().items():

                for __shs in searched_headers:
                    if __shs == __header:
                        # print('~~~', __header, '~~~')
                        searched[__shs] = []
                        for e, val in __valores.items():
                            val = val.strip()
                            searched[__shs].append(val)
                            # print(val)
                        yield searched

        # print('---------------',sh_nome, ' ----------------')


def parse_final(parsearch, printme=False):

    def typeof(my_var):
        # print(f'{my_var if isinstance(my_var, str) else [nome for nome in my_var[:listcontmax]]} do tipo: {type(my_var)}')
        # tentei mas não fez o mesmo
        if isinstance(my_var, (str, int)):
            print('Tipo de: ', my_var, type(my_var))
        else:
            for parte in my_var[:]:
                print('Tipo de: ', parte, '...', type(my_var)) if len(parte) <= 25 else None

    for ddc in iter(parsearch):
        for key, value in ddc.items():
            print(key, ':', value)
            if printme:
                typeof(key)
                typeof(value)


parse_final(parse_searched('G5_ISS', 'Razão Social'))


input('')


# a = parse_searched('G5_ISS','Razão Social', 'CNPJ')
# print(list(a))

for dictt in iter(parse_searched('G5_ISS', 'Razão Social')):
    for k, v in dictt.items():
        print(k, ':', v)
    # set_paths._files_path_v2()
input()
parse_sh_name(set_paths.compt_and_filename())
