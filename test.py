import pyautogui as pygui
from time import sleep


def _sleepme():
    sleep(.25)


pygui.hotkey('alt', 'tab')
for i in range(6, 13):

    sleep(1)
    _sleepme()
    pygui.write(f'0{i}') if len(str(i)) == 1 else pygui.write(str(i))
    _sleepme()
    pygui.write(str(2020))
    _sleepme()
    pygui.hotkey('enter')
    sleep(1)
    pygui.hotkey('tab')
    _sleepme()
    pygui.hotkey('enter')
    sleep(1)
    pygui.hotkey('enter')
    sleep(1)
    pygui.click(x=519, y=580)
    sleep(1)
    pygui.click(x=119, y=270)
    sleep(1)