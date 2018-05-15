# coding=utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page import Page
from os import environ
from component import Component
from urlparse import urljoin
import constants
from utils import awaited_property, wait_and_get_element, same_urls



class VideoListPage(Page):
    PATH = 'video/'

    MY_VIDEO_PATH = 'myVideo/'
    WATCH_LATER_PATH = 'watchLater/'

    MY_VIDEO_INNERPATHS = [
            urljoin(urljoin(Page.BASE_URL, PATH), MY_VIDEO_PATH),
            urljoin(urljoin(Page.BASE_URL, PATH), WATCH_LATER_PATH),
    ]

    _WATCHLATER_BUTTON = '//*[@id="vv_btn_watchLater"]'

    _HOOK_BLOCK = '//*[@id="hook_Block_VideoVitrinaContent"]'
    _VIDEO_LIST = '//*[@id="vv_main_content"]/div/div/div[1]'
    _VIDEO_SCROLL_LIST = '//*[@id="layer_main_cnt_scroll"]'
    _VIDEOS = '//*[@id="vv_main_content"]/div/div/div[1]/div[contains(concat(" ", normalize-space(@class), " "), " vid-card ")]'
    _VIDEO_BY_NUM = '//*[@id="vv_main_content"]/div/div/div[1]/div[contains(concat(" ", normalize-space(@class), " "), " vid-card ")][{num}]'

    _VIDEO_LIST_MYVIDEO = '//*[@id="vv_main_content"]/div/div'
    _VIDEOS_MYVIDEO = '//*[@id="vv_main_content"]/div/div/div[contains(concat(" ", normalize-space(@class), " "), " vid-card ")]'
    _VIDEO_BY_NUM_MYVIDEO = '//*[@id="vv_main_content"]/div/div/div[contains(concat(" ", normalize-space(@class), " "), " vid-card ")][{num}]'

    @property
    def is_on_myvideos_page(self):
        return bool(filter(lambda url: same_urls(self.driver.current_url, url), self.MY_VIDEO_INNERPATHS))

    def open_my_videos_by_url(self):
        self.open(self.MY_VIDEO_PATH)

    def open_watchlater(self):
        self.open_my_videos_by_url()
        wait_and_get_element(self, self._WATCHLATER_BUTTON).click()

    def wait_for_load(self):
        self.wait_and_get_hook_block

    @property
    def video_list(self):
        if self.is_on_myvideos_page:
            return wait_and_get_element(self, self._VIDEO_LIST_MYVIDEO)

        return wait_and_get_element(self, self._VIDEO_LIST)


    @awaited_property
    def video_scroll_list(self):
        pass

    @awaited_property
    def hook_block(self):
        pass

    @awaited_property('_HOOK_BLOCK')
    def wait_and_get_hook_block(self):  # то же, что и выше
        pass

    def wait_and_get_video_by_num(self, num):
        if self.is_on_myvideos_page:
            return wait_and_get_element(self, self._VIDEO_BY_NUM_MYVIDEO.format(num=num + 1)) # нумерация в xpath с единицы

        return wait_and_get_element(self, self._VIDEO_BY_NUM.format(num=num + 1))  # нумерация в xpath с единицы

    def scroll_videos_to(self, y):
        self.driver.execute_script('document.evaluate(`{xpath}`, document).iterateNext().scrollTo(0, {to})'
                                   .format(xpath=self._VIDEO_SCROLL_LIST, to=y))

    @property
    def videos(self):
        self.video_list
        if self.is_on_myvideos_page:
            return self.driver.find_elements_by_xpath(self._VIDEOS_MYVIDEO)

        return self.driver.find_elements_by_xpath(self._VIDEOS)

    @property
    def video_count(self):
        return len(self.videos)

    @property
    def video_ids(self):
        return map(lambda node: int(node.get_attribute('data-id')), self.videos)
