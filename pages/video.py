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
    PATH = 'video/{id}'

    MY_VIDEO_PATH = 'myVideo/'

    _HOOK_BLOCK = '//*[@id="hook_Block_VideoVitrinaContent"]'
    _VIDEO_LIST = '//*[@id="vv_main_content"]/div/div/div[1]'
    _VIDEO_SCROLL_LIST = '//*[@id="layer_main_cnt_scroll"]'
    _VIDEO_BY_NUM = '//*[@id="vv_main_content"]/div/div/div[1]/div[{num}]'

    def open(self, relative_url=''):
        raise NotImplemented('Can`t open a video without an id')

    def open_by_id(self, video_id):
        # type: (int) -> None
        super(VideoPage, self).open(str(video_id))

