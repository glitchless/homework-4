# coding=utf-8
from page import Page
from os import environ
from component import Component


class MainPage(Page):
    PATH = ''
    _VIDEOPAGE_BUTTON = '//*[@id="hook_Block_TopMenuVideo"]/div/div[2]/div'

    def go_to_videos(self):
        self.driver.find_element_by_xpath(self._VIDEOPAGE_BUTTON).click()

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
    _SUBMIT_BUTTON = '//input[@value="Войти"]'

    def set_login(self, login):
        self.driver.find_element_by_xpath(self._LOGIN_FIELD).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self._PASSWORD_FIELD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self._SUBMIT_BUTTON).click()