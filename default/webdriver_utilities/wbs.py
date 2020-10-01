from default.webdriver_utilities import *
# wbs = web driver shortcuts


class WDShorcuts:
    def __init__(self, driver):
        self.__arg_driver = driver

    def send_keys_anywhere(self, typed, times=1, pause=.13):
        """
        :param typed: o que quero digitar EM QUALQUER LUGAR DO NAVEGADOR
        :param pause: float interval
        :param times: quantidade de vezes
        :return: já digitado
        """
        from time import sleep

        driver = self.__arg_driver
        actions = ActionChains(driver=driver)
        for i in range(times):
            # print('send keys')
            actions.send_keys(typed)
            actions.pause(pause)
        actions.perform()
        sleep(1)

    def keys_action(self, *args, pause=1):
        """
        :param str args: keys or selenium keys
        :param float pause: how long time to pause
        """
        driver = self.__arg_driver
        action = ActionChains(driver=driver)

        action.send_keys(*args)
        action.pause(pause)

        action.perform()
        driver.implicitly_wait(pause)

    def click_ac_elementors(self, *args, pause=1.5):
        """
        :param args: element already defined
        :param pause: pause between clicks and elements
        :return:
        """
        driver = self.__arg_driver
        action = ActionChains(driver=driver)
        for arg in args:
            action.move_to_element(arg)
            action.click()
        # x, y = xy = driver.find_element_by_tag_name('label').location.values()
        action.perform()
        driver.implicitly_wait(pause)

    def click_elements_by_tt(self, *args, tortil='text'):
        # by_tt = by text or title
        """
        :param args: classes p/ find by text only
        :param tortil: Optional text, or set title

        *** with_text
        :return:
        """
        from selenium.webdriver.common.action_chains import ActionChains
        driver = self.__arg_driver

        action = ActionChains(driver=driver)

        for e, arg in enumerate(args):
            if tortil == 'title':
                elem = self.contains_title(arg)
            else:
                elem = self.contains_text(arg)

            x, y = xy = elem.location.values()
            action.move_to_element(elem)
            action.click()
            if e > 0:
                driver.implicitly_wait(2.5)
        action.perform()

    def contains_text(self, item):
        driver = self.__arg_driver
        el = driver.find_element_by_xpath(f'//*[contains(text(),"{item}")]')
        return el

    def contains_title(self, item):
        driver = self.__arg_driver
        el = driver.find_element_by_css_selector(f"[title*='{item}']")
        return el

    def tags_wait(self, *tags):
        driver = self.__arg_driver
        delay = 10
        for tag in tags:
            try:
                my_elem = WebDriverWait(driver, delay).until(expected_conditions.presence_of_element_located((By.TAG_NAME, tag)))
                # print(f"\033[1;31m{tag.upper()}\033[m is ready!")
            except TimeoutException:
                print("Loading took too much time!")

    def find_submit_form(self):
        driver = self.__arg_driver
        self.tags_wait('form')
        driver.implicitly_wait(5)
        driver.find_element_by_tag_name("form").submit()

    def get_sub_site(self, url, main_url):
        """
        :param url: / + get
        :param main_url: url atual
        :return:
        """
        # site dentro de site...
        new_url = f'{main_url}{url}'.replace('//', '/')

        driver = self.__arg_driver
        driver.get(new_url)

    def del_dialog_box(self, class_name):
        """
        :param class_name: Deleta por Class, nome
        :return: javascript

        # GLÓRIA A DEUS
        """
        driver = self.__arg_driver

        # driver.find_element_by_xpath('//div[@class=""')
        try:
            driver.implicitly_wait(10)
            driver.execute_script(f"return document.getElementsByClassName('{class_name}')[0].remove();")
        except JavascriptException:
            print('Elemento não encontrado em self.del_dialog_box')
        else:
            print('certo')