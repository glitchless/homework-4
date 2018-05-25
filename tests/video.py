# coding=utf-8
from os import environ
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest
import router

import constants
from pages.mainpage import MainPage
from pages.video_list import VideoListPage
from pages.video import VideoPage
from pages.wall import WallPost, VideoSelector
from utils import print_test_info

SCREENSHOT_PATH = constants.SCREENSHOT_PATH + '/video/'


class VideoTest(unittest.TestCase):
    LOGIN = environ['LOGIN']  # type: strТ
    PASSWORD = environ['PASSWORD']  # type: str
    driver = None  # type: webdriver.Remote
    TEST_VIDEO_ID = 657791912610
    TEST_EXTERNAL_VIDEO_LINK = 'https://www.youtube.com/watch?v=OPf0YbXqDm0'

    @classmethod
    def setUpClass(cls):
        browser = environ.get('BROWSER', 'CHROME')

        cls.driver = webdriver.Remote(
            command_executor=constants.COMMAND_EXECUTOR,
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        router.Router(driver=cls.driver)

    def setUp(self):
        self.driver.refresh()
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

        self.assertEqual(self.driver.current_url, constants.BASE_URL + VideoListPage.PATH + 'top')

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
    def test_post_multiple_videos(self):
        main_page = MainPage(self.driver)
        main_page.open_note()

        wall_post = WallPost(self.driver)

        expected_video_count = 2
        for i in range(expected_video_count):
            wall_post.open_video_select_dialog()
            video_selector = VideoSelector(self.driver)
            video_selector.select_first()

        added_video_count = wall_post.get_added_blocks_count()

        self.assertTrue(added_video_count == expected_video_count)

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_post_video_with_text(self):
        """
        Описание: Можно добавить видео к посту через диалог и опубликовать его (с текстом)
        """
        main_page = MainPage(self.driver)
        main_page.open_note()

        wall_post = WallPost(self.driver)
        wall_post.write_post("Post")
        wall_post.open_video_select_dialog()

        video_page = VideoSelector(self.driver)
        video_page.select_first()
        wall_post.post()

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_post_video_with_text_smile(self):
        """
        Описание: Можно добавить видео к посту через диалог и опубликовать его (со смайлом)
        """
        main_page = MainPage(self.driver)
        main_page.open_note()

        wall_post = WallPost(self.driver)
        wall_post.write_post("Post")
        wall_post.open_smile_list()
        wall_post.add_smile_totext()
        wall_post.close_smile_list()
        wall_post.open_video_select_dialog()

        video_page = VideoSelector(self.driver)
        video_page.select_first()
        wall_post.post()

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_post_video_with_smile(self):
        """
        Описание: Можно добавить видео к посту через диалог и опубликовать его (со смайлом)
        """
        main_page = MainPage(self.driver)
        main_page.open_note()

        wall_post = WallPost(self.driver)
        wall_post.open_smile_list()
        wall_post.add_smile_totext()
        wall_post.close_smile_list()
        wall_post.open_video_select_dialog()

        video_page = VideoSelector(self.driver)
        video_page.select_first()
        wall_post.post()

    @unittest.skip("WIP")
    def test_outer_post_upload_video(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()
        video_list_page = VideoListPage(self.driver)
        video = video_list_page.wait_and_get_video_by_num(0)
        before_video_id = video.get_attribute('data-id')

        main_page.go_to_main()
        wall_post = WallPost(self.driver)
        attach_video_input = wall_post.get_attach_video_input()
        attach_video_input.send_keys('content/video.mp4')

        video_list_page = VideoListPage(self.driver)
        video = video_list_page.wait_and_get_video_by_num(0)
        after_video_id = video.get_attribute('data-id')

        self.assertFalse(before_video_id == after_video_id)

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
    def test_external_upload_video_and_delete_video(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_list_page = VideoListPage(self.driver)

        router.Router().open_my_videos_by_url()

        video_count_initial = video_list_page.video_count

        video_upload_dialog = video_list_page.open_video_upload_dialog()

        video_upload_dialog.open_external_upload_dialog()

        video_upload_dialog.add_external_video(self.TEST_EXTERNAL_VIDEO_LINK)

        video_list_page.wait_until_popup_is_closed()

        video = video_list_page.wait_and_get_video_by_num(0)

        self.assertEqual(video_count_initial + 1, video_list_page.video_count, 'Video wasn`t added')
        video_id = video.get_attribute('data-id')

        video_list_page.delete_video(video)
        video_ids_after_delete = video_list_page.video_ids

        self.assertNotIn(video_id, video_ids_after_delete, 'Video was not removed')
        self.assertEqual(video_count_initial, video_list_page.video_count)

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_upload_video(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoListPage(self.driver)

        router.Router().open_my_videos_by_url()
        video_count_initial = video_page.video_count
        upload_page = video_page.open_video_upload_dialog()

        upload_page.upload_file()
        video_page.wait_load()
        video_page.wait_noload()

        video_count_second = video_page.video_count
        video = video_page.wait_and_get_video_by_num(0)

        self.assertEqual(video_count_initial + 1, video_count_second)

        video_page.delete_video(video)

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_attach_video_message(self):
        main_page = MainPage(self.driver)

        message_page = main_page.go_to_message()
        message_page.open_first_dialog()

        selector = message_page.open_video_dialog()
        selector.select_first()

        initial_message_count = message_page.message_count()
        message_page.send()
        second_message_count = message_page.message_count()

        self.assertTrue(second_message_count > initial_message_count,
                        "{0} !> {1}".format(second_message_count, initial_message_count))

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_comment_stream(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoPage(self.driver)
        video_page_list = VideoListPage(self.driver)

        router.Router().open_live()
        video_page_list.wait_open_stream()

        video = video_page_list.wait_and_get_video_by_num(0)

        video_page.open_by_id(video.get_attribute('data-id'))
        video_page.watch_video()
        video_page.send_comment('Test{0}'.format(self.LOGIN))
        video_page.find_comment_with_text('Test{0}'.format(self.LOGIN))

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_open_video(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoPage(self.driver)
        video_page_list = VideoListPage(self.driver)

        router.Router().open_new()
        video = video_page_list.wait_and_get_video_by_num(0)
        video_page.open_by_id(video.get_attribute('data-id'))
        video_page.watch_video()

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_subscription(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoListPage(self.driver)
        router.Router().open_subscriptions()
        initial_count = video_page.count_subscribtions()

        video_page.search('Test')
        video_page.wait_open_search()
        video_page.subscribe()

        router.Router().open_subscriptions()
        second_count = video_page.count_subscribtions()

        self.assertEqual(initial_count + 1, second_count,
                         "Not equals: {0} + 1 != {1}".format(initial_count, second_count))

        initial_count = second_count

        video_page.search('Test')
        video_page.wait_open_search()
        video_page.unsubscribe()

        router.Router().open_subscriptions()
        second_count = video_page.count_subscribtions()

        self.assertEqual(initial_count - 1, second_count,
                         "Not equals: {0} - 1 != {1}".format(initial_count, second_count))

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_comment_video(self):
        video_page = VideoPage(self.driver)
        video_page.open_by_id(self.TEST_VIDEO_ID)

        video_page.send_comment('Test{0}'.format(self.LOGIN))
        element = video_page.find_comment_with_text('Test{0}'.format(self.LOGIN))
        video_page.remove_comment(element)

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_open_stream(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoPage(self.driver)
        video_page_list = VideoListPage(self.driver)

        router.Router().open_live()
        video = video_page_list.wait_and_get_video_by_num(0)
        video_page.open_by_id(video.get_attribute('data-id'))
        video_page.watch_video()

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_search(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoListPage(self.driver)
        video_page.search('Test')
        video_page.wait_open_search()
        video_id = int(video_page.wait_and_get_video_by_num(0).get_attribute('data-id'))
        self.assertEqual(video_id, 1691355875,
                         'First video need be https://ok.ru/video/1691355875 by "Test" request. Not {0}'.format(
                             video_id))

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_tab_change(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        router.Router().open_top()
        self.assertEqual(self.driver.current_url, "{0}video/{1}".format(constants.BASE_URL, 'top'))

        router.Router().open_liveapp()
        self.assertEqual(self.driver.current_url, "{0}video/{1}".format(constants.BASE_URL, 'liveApp'))

        router.Router().open_new()
        self.assertEqual(self.driver.current_url, "{0}video/{1}".format(constants.BASE_URL, 'new'))

        router.Router().open_live()
        self.assertEqual(self.driver.current_url, "{0}video/{1}".format(constants.BASE_URL, 'live'))

        router.Router().open_suggest()
        self.assertEqual(self.driver.current_url, "{0}video/{1}".format(constants.BASE_URL, 'suggestedAlbums'))

        router.Router().open_catalog()
        self.assertEqual(self.driver.current_url, "{0}video/{1}".format(constants.BASE_URL, 'channels'))

        router.Router().open_my_videos()
        self.assertEqual(self.driver.current_url, "{0}video/{1}".format(constants.BASE_URL, 'myVideo'))

        router.Router().open_subscriptions()
        self.assertEqual(self.driver.current_url, "{0}video/{1}".format(constants.BASE_URL, 'subscriptions'))

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_video_watch_later(self):
        video_list_page = VideoListPage(self.driver)
        video_page = VideoPage(self.driver)

        router.Router().open_watchlater()

        test_vid_in_watchlater = self.TEST_VIDEO_ID in video_list_page.video_ids

        if test_vid_in_watchlater:
            video_page.open_by_id(self.TEST_VIDEO_ID)
            video_page.toggle_watch_later()

            router.Router().open_watchlater()

            self.assertNotIn(self.TEST_VIDEO_ID, video_list_page.video_ids,
                             'Didn`t remove video from watch later page on removing it from watch later')

        video_page.open_by_id(self.TEST_VIDEO_ID)

        video_page.toggle_watch_later()

        router.Router().open_watchlater()

        self.assertIn(self.TEST_VIDEO_ID, video_list_page.video_ids,
                      'Didn`t add video to watch later page on marking it watch later')

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_video_get_link(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoPage(self.driver)
        video_page_list = VideoListPage(self.driver)

        router.Router().open_new()
        video = video_page_list.wait_and_get_video_by_num(0)

        video_id = video.get_attribute('data-id')
        video_page.open_by_id(video_id)
        video_page.get_video_player().click()
        video_url = video_page.get_video_link()

        self.driver.get(video_url)
        video_page = VideoPage(self.driver)

        self.assertEqual(video_id, video_page.get_video_id())

    @unittest.skipIf(constants.SKIP_FINISHED_TESTS, '')
    def test_can_add_and_remove_like(self):
        main_page = MainPage(self.driver)
        main_page.go_to_videos()

        video_page = VideoPage(self.driver)
        video_page_list = VideoListPage(self.driver)

        router.Router().open_new()
        video = video_page_list.wait_and_get_video_by_num(0)

        video_id = video.get_attribute('data-id')
        video_page.open_by_id(video_id)

        like_button = video_page.get_like_button()
        like_button.click()

        self.driver.refresh()

        video_page = VideoPage(self.driver)

        like_button_container = video_page.get_like_button_container()
        entry = '__active' in like_button_container.get_attribute('class')

        video_page.get_like_button().click()

        self.assertTrue(entry)

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
