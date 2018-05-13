from os import environ
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest

import constants
from pages.mainpage import MainPage
from datetime import datetime

SCREENSHOT_PATH = constants.SCREENSHOT_PATH + '/video/'


class ExampleTest(unittest.TestCase):
    LOGIN = environ['LOGIN']
    PASSWORD = environ['PASSWORD']

    def setUp(self):
        browser = environ.get('BROWSER', 'CHROME')

        self.driver = webdriver.Remote(
            command_executor=constants.COMMAND_EXECUTOR,
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def test_auth(self):
        main_page = MainPage(self.driver)
        main_page.open()
        main_page.authentificate(self.LOGIN, self.PASSWORD)
        self.driver.save_screenshot(SCREENSHOT_PATH + 'login{time}.png'.format(time=datetime.now().time().isoformat()))
        self.driver.delete_all_cookies()
        self.driver.refresh()
        self.driver.save_screenshot(SCREENSHOT_PATH + 'sessionreset{time}.png'.format(time=datetime.now().time().isoformat()))
