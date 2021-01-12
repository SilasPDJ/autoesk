from datetime import datetime as dt


class Now:

    @staticmethod
    def time():
        pass

    @staticmethod
    def hj():
        return dt.now().day

    @staticmethod
    def m():
        return dt.now().month

    @staticmethod
    def y():
        return dt.now().year

    @staticmethod
    def nome_mes(mes: int):
        nomes = """Janeiro 
        Fevereiro
        Março
        Abril
        Maio
        Junho
        Julho
        Agosto
        Setembro
        Outubro
        Novembro
        Dezembro
        """.strip().split()
        if mes > 0:
            return nomes[mes - 1]
        elif mes == 0:
            print('\033[1;31m Retornando janeiro')
            return nomes[0]
        else:
            return nomes[mes]

    @staticmethod
    def date2date_brazil(dd, sep='/'):
        try:
            dia = dd.day
            mes = dd.month
            ano = dd.year
        except (AttributeError, NameError) as e:
            raise e('Deu ruim!!! date2date_brazil')
        else:
            return f'{dia:02d}{sep}{mes:02d}{sep}{ano}'
