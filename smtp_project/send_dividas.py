from smtp_project import EmailExecutor
# from smtp_project import *


class SendDividas(EmailExecutor):
    def __init__(self):
        import pandas as pd
        super().__init__()
        # venc_dividas = self.das_venc_data()[3]

        excel_compt, excel_file_name = self.get_atual_competencia(-1)
        go_get = excel_compt, excel_file_name
        self.venc_boletos = self.get_vencimento()

        print('VENCIMENTO DÍVIDAS: ', self.venc_boletos)

        sh_names = ['_Dívidas']

        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path
            mshExcelFile = pd.ExcelFile(excel_file_name)
            # input(mshExcelFile.sheet_names)
            msh = mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = mshExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            self.after_READ = self.readnew_lista(READ, False)
            after_READ = self.after_READ

            for i, CNPJ in enumerate(after_READ['CNPJ']):
                # ####################### A_Main INTELIGENCIA EXCEL ESTÁ SEM OS SEM MOVIMENTOS NO MOMENTO

                CLIENTE = after_READ['Razão Social'][i]
                JA_DECLARED = after_READ['Declarado'][i].upper().strip()
                # CodSim = after_READ['Código Simples'][i]
                # CPF = after_READ['CPF'][i]
                # icms_or_iss = sh_names[sh_names.index(sh_name)]
                JA_FOI_ENV = after_READ['envio'][i].upper().strip()
                now_email = after_READ['email'][i]

                if JA_DECLARED in ['S', 'OK', 'FORA'] and JA_FOI_ENV not in ['S', 'OK']:
                    print(now_email)
                    # print(f'VALOR: {VALOR}')
                    print(f'CLIENTE: {CLIENTE}')

                    dividas_pdf_files = self.files_get_anexos(CLIENTE, year=False, file_type='pdf')
                    qtd_arquivos = len(dividas_pdf_files)
                    mail_header = f"com vencimento previsto para o dia: {self.venc_boletos.replace('-', '/')}"
                    mail_header = f"Parcelamentos, {'boleto' if qtd_arquivos == 1 else 'boletos'} {mail_header}"
                    print('titulo: ', mail_header)

                    message = self.mail_dividas_msg(CLIENTE, CNPJ, len(dividas_pdf_files))
                    print(message)
                    das_message = self.write_message(message)

                    # input(len(dividas_pdf_files))

                    # input('camdaprotetora')

                    # self.main_send_email(now_email, mail_header, das_message, dividas_pdf_files)
                    self.main_send_email(now_email, mail_header, das_message, dividas_pdf_files)

                    """a partir do terceiro argumento, só há mensagens attachedas"""

    def mail_dividas_msg(self, client, cnpj, main_anx_len=0):

        colours = self.load_json('zlist_colours.json')
        red, blue, money, parc_style = \
            self.wcor(colours[114]), self.wcor('blue'), ' style="background-color:yellow; color:green"', \
            'style="background-color:yellow; color:red"'
        ntt = self.tag_text
        inso = self.inside_me_others
        # posso inso dentro de inso sem problema
        full_mensagem = f"""
{ntt('h1', f'{self.hora_mensagem()}, {client}!')}

{inso(ntt('h2', 'Seguem anexados:'), inso(ntt('p', '->'),ntt('span '+parc_style, f' {main_anx_len} Parcelamentos pendentes'), 
                                          ntt('h2', '-> A data de vencimento é igual para todos os boletos anexados')))
        if main_anx_len > 1 else inso(ntt('h2', 'Segue anexado:'), inso(ntt('p', '-> '),ntt('span'+red, 'Parcelamento pendente'))) 
        if main_anx_len > 0 else ntt('h3'+money, 'NÃO HÁ PARCELAMENTOS PENDENTES OU ANEXADOS')}


<div>
Este e-mail é automático. Por gentileza, cheque o nome e o CNPJ ({ntt('span'+red, cnpj)}) antes de pagar o documento.
<h4>Caso haja qualquer conflito, responda sem hesitar esta mensagem neste e-mail.</h4>
<h4>Todas as declarações são e continuarão sendo feitas minuciosamente.</h4>
</div>
{ntt('h2'+blue,'ATT, Oesk Contábil')}
        """
        return full_mensagem

    def get_vencimento(self):
        """
        :param m_cont: quantos meses para trás? (0 atual)
        :param y_cont: quantos anos para trás?

        :return: data vencimento formato dia-mes-ano
        """

        mes_ano_folder = self.compt_and_filename()[0]
        print('Mês, ano, folder', mes_ano_folder)
        venc_dividas = self.get_last_business_day_of_month()

        venc = f'{venc_dividas}-{mes_ano_folder}'

        return venc

# depois o send email vai emglobar tudo que ta em package init_email... # no projeto final