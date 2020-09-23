from default.webdriver_utilities import *

# wbs = web driver shortcuts


class WDShorcuts:
    def __init__(self, driver):
        self.arg_driver = driver

    def send_keys_anywhere(self, typed, times=1, pause=.13):
        """
        :param typed: o que quero digitar EM QUALQUER LUGAR DO NAVEGADOR
        :param pause: float interval
        :param times: quantidade de vezes
        :return: já digitado
        """
        from time import sleep

        driver = self.arg_driver
        actions = ActionChains(driver=driver)
        for i in range(times):
            # print('send keys')
            actions.send_keys(typed)
            actions.pause(pause)
        actions.perform()
        sleep(1)

    def click_ac_elementors(self, *args, pause=1.5):
        """
        :param args: element already defined
        :param pause: pause between clicks and elements
        :return:
        """
        driver = self.arg_driver
        action = ActionChains(driver=driver)
        for arg in args:
            action.move_to_element(arg)
            action.click()
        # x, y = xy = driver.find_element_by_tag_name('label').location.values()
        action.perform()
        driver.implicitly_wait(pause)

    def keys_action(self, *args, pause=1):
        """
        :param str args: keys or selenium keys
        :param float pause: how long time to pause
        """
        driver = self.arg_driver
        action = ActionChains(driver=driver)

        action.send_keys(*args)
        action.pause(pause)

        action.perform()
        driver.implicitly_wait(pause)

    def tags_wait(self, *tags):
        driver = self.arg_driver
        delay = 10
        for tag in tags:
            try:
                my_elem = WebDriverWait(driver, delay).until(expected_conditions.presence_of_element_located((By.TAG_NAME, tag)))
                # print(f"\033[1;31m{tag.upper()}\033[m is ready!")
            except TimeoutException:
                print("Loading took too much time!")
