from default import talk2cli
from time import sleep
from smtp_project.init_email import JsonDateWithImprove

from default.data_treatment import ExcelToData
from .init_wp import MainWP
vencimento_das = JsonDateWithImprove().vencimento_das()


class PgdasWP(MainWP, ExcelToData):

    def __init__(self):
        print('Este driver está localizado em MainWP, pois ele faz caminhos diferentes, checar depois')
        import pandas as pd
        # input(self.VENCIMENTO_DAS)
        sh_names = 'G5_ISS', 'G5_ICMS'

        compt, excel_file_name = self.set_get_compt_file(1)
        # posso mudar os argumentos de get_atual_competencia, ele já tem padrão, mas coloquei pra lembrar
        # responsivo...

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

                hora_da_mensagem = talk2cli.hora_mensagem_default()
                try:
                    wp = after_READ['whatsapp'][i].upper().strip()
                    wpenv = after_READ['wpenv'][i].upper().strip()
                    __valor = after_READ['Valor'][i]
                    try:
                        __valor = float(__valor)
                        __valor = f'R${__valor:.2f}'.replace('.', ',')
                    except ValueError:
                        pass

                    # campo no excel do cliente,  eu vou transformar isso tudo em json mais pra frente
                    if wp == 'WP':

                        # input(f'\033[1;33mcheguei no troll {CLIENTE}\033[m')
                        if CLIENTE == 'Leusivan Pereira Rodrigues':
                            print('\033[1;31mTratando os irmãos lourivan kk\033[m')
                            responsavel = after_READ['Razão Social'][i+1]
                        else:
                            responsavel = CLIENTE
                            print(responsavel)

                        if JA_DECLARED in ['S'] and wpenv not in ['S', 'OK']:
                            # responsavel = 'Pai'
                            self.driver = self.whatsapp_DRIVER(CLIENTE, True)

                            driver = self.driver
                            super().__init__(driver=driver)
                            print(f'\033[1;34mCLIENTE: {CLIENTE}\033[m')
                            pdf_files = self.files_get_anexos(CLIENTE, file_type='pdf', upload=True)
                            print(len(pdf_files))

                            print(pdf_files)

                            self.access_whatsapp_site()

                            self.search_and_open(responsavel)

                            self.write_wp_msg(f'{hora_da_mensagem}, {CLIENTE}! Sou da OESK Contábil, contador Osiel. '
                                              f'Esta mensagem é referente à apuração da competência {compt}',
                                              f'Segue boleto PGDAS a vencer no dia {vencimento_das}, sobre valor de {__valor}. '
                                              f'Segue também protocolos sobre a declaração. ATT',
                                              f'Também enviei em seu email: {after_READ["email"][i]}',
                                              'Atenciosamente.'
                                              )

                            self.anexa_wp_files(*pdf_files)
                            sleep(5)
                            self.quit_session()

                except KeyError:
                    pass

                finally:
                    print(CLIENTE)
