# coding=utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page import Page
from os import environ
from component import Component
import constants
from utils import awaited_property


class VideoPage(Page):
    PATH = 'video/'
    _HOOK_BLOCK = '//*[@id="hook_Block_VideoVitrinaContent"]'

    def wait_for_load(self):
        self.hook_block

    @awaited_property
    def hook_block(self):
        pass


# video_page = VideoPage(None)
# print video_page.HOOK_BLOCK