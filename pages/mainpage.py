# coding=utf-8
from page import Page
from os import environ
from component import Component
from utils import wait_and_get_element


class MainPage(Page):
    PATH = ''
    _VIDEOPAGE_BUTTON = '//div[@class="toolbar_nav_a toolbar_nav_a__video"]'
    _NOTE_FIELD = '//div[@class="input_placeholder"]'

    def open_note(self):
        wait_and_get_element(self, self._NOTE_FIELD).click()

    def go_to_videos(self):
        wait_and_get_element(self, self._VIDEOPAGE_BUTTON).click()

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
    _SUBMIT_BUTTON = u'//*[@id="anonymPageContent"]/div[2]/div/div[3]/form/div[5]/div[1]/input'

    def set_login(self, login):
        self.driver.find_element_by_xpath(self._LOGIN_FIELD).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self._PASSWORD_FIELD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self._SUBMIT_BUTTON).click()
