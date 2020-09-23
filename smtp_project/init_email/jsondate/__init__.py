import json
# from smtp_project import *


class JsonDateWithImprove:
    def __init__(self):
        # se eu colocar a class parent de parâmetro no super, ele vai ignorar o init dela
        self.last_portal_update()
        self.VENCIMENTO_DAS = self.das_venc_data()[0]
        print(f'Data de vencimento (PGDAS): {self.VENCIMENTO_DAS} (JsonDateWithImprove)')
        # input(self.VENCIMENTO_DAS)

    @staticmethod
    def vencimento_das(n=0):
        # pega o vencimento do site pra puxar em outro lugar, muito legal
        self = JsonDateWithImprove()
        return self.das_venc_data()[n]

    def inside_me_others(self, inside_me, *others):
        """
        :param str inside_me:
        :param str others:
        :return:

        Cria tags (*others) dentro da inside_me
        """
        # pega o final e separa para colocar no meio
        ff = inside_me.index('</')

        final = inside_me[ff:]
        returned = inside_me[:ff]

        for other in others:
            returned += other
            # input(returned)
        returned += final
        return returned

    def wcor(self, cor):
        r = f' style=color:{cor}'
        return r

    def load_json(self, file):
        """
        :param str file: file name
        :return: dict or list or tuple from json loaded
        """

        with open(file, 'r') as f:
            return json.load(f)

    def dump_json(self, objeto, file):
        """
        :param object objeto:
        :param file:
        :return:

        # object engloba list, tuple, dict
        """
        with open(file, 'w') as f:
            json.dump(objeto, f)

    def das_venc_data(self):
        """

        bs4 BeautifulSoup requests

        :return: A_Main data de vencimento da competência de acordo com o portal
        """
        from bs4 import BeautifulSoup
        import requests

        def soup(me):
            """
            :param me: element
            :return:
            """
            me = str(me)
            btf = BeautifulSoup(me, 'html.parser')
            return btf

        # bto é btf
        req = requests.get('http://www8.receita.fazenda.gov.br/SimplesNacional/Agenda/Agenda.aspx').text
        btinit = soup(req)
        # btinit = BeautifulSoup(rq, "html.parser")
        # aqui é o início, a soup vai ser com os elementos vindos daqui

        agenda = btinit.select('#agenda .prazo')
        # print(agenda) -> HTML
        venc = soup(agenda)
        venc_text = venc.get_text()
        venc_final = self.date_only(venc_text)

        # venc_final[0] -> DAS, venc_final[1] -> MEI
        venc_final = venc_final[0] if len(venc_final) == 1 else venc_final
        # return vencimento DAS date
        return venc_final

        # soup(el).get_text # -> somente um dos métodos, o mesmo retorna uma lista

    def last_portal_update(self):
        """
        :return: data da atualização
        """

        from bs4 import BeautifulSoup
        import requests

        def soup(me):
            """
            :param me: element
            :return:
            """
            me = str(me)
            btf = BeautifulSoup(me, 'html.parser')
            return btf

        # bto é btf
        req = requests.get('http://www8.receita.fazenda.gov.br/SimplesNacional/Agenda/Agenda.aspx').text
        btinit = soup(req)

        last_update = btinit.select('#atualizado')

        updt = soup(last_update)
        updt = updt.get_text()

        updt = self.date_only(updt)
        # se o len do update for 1, é o caso do id, não precisa colocar index

        try:
            with open('ultima_att_agenda.txt') as f:
                att = f.read()
                if self.date_only(att) != updt:
                    raise FileNotFoundError
                    # ele vai escrever a última atualização
                else:
                    raise FileExistsError
        except FileNotFoundError:
            with open('ultima_att_agenda.txt', 'w') as f:
                f.write(updt)
                print(' \033[1;31m -------> NOVA ATUALIZAÇÃO DO PORTAL!!!\033[m')
                return updt

        except FileExistsError:
            with open('ultima_att_agenda.txt', 'w') as f:
                f.write(f'ATUALIZADO -> {updt}')
                print('\033[1;34m ---> Portal está de acordo com o arquivo\033[m')
                return att

        # return True pra de acordo e False pra nova atualização????????????????????????????

    def date_only(self, venc_text):
        """
        :param venc_text: containing DATES
        :return: list scrapping DATES
        """
        try:
            venc_text = venc_text.split()
        except AttributeError:
            if isinstance(venc_text, object):
                print('prossegue')
            else:
                return False

        venc_final = []
        for el in venc_text:
            new_el = ''
            for e in el:
                if e.isnumeric() or e == '/':
                    new_el += e
                    new_el = new_el.strip()
            if new_el != '':
                venc_final.append(new_el)

        venc_final = venc_final[0] if len(venc_final) == 1 else venc_final
        # se tiver o tamanho só de 1, eu já retorno, por causa do teste na função self.last_portal_update
        return venc_final