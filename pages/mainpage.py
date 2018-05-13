# coding=utf-8
from page import Page
from os import environ
from component import Component


class MainPage(Page):
    PATH = ''
    FEED_BUTTON = '//a[@href="/feed"]'

    def go_to_feed(self):
        self.driver.find_element_by_xpath(self.FEED_BUTTON).click()

    def authentificate(self, login=environ['LOGIN'], password=environ['PASSWORD']):
        auth_form = AuthForm(self.driver)

        auth_form.set_login(login)
        auth_form.set_password(password)
        auth_form.submit()


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