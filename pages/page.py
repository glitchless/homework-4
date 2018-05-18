from urllib.parse import urljoin
from selenium.webdriver import Remote

import constants


class Page(object):
    BASE_URL = constants.BASE_URL
    PATH = ''
    driver = None  # type: Remote

    def __init__(self, driver):
        # type: (Remote) -> None
        self.driver = driver

    def open(self, relative_url=''):
        # type: (str) -> None
        url = urljoin(urljoin(self.BASE_URL, self.PATH), relative_url)
        self.driver.get(url)
        # self.driver.maximize_window()