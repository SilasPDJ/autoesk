from default.webdriver_utilities import Options, webdriver
from whatsapp.dialog_profile_path import profiles_main_folder
# from default.settings.set_paths import SetPaths

# import QR code...
# o outro driver "mais complexo" está somente dentro do projeto whatsapp


def default_qrcode_driver(path=''):
    """
    :param path: default path atual (downloads)
    :return: o driver para fechar no loop

    # sem perfil específico

    # new_path_set -> abre uma pasta para download especificada caso ela não exista ainda
    """
    __padrao = profiles_main_folder()
    # path = SetPaths().new_path_set(path)
    # já está em mamae_download

    path = path.replace('/', '\\')
    # o try já tá dentro de replace

    link = "Chromedriver/chromedriver.exe"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument(f"user-data-dir={__padrao}")
    # carrega o perfil padrão com o qr_code
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        'profile.default_content_setting_values.automatic_downloads': 1

    })

    chromedriver = link
    driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

    # self.tags_wait('body', 'input', 'div')

    # sleep(5)
    return driver
