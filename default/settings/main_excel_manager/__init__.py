def mensagem(arq_name):

    mensagem = f'O arquivo {arq_name} foi atualizado com sucesso através de outro arquivo'
    # messagebox.showinfo('ATENÇÃO!', message=mensagem)
    import tkinter as tk
    time = 7

    class ExampleApp(tk.Tk):
        def __init__(self):
            super().__init__(self)
            tk.Label(text=mensagem, pady=10).pack()
            tk.Button(self, text="OK", command=self.quit, fg='white', bg='black', activeforeground="black",
                      activebackground="green4", pady=10, width=10).pack()

            self.label = tk.Label(self, text="", width=10)
            self.label.pack()
            self.remaining = 0
            self.countdown(time)
            # self.after(time * 1000, lambda: self.destroy())
            self.geometry('500x250+1400+10')

        def countdown(self, remaining=None):
            if remaining is not None:
                self.remaining = remaining

            if self.remaining <= 0:
                self.label.configure(text="000000")
                self.quit()
            else:
                self.label.configure(text="%d" % self.remaining)
                self.remaining = self.remaining - 1
                self.after(1000, self.countdown)

    ExampleApp().mainloop()


def show_actual_tk_window(searched='tk'):
    import pyautogui as p
    from time import sleep
    lis = p.getAllWindows()

    for e, l in enumerate(lis):
        # print(l.title.lower())
        # l.restore()
        # l.activate()
        if searched == l.title.lower():
            print(f'Já achei uma flor gloriosa {l.title.lower()}, --> {searched}')
            fw = p.getWindowsWithTitle(l.title)
            # fw = fw[0]
            # fw.maximize()
            # fw.activate()
            sleep(0.5)
            print(l.title)
            break
        sleep(0.2)

    sleep(1)
    # hotkey('alt', 'shift', 'tab', interval=0.2)


def threading(arq_name):
    """
    :param arq_name: from exe
    :return: mixes the two functions above (show_actual_tk_window, mensagem)
    """
    from concurrent.futures import ThreadPoolExecutor
    executors_list = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        executors_list.append(executor.submit(mensagem, arq_name=arq_name))
        executors_list.append(executor.submit(show_actual_tk_window, searched='tk'))
        # executors_list.append(executor.submit(alt_tab))


def exe():
    from datetime import datetime
    ano = datetime.now().year
    mes = datetime.now().month
    arq_name = f'{mes-1:02d}-{ano}.xlsx'

    import os
    os.system('xlsx_changeME.lnk') # excel abre MEXENDO na pasta salva

    from os import system
    system('SAVEafter-changes.lnk')

    threading(arq_name)
    # mensagem(arq_name)

def target():
    """
    # read_path_files

    # quem manda é o with_titlePATH daqui, o outro vai pra outro lugar

    :return: O lugar onde estão as planilhas
    """


    with_title_name = 'with_titlePATH.txt'
    try:

        value = open(with_title_name).read()

    except FileNotFoundError:
        # IF FILE CONTAINING PATH NOT EXISTS, IT'LL DISPLAY A SELECTOR

        def returned_quero_2x(ff):
            quero = ''
            for f in ff:
                quero += f'{f}/'
            return quero

        from tkinter import filedialog
        from tkinter import Tk
        root = Tk()
        root.withdraw()
        root = Tk()
        root.withdraw()
        while True:



            way = filedialog.askdirectory(title='SELECIONE ONDE ESTÃO SUAS PLANILHAS')
            """~~~~~~~~~~~MEXENDO~~~~~~~~~~~~~~~~~~~~"""

            # pega onde está localizado o caminho do atalho escreve o caminho "way" vindo do filedialog
            # num arquivo da localização do atalho para que onde ele estiver
            # possa ler onde está foi que o filedialog quis ser feito

            file_in_email_exe_path = read_path_files('SAVEafter-changes.lnk')
            ffi = file_in_email_exe_path.split(chr(92))[:-1]

            fatiado_1 = returned_quero_2x(ffi)

            file_way = open(f'{fatiado_1}/{with_title_name}', 'w')
            file_way.write(way)
            file_way.close()

            """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


            """~~~~~~~~~~~~MEXENDO 2 ~~~~~~~~~~~~~~~~~~"""
            file_for_target = read_path_files('xlsx_changeME.lnk')
            ffe = file_for_target.split(chr(92))[:-1]
            fatiado_2 = returned_quero_2x(ffe)

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
    finally:
        ...

    return value


def reset_mexendo():
    def atualiza():
        data = read_path_files('xlsx_changeME.lnk')
        print(f'Atualizando o arquivo {data}')
        from shutil import copy2

        PATH = target()

        copy2(r'{}/padrão_pandas_.xlsx'.format(PATH),
              r'{}'.format(data))
    # meu reset por enquanto ta com problema

    from datetime import datetime as dt
    mes = dt.now().month - 1
    mes = f'{mes:02d}'
    try:
        file = open('MEXENDOchangeCHECKER_ID.txt', 'r')
        check = file.read()
        # print(check)
        if check != mes:
            # ESTAMOS NUM NOVO MÊS
            atualiza()

            file = open('MEXENDOchangeCHECKER_ID.txt', 'w')
            file.write(mes)
            file.close()

    except FileNotFoundError:
        file = open('MEXENDOchangeCHECKER_ID.txt', 'w')
        file.write(f'{mes}')
        file.close()
