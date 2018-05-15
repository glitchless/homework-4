# coding=utf-8
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page import Page
from os import environ
from component import Component
import constants
from utils import awaited_property, wait_and_get_element


class VideoPage(Page):
    PATH = 'video/{id}'

    _HOOK_BLOCK = '//*[@id="hook_Block_VideoVitrinaContent"]'
    _VIDEO_LIST = '//*[@id="vv_main_content"]/div/div/div[1]'
    _VIDEO_SCROLL_LIST = '//*[@id="layer_main_cnt_scroll"]'
    _VIDEO_BY_NUM = '//*[@id="vv_main_content"]/div/div/div[1]/div[{num}]'
    _VIDEO_UPLOAD_BUTTON = '//div[@class="vl_add-video"]'
    _VIDEO_WATCH_LATER_BUTTON = '//*[@al-click="watchLater()"]'
    _VIDEO_PLAYER = '//*[@id="VideoAutoplayPlayerE"]/div/div[2]/video'

    def wait_for_load(self):
        self.wait_and_get_hook_block

    def open(self, relative_url=''):
        raise NotImplemented('Can`t open a video without an id')

    def open_by_id(self, video_id):
        # type: (int) -> None
        super(VideoPage, self).open(str(video_id))

    def toggle_watch_later(self):
        video = wait_and_get_element(self, self._VIDEO_PLAYER)
        hover = ActionChains(self.driver).move_to_element(video)
        hover.perform()
        wait_and_get_element(self, self._VIDEO_WATCH_LATER_BUTTON).click()

    @awaited_property('_HOOK_BLOCK')
    def wait_and_get_hook_block(self):  # то же, что и выше
        pass

    def wait_and_get_video_by_num(self, num):
        return wait_and_get_element(self, self._VIDEO_BY_NUM.format(num=num))

    def open_upload_video(self):
        wait_and_get_element(self, self._VIDEO_UPLOAD_BUTTON)

    def scroll_videos_to(self, y):
        self.driver.execute_script('document.evaluate(`{xpath}`, document).iterateNext().scrollTo(0, {to})'
                                   .format(xpath=self._VIDEO_SCROLL_LIST, to=y))
