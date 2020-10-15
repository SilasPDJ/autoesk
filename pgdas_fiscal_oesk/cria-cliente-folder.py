def cria_client_folder(fold_path=r'C:\Users\Silas\OneDrive\_FISCAL-2020', year_first=True):
    import os
    from datetime import datetime as dt
    os.chdir(fold_path)
    # vou criar os meses
    type_folders = os.listdir()
    ano = dt.now().year
    """
    :param fold_path: Caminho da pasta, vindo do dialogbox
    :param year_first: Ano criado primeiro ou não? 
    :return: pastas criadas dos anos com sucesso

    # o os.chdir tem que fazer um dialogo p/ selecionar onde estão os clientes


    Autor: S.B Ferreira utilizando módulo OS 
    """
    cont = 10

    tf = input('Digite o nome do cliente: ')
    # for tf in type_folders:
    try:
        os.chdir(tf)  # mudei pros g5, sem_mov, etc
    except FileNotFoundError:
        os.mkdir(tf)
    a = os.listdir()  # criei a lista dos clientes
    for sub_folder in a:
        # Year first
        if year_first:
            os.mkdir(r'{}/{}'.format(sub_folder, ano))
            for i in range(1, 12 + 1):  # meses
                os.mkdir(r'{}/{}/{:02d}-{}'.format(sub_folder, ano, i, ano))
        else:
            for i in range(1, 12 + 1):
                os.mkdir(r'{}/{:02d}-{}'.format(sub_folder, i, ano))
    print(f'Estou carregando... {cont * 3.3}%')
    cont += 10
    # o nome is up
    os.chdir('..')
    print('..................... 100%')


# cria_folders_este_ano_t()
cria_client_folder(r'C:\Users\Silas\OneDrive\_FISCAL-2020\G5')
