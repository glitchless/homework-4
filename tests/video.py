from os import environ
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest

import constants
from pages.mainpage import MainPage
from pages.upload import UploadPage
from pages.video_list import VideoListPage
from pages.video import VideoPage
from datetime import datetime

from pages.wall import WallPost, VideoSelector

SCREENSHOT_PATH = constants.SCREENSHOT_PATH + '/video/'


class VideoTest(unittest.TestCase):
    LOGIN = environ['LOGIN']  # type: str
    PASSWORD = environ['PASSWORD']  # type: str
    driver = None  # type: webdriver.Remote
    TEST_VIDEO_ID = 566094269061

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

        video_page = VideoListPage(self.driver)

        video_page.wait_for_load()

        self.assertEquals(self.driver.current_url, constants.BASE_URL + VideoListPage.PATH + 'top')

        if constants.MAKE_SCREENSHOTS:
            self.driver.save_screenshot(
                SCREENSHOT_PATH + 'videopage/{time}.png'.format(time=datetime.now().time().isoformat()))

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_post_video(self):
        main_page = MainPage(self.driver)
        main_page.open_note()

        wall_post = WallPost(self.driver)
        wall_post.open_video_select_dialog()

        video_page = VideoSelector(self.driver)
        video_page.select_first()

        wall_post.check_exist_video()
        wall_post.post()

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_scrolling_loads_videos(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoListPage(self.driver)

        videos_portion_count = video_page.video_count

        video_page.scroll_videos_to(1000000)

        # check that a video, that wasn't there, is now loaded
        video = video_page.wait_and_get_video_by_num(videos_portion_count + 1)

        self.assertTrue(video, 'Didn`t load videos on scroll')

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_upload_video(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoListPage(self.driver)
        video_page.open_video_upload()

        upload_page = UploadPage(self.driver)
        upload_page.upload_file()
        video_page.wait_load()
        video_page.wait_noload()

        video_page.wait_and_get_video_by_num(0)

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_video_watch_later(self):
        video_list_page = VideoListPage(self.driver)
        video_page = VideoPage(self.driver)

        video_list_page.open_watchlater()

        test_vid_in_watchlater = self.TEST_VIDEO_ID in video_list_page.video_ids

        if test_vid_in_watchlater:
            video_page.open_by_id(self.TEST_VIDEO_ID)
            video_page.toggle_watch_later()

            video_list_page.open_watchlater()

            self.assertNotIn(self.TEST_VIDEO_ID, video_list_page.video_ids,
                             'Didn`t remove video from watch later page on removing it from watch later')

        video_page.open_by_id(self.TEST_VIDEO_ID)

        video_page.toggle_watch_later()

        video_list_page.open_watchlater()

        self.assertIn(self.TEST_VIDEO_ID, video_list_page.video_ids,
                      'Didn`t add video to watch later page on marking it watch later')

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
                SCREENSHOT_PATH + 'clear/{time}.png'.format(time=datetime.now().time().isoformat()))
        cls.driver.quit()
