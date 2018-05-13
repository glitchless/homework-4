from os import environ
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest

import constants
from pages.mainpage import MainPage
from pages.video import VideoPage
from datetime import datetime

from pages.wall import WallPost, VideoSelector

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

        main_page = MainPage(self.driver)
        main_page.open()
        main_page.authentificate(self.LOGIN, self.PASSWORD)
        if constants.MAKE_SCREENSHOTS:
            self.driver.save_screenshot(
                SCREENSHOT_PATH + 'login/{time}.png'.format(time=datetime.now().time().isoformat()))

    def test_going_to_videopage(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoPage(self.driver)

        video_page.wait_for_load()
        print self.driver.current_url

        self.assertEquals(self.driver.current_url, constants.BASE_URL + 'video/top')

        if constants.MAKE_SCREENSHOTS:
            self.driver.save_screenshot(
                SCREENSHOT_PATH + 'videopage/{time}.png'.format(time=datetime.now().time().isoformat()))

    def test_post_video(self):
        main_page = MainPage(self.driver)
        main_page.open_note()

        wall_post = WallPost(self.driver)
        wall_post.wait_load()
        wall_post.open_video_select_dialog()

        video_page = VideoSelector(self.driver)
        video_page.wait_load()
        video_page.select_first()

        wall_post.check_exist_video()
        wall_post.post()

    def tearDown(self):
        main_page = MainPage(self.driver)
        main_page.hard_clear_authentification()
        self.driver.refresh()
        if constants.MAKE_SCREENSHOTS:
            self.driver.save_screenshot(
                SCREENSHOT_PATH + 'sessionreset/{time}.png'.format(time=datetime.now().time().isoformat()))
        self.driver.quit()
