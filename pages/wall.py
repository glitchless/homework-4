# coding=utf-8
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import constants
from component import Component
from utils import wait_and_get_element, awaited_property


class WallPost(Component):
    _VIDEO_ADD_BUTTON = '//*[@id="hook_Block_MediaStatusLayerBody"]/div[1]/div[2]/div/div[7]/div/div/div/div[2]/div[2]/div'
    _VIDEO_COMPONENT = '//*[@class="hookBlock"]/div/div'
    _SUBMIT_BUTTON = '//div[@class="posting_submit button-pro"]'
    _ATTACH_BUTTONS = '//div[@class="posting_ac"]'


    # Говнофикс бага с не кликающим элементом
    def open_video_select_dialog(self):
        print('open_video_select_dialog')
        not_open = True
        one_execute = False  # Проверка что хотя бы один раз элемент проверился

        while not_open:
            try:
                one_execute = True
                wait_and_get_element(self, self._VIDEO_ADD_BUTTON).click()
            except WebDriverException as e:
                if not one_execute:
                    raise e
                not_open = False

    def check_exist_video(self):
        self.driver.find_element_by_xpath(self._VIDEO_COMPONENT)

    def post(self):
        wait_and_get_element(self, self._SUBMIT_BUTTON).click()


class VideoSelector(Component):
    _VIDEO_FIRST_BUTTON = '//div[@class="vid-card_cnt"]'

    def select_first(self):
        self.video_first_button.click()

    @awaited_property
    def video_first_button(self):
        pass
