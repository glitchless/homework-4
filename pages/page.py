import urlparse
from selenium.webdriver import Remote

import constants


class Page:
    BASE_URL = constants.BASE_URL
    PATH = ''

    def __init__(self, driver):
        # type: (Remote) -> None
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        # self.driver.maximize_window()