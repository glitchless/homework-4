from os import environ
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import constants
from pages.mainpage import MainPage
from pages.video import VideoPage
from datetime import datetime

SCREENSHOT_PATH = constants.SCREENSHOT_PATH + '/video/'


class VideoTest(unittest.TestCase):
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

    def test_going_to_videopage(self):
        main_page = MainPage(self.driver)
        main_page.open()
        main_page.authentificate(self.LOGIN, self.PASSWORD)
        self.driver.save_screenshot(SCREENSHOT_PATH + 'login{time}.png'.format(time=datetime.now().time().isoformat()))
        main_page.go_to_videos()

        video_page = VideoPage(self.driver)

        video_page.wait_for_load()

        self.driver.save_screenshot(SCREENSHOT_PATH + 'videopage{time}.png'.format(time=datetime.now().time().isoformat()))

        main_page.hard_clear_authentification()
        self.driver.refresh()
        self.driver.save_screenshot(SCREENSHOT_PATH + 'sessionreset{time}.png'.format(time=datetime.now().time().isoformat()))