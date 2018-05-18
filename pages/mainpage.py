# coding=utf-8
from .page import Page
from os import environ
from .component import Component
from pages.messages import MessagePage
from utils import wait_and_get_element, awaited_property


class MainPage(Page):
    PATH = ''
    _MAIN_PAGE_BUTTON = '//*[@id="topPanelLeftCorner"]'
    _VIDEOPAGE_BUTTON = '//div[@class="toolbar_nav_a toolbar_nav_a__video"]'
    _MESSAGE_BUTTON = '//li[@data-l="t,messages"]'
    _NOTE_FIELD = '//div[@class="input_placeholder"]'
    _VIDEO_CONTENT = '//div[@class="js-loader-container clearfix"]'

    def open_note(self):
        wait_and_get_element(self, self._NOTE_FIELD).click()

    def go_to_main(self):
        wait_and_get_element(self, self._MAIN_PAGE_BUTTON).click()

    def go_to_videos(self):
        wait_and_get_element(self, self._VIDEOPAGE_BUTTON).click()
        wait_and_get_element(self, self._VIDEO_CONTENT)

    def go_to_message(self):
        wait_and_get_element(self, self._MESSAGE_BUTTON).click()
        return MessagePage(self.driver)

    def authentificate(self, login=environ['LOGIN'], password=environ['PASSWORD']):
        auth_form = AuthForm(self.driver)

        auth_form.set_login(login)
        auth_form.set_password(password)
        auth_form.submit()

    def hard_clear_authentification(self):
        self.driver.delete_all_cookies()


class AuthForm(Component):
    _LOGIN_FIELD = '//input[@name="st.email"]'
    _PASSWORD_FIELD = '//input[@name="st.password"]'
    _SUBMIT_BUTTON = '//*[@id="anonymPageContent"]/div[2]/div/div[3]/form/div[5]/div[1]/input'

    def set_login(self, login):
        wait_and_get_element(self, self._LOGIN_FIELD).send_keys(login)

    def set_password(self, pwd):
        wait_and_get_element(self, self._PASSWORD_FIELD).send_keys(pwd)

    def submit(self):
        wait_and_get_element(self, self._SUBMIT_BUTTON).click()
