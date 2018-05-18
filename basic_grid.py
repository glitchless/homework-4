# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import constants

if __name__ == '__main__':
    browser = os.environ.get('BROWSER', 'CHROME')
    login = os.environ['LOGIN']
    password = os.environ['PASSWORD']
    print(browser, login, password)
    driver = webdriver.Remote(
        command_executor=constants.COMMAND_EXECUTOR,
        desired_capabilities=getattr(DesiredCapabilities, browser).copy(),
    )
    driver.get("https://ok.ru/")
    driver.save_screenshot(constants.SCREENSHOT_PATH + 'scr.png')
    driver.quit()
