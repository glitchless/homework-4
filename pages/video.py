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

    _VIDEO_WATCH_LATER_BUTTON = '//*[@al-click="watchLater()"]'
    _VIDEO_PLAYER = '//*[@id="VideoAutoplayPlayerE"]/div/div[2]/video'

    def open(self, relative_url=''):
        raise NotImplemented('Can`t open a video without an id')

    def open_by_id(self, video_id):
        # type: (int) -> None
        super(VideoPage, self).open(str(video_id))

    def toggle_watch_later(self):  # WARNING: MAY CAUSE SIDE EFFECTS
        wait_and_get_element(self, self._VIDEO_PLAYER).click()
        wait_and_get_element(self, self._VIDEO_WATCH_LATER_BUTTON).click()
        wait_and_get_element(self, self._VIDEO_PLAYER).click()
