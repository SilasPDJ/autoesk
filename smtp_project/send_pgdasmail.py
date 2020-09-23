from smtp_project import EmailExecutor
# from smtp_project import *


class PgDasmailSender(EmailExecutor):

    def __init__(self):
        import pandas as pd
        super().__init__()
        venc = self.VENCIMENTO_DAS
        sh_names = 'sem_mov', 'G5_ISS', 'G5_ICMS'

        compt, excel_file_name = self.get_atual_competencia(1)
        # posso mudar os argumentos de get_atual_competencia, ele já tem padrão, mas coloquei pra lembrar

        mail_header = f"Fechamentos para apuração do imposto PGDAS, competência: {compt.replace('-', '/')}"
        print('titulo: ', mail_header)
        # é o meu teste

        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path
            mshExcelFile = pd.ExcelFile(excel_file_name)

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
                CodSim = after_READ['Código Simples'][i]
                CPF = after_READ['CPF'][i]
                icms_or_iss = sh_names[sh_names.index(sh_name)]

                try:
                    VALOR = self.trata_money_excel(after_READ['Valor'][i])
                except KeyError:
                    VALOR = self.trata_money_excel('zerou')
                try:
                    now_email = after_READ['email'][i]
                    JA_FOI_ENV = after_READ['envio'][i].upper().strip()
                except KeyError:
                    print(f'CLIENTE {CLIENTE}\033[1;31m NÃO\033[m tem email')
                    JA_FOI_ENV = 'OK'
                else:
                    if now_email == '':
                        print(f'-------------> PLANILHA {sh_name}')
                        input('Enter p/ terminar')
                        break
                        # raise KeyError
                    if JA_DECLARED in ['S', 'OK', 'FORA'] and JA_FOI_ENV not in ['S', 'OK']:
                        print(now_email)
                        print(f'VALOR: {VALOR}')
                        print(f'CLIENTE: {CLIENTE}')

                        message = self.mail_pgdas_msg(CLIENTE, CNPJ, icms_or_iss, VALOR)
                        # input(message)
                        das_message = self.write_message(message)

                        das_anx_files = self.files_get_anexos(CLIENTE)

                        self.main_send_email(now_email, mail_header, das_message, das_anx_files)
                        """a partir do terceiro argumento, só há mensagens attachedas"""

    def mail_pgdas_msg(self, client, cnpj, tipo_das, valor):

        colours = self.load_json('zlist_colours.json')
        red, blue, money = self.wcor(colours[114]), self.wcor('blue'), 'style="background-color:yellow; color:green"'
        ntt = self.tag_text
        inso = self.inside_me_others
        inside_me = ntt(f'strong'+blue, 'inside meeeeeeeee')
        # {inso(ntt('h2'+blue, f"{self.hora_mensagem()}, "), ntt("span"+blue,f"{client}!"))}
        # {inso(ntt('h3' + blue, f'CNPJ: '), ntt('span' + red, cnpj))}
        # {ntt('h3', f'CNPJ: {cnpj}')}
        full_mensagem = f"""
{ntt('h2', f'{self.hora_mensagem()}, {client}!')}
{ntt('h3', 'Seguem anexados:')}
<h3> 
-> DAS ({ntt('span'+blue,'ISS' if 'ISS' in tipo_das.upper() else 'ICMS')})
sobre faturamento de {ntt('span style="background-color:yellow; color:green"', 'R$ '+valor)}
</h3>

<h3> 
    -> Protocolos e demonstrativos respectivos
            {
    f'''
    <h3>
        -> A data de vencimento do boleto é: {ntt('span' + red, self.VENCIMENTO_DAS)}
    </h3>
    <h4> 
        -> O arquivo do boleto contém as iniciais "{ntt('span'+red,'PGDASD-DAS')}"
    </h4>
    '''
            if valor != 'SEM VALOR DECLARADO' else f"<h3>{ntt('span'+red,'NÃO')} há boleto a pagar.</h3>"
            }
<hr>
</h3> 


<div>
Este e-mail é automático. Por gentileza, cheque o nome e o CNPJ ({ntt('span'+red, cnpj)}) antes de pagar o documento.
<h4>Caso haja qualquer conflito, responda sem hesitar esta mensagem neste e-mail.</h4>
<h4>Todas as declarações são e continuarão sendo feitas minuciosamente.</h4>
</div>
{ntt('h2'+blue,'ATT, Oesk Contábil')}

        """
        return full_mensagem
