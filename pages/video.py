# coding=utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page import Page
from os import environ
from component import Component
import constants


class VideoPage(Page):
    PATH = ''
    _HOOK_BLOCK = '//*[@id="hook_Block_VideoVitrinaContent"]'

    def wait_for_load(self):
        WebDriverWait(self.driver, constants.WAIT_TIME).until(
            expected_conditions.visibility_of_element_located((By.XPATH, self._HOOK_BLOCK))
        )
