# coding=utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import constants
from component import Component


class WallPost(Component):
    _TEXT_FIELD = '//div[@class="posting_cnt"]'
    _VIDEO_ADD_BUTTON = '//*[@data-id="Status_add_video"]'
    _VIDEO_COMPONENT = '//div[@class="posting-form_sctn"]/div[@class="vid-card vid-card__xl"]'
    _SUBMIT_BUTTON = '//div[@class="posting_submit button-pro"]'

    def wait_load(self):
        WebDriverWait(self.driver, constants.WAIT_TIME).until(
            expected_conditions.visibility_of_element_located((By.XPATH, self._TEXT_FIELD))
        )

    def open_video_select_dialog(self):
        self.driver.find_element_by_xpath(self._VIDEO_ADD_BUTTON).click()

    def check_exist_video(self):
        self.driver.find_element_by_xpath(self._VIDEO_COMPONENT)

    def post(self):
        self.driver.find_element_by_xpath(self._SUBMIT_BUTTON).click()


class VideoSelector(Component):
    _VIDEO_FIRST_BUTTON = '//div[@class="vid-card_cnt"]'
    _MODAL_FIELD = '//div[@class="modal-new_cnt"]'

    def wait_load(self):
        WebDriverWait(self.driver, constants.WAIT_TIME).until(
            expected_conditions.visibility_of_element_located((By.XPATH, self._MODAL_FIELD))
        )

    def select_first(self):
        self.driver.find_element_by_xpath(self._VIDEO_FIRST_BUTTON).click()
