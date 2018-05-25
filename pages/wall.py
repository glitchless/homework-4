# coding=utf-8
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import constants
from .component import Component
from utils import wait_and_get_element, awaited_property


class WallPost(Component):
    _VIDEO_ADD_BUTTON = '//div[@data-id="Status_add_video"]'
    _VIDEO_COMPONENT = '//*[@class="hookBlock"]/div/div'
    _SUBMIT_BUTTON = '//div[@class="posting_submit button-pro"]'
    _ATTACH_BUTTONS = '//div[@class="posting_ac"]'
    _ATTACH_VIDEO_BUTTON = '//span[@data-l="t,pf_video_button"]'
    _ATTACH_VIDEO_INPUT = '//span[@data-l="t,pf_video_button"]/input'
    _POST_TEXT = '//div[@data-module="postingForm/mediaText"]'

    # Говнофикс бага с не кликающим элементом
    def open_video_select_dialog(self):
        not_open = True
        one_execute = False  # Проверка что хотя бы один раз элемент проверился

        while not_open:
            try:
                wait_and_get_element(self, self._VIDEO_ADD_BUTTON).click()
                one_execute = True
            except WebDriverException as e:
                if not one_execute:
                    raise e
                not_open = False

    def check_exist_video(self):
        self.driver.find_element_by_xpath(self._VIDEO_COMPONENT)

    def get_added_blocks_count(self):
        return len(self.driver.find_elements_by_class_name('posting_block')) - 1

    def write_post(self, text):
        wait_and_get_element(self, self._POST_TEXT).send_keys(text)

    def empty(self):
        [element.click() for element in self.driver.find_elements_by_class_name('posting_close')]

    def get_attach_video_button(self):
        return wait_and_get_element(self, self._ATTACH_VIDEO_BUTTON)

    def get_attach_video_input(self):
        return wait_and_get_element(self, self._ATTACH_VIDEO_INPUT)

    def post(self):
        wait_and_get_element(self, self._SUBMIT_BUTTON).click()


class VideoSelector(Component):
    _VIDEO_FIRST_BUTTON = '//div[@class="vid-card_img_w"]'

    def select_first(self):
        self.video_first_button.click()

    @awaited_property
    def video_first_button(self):
        pass
