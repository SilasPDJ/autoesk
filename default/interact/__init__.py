def press_key_b4(key: str):
    """
    # # PRECISO COLOCAR ELE EM OUTRO LUGAR ############## CHECAR OS LUGARES EM Q ESTE METODO ESTÁ
    :param key: é a key, presente no SemMov_fullSELENIUM
    :return:
    """
    from keyboard import is_pressed
    while True:
        #
        if is_pressed(key):
            if is_pressed(key):
                return True
        else:
            ...


def press_keys_v4(*keys: str):
    """
    :param keys: any key you wish
    :return:
    """
    import keyboard
    from keyboard import is_pressed
    while True:
        for key in keys:
            if is_pressed(key):
                if is_pressed(key):
                    return key
            else:
                pass
                # print(key)


def activate_window(title, where=''):
    """
    :param title: nome/name janela/window
    :param where: optional. Message
    :return: última janela de um title específico ativada para manipular a princípio o diálogo do sistema operacional

    # done
    """
    from time import sleep
    from pyautogui import getWindowsWithTitle, hotkey, getActiveWindow, keyUp, keyDown
    # my_window = getWindowsAt(-1055, 0)[0]

    window = getWindowsWithTitle(title)
    window = window[0]

    # print(window.right, window.top, '..', window.title)
    # window.move(1055, 0)
    sleep(2)
    msg = f'{window.title}.\n\n {where.upper() if where != "" else ""}'
    # self.mensagem(msg)
    tk_msg(msg)
    tabs = ['tab']
    while True:

        sleep(2)
        try:
            var = getActiveWindow().title
            var = var.lower()
            win_logic = window.title.lower()
            print(var, window.title)
            if var == win_logic:
                break
            else:
                keyDown('alt')
                for tab in tabs:
                    hotkey(tab)
                keyUp('alt')
                tabs.append('tab')
        except AttributeError:
            print('window not found')
            pass


def tk_msg(mensagem:str, time=7):
    """
    chamada em activate_driver_window
    :param mensagem: text displayed
    :param time: cont time before closes
    """
    import tkinter as tk

    class ExampleApp(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            tk.Label(text=mensagem, pady=10).pack()

            tk.Button(self, text="OK", fg='white', bg='black', command=self.destroy, activeforeground="black",
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
                self.destroy()
            else:
                self.label.configure(text="%d" % self.remaining)
                self.remaining = self.remaining - 1
                self.after(1000, self.countdown)

    print('Mensagem: ', mensagem)
    ExampleApp().mainloop()
