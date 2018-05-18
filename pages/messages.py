from selenium.common.exceptions import WebDriverException

from pages.page import Page
from pages.wall import VideoSelector
from utils import wait_and_get_element


class MessagePage(Page):
    _DIALOG_BUTTON = '//a[@class="chats_i_ovr"]'
    _ATTACH_BUTTON = '//span[@class="comments_attach_trigger __new"]'
    _ATTACH_MENU = '//div[@class="sc-menu sc-menu__top"]'
    _ATTACH_MENU_HIDDEN = '//div[@class="sc-menu sc-menu__top sc-menu__hidden"]'
    _VIDEO_ADD_BUTTON = '//a[@data-l="t,videoLink"]'
    _DIALOG_FIELD = '//div[@class="js-messages-list"]/div/div'
    _SEND_BUTTON = '//button[@class="button-pro comments_add-controls_save"]'

    def open_first_dialog(self):
        wait_and_get_element(self, self._DIALOG_BUTTON).click()

    def open_video_dialog(self):
        wait_and_get_element(self, self._ATTACH_BUTTON).click()
        wait_and_get_element(self, self._ATTACH_MENU)

        try:
            self.driver.execute_script(
                'document.evaluate(`{xpath}`, document).iterateNext().classList.remove(`sc-menu__hidden`)'.format(
                    xpath=self._ATTACH_MENU_HIDDEN))
        except WebDriverException:
            pass

        wait_and_get_element(self, self._VIDEO_ADD_BUTTON).click()

        return VideoSelector(self.driver)

    def message_count(self):
        return len(self.driver.find_elements_by_xpath(self._DIALOG_FIELD))

    def send(self):
        wait_and_get_element(self, self._SEND_BUTTON).click()
