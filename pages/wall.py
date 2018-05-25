# coding=utf-8
import random

from selenium.common.exceptions import WebDriverException, ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import constants
from .component import Component
from utils import wait_and_get_element, awaited_property


class WallPost(Component):
    _VIDEO_ADD_BUTTON = '//div[@class="posting_ac"]/div[2]/div'
    _VIDEO_COMPONENT = '//*[@class="hookBlock"]/div/div'
    _SUBMIT_BUTTON = '//div[@class="posting_submit button-pro"]'
    _ATTACH_BUTTONS = '//div[@class="posting_ac"]'
    _ATTACH_VIDEO_BUTTON = '//span[@data-l="t,pf_video_button"]'
    _ATTACH_VIDEO_INPUT = '//span[@data-l="t,pf_video_button"]/input'
    _POST_TEXT = '//div[@data-module="postingForm/mediaText"]'
    _POST_SMILE = '//span[@id="hook_Block_smnull"]'
    _POST_DIVS = '//div[@class="feed-list"]/div'
    _POST_SMILE_LIST = '//span[@id="hook_Block_smnull"]/div'
    _POST_SMILE_SELECT = '//div[@class="comments_smiles_set"]/ul/li[@class="comments_smiles_i"]'

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
        return len(self.driver.find_elements_by_xpath(self._POST_DIVS))

    def write_post(self, text):
        wait_and_get_element(self, self._POST_TEXT).send_keys(text)

    def close_smile_list(self):
        wait_and_get_element(self, self._POST_SMILE)
        self.driver.execute_script(
            'document.evaluate(`{xpath}`, document).iterateNext().dispatchEvent(new Event("mouseout"))'.format(
                xpath=self._POST_SMILE))
        WebDriverWait(self.driver, constants.WAIT_TIME).until(
            expected_conditions.invisibility_of_element_located((By.XPATH, self._POST_SMILE_LIST))
        )

    def open_smile_list(self):
        wait_and_get_element(self, self._POST_SMILE).click()

    def add_smile_totext(self):
        wait_and_get_element(self, self._POST_SMILE_LIST)
        self.select_random_smile_and_open()

    def select_random_smile_and_open(self):
        try:
            smile_list = self.driver.find_elements_by_xpath(self._POST_SMILE_SELECT)
            element = random.choice(smile_list)
            element.click()
        except ElementNotVisibleException:
            self.select_random_smile_and_open()

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
