def profiles_main_folder(recria_padrao=False):
    """
    :param recria_padrao: True -> apaga arquivo e abre caixa de diálogo
    Create new profile
    """
    #
    with_title_name = 'PATH_PROFILES.txt'
    if recria_padrao:
        with open(with_title_name, 'w') as f:
            f.write('')
    try:
        value = open(with_title_name).read()
        if value == '':
            raise FileNotFoundError
    except FileNotFoundError:
        # IF FILE CONTAINING PATH NOT EXISTS, IT'LL DISPLAY A SELECTOR

        from tkinter import filedialog
        from tkinter import Tk
        root = Tk()
        root.withdraw()
        root = Tk()
        root.withdraw()
        while True:
            input('cheguei em onde estão as planilhas aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa tiramee')
            way = filedialog.askdirectory(title='SELECIONE ONDE ESTÃO SUAS PLANILHAS')

            # input(f'{fatiado_1} ;;;; {fatiado_2}')
            """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

            file = open(with_title_name, 'w') # mt da hora
            file.write(way)
            file.close()
            value = open(with_title_name).read()
            if len(value) <= 0:
                from tkinter import messagebox
                resp = messagebox.askokcancel('ATENÇÃO!', message='Selecione uma pasta ou clique em CANCELAR.')
                if not resp:
                    return
            else:
                root.quit()
                break
            root.mainloop()
    value = value.replace('/', '\\')
    return value
