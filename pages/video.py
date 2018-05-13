# coding=utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page import Page
from os import environ
from component import Component
import constants
from utils import awaited_property, wait_and_get_element


class VideoPage(Page):
    PATH = 'video/'
    _HOOK_BLOCK = '//*[@id="hook_Block_VideoVitrinaContent"]'
    _VIDEO_LIST = '//*[@id="vv_main_content"]/div/div/div[1]'
    _VIDEO_SCROLL_LIST = '//*[@id="layer_main_cnt_scroll"]'
    _VIDEO_BY_NUM = '//*[@id="vv_main_content"]/div/div/div[1]/div[{num}]'

    def wait_for_load(self):
        self.wait_and_get_hook_block

    @awaited_property
    def video_list(self):
        pass

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
        return wait_and_get_element(self, self._VIDEO_BY_NUM.format(num=num))

    def scroll_videos_to(self, y):
        self.driver.execute_script('document.evaluate(`{xpath}`, document).iterateNext().scrollTo(0, {to})'
                            .format(xpath=self._VIDEO_SCROLL_LIST, to=y))
