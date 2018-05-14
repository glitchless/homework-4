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
    LOGIN = environ['LOGIN']  # type: str
    PASSWORD = environ['PASSWORD']  # type: str
    driver = None  # type: webdriver.Remote

    @classmethod
    def setUpClass(cls):
        browser = environ.get('BROWSER', 'CHROME')

        cls.driver = webdriver.Remote(
            command_executor=constants.COMMAND_EXECUTOR,
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def setUp(self):
        main_page = MainPage(self.driver)
        main_page.open()
        main_page.authentificate(self.LOGIN, self.PASSWORD)
        if constants.MAKE_SCREENSHOTS:
            self.driver.save_screenshot(
                SCREENSHOT_PATH + 'login/{time}.png'.format(time=datetime.now().time().isoformat()))

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_going_to_videopage(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoPage(self.driver)

        video_page.wait_for_load()

        self.assertEquals(self.driver.current_url, constants.BASE_URL + VideoPage.PATH + 'top')

        if constants.MAKE_SCREENSHOTS:
            self.driver.save_screenshot(
                SCREENSHOT_PATH + 'videopage/{time}.png'.format(time=datetime.now().time().isoformat()))

    @unittest.skip('WIP')
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

    def test_scrolling_loads_videos(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoPage(self.driver)

        video_list = video_page.video_list

        videos_count = len(video_list.get_property('children'))

        video_page.scroll_videos_to(1000000)

        video_page.wait_and_get_video_by_num(videos_count + 1)

    def tearDown(self):
        main_page = MainPage(self.driver)
        main_page.hard_clear_authentification()
        self.driver.refresh()
        if constants.MAKE_SCREENSHOTS:
            self.driver.save_screenshot(
                SCREENSHOT_PATH + 'sessionreset/{time}.png'.format(time=datetime.now().time().isoformat()))

    @classmethod
    def tearDownClass(cls):
        if constants.MAKE_SCREENSHOTS:
            cls.driver.save_screenshot(
                SCREENSHOT_PATH + 'sessionreset/{time}.png'.format(time=datetime.now().time().isoformat()))
        cls.driver.quit()
