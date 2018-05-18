from functools import partial

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from inspect import isroutine

import constants


def awaited_property(func_or_name, wait_for_visibility=True):
    # type: (function | str) -> property | function
    if isroutine(func_or_name):
        func = func_or_name
        name = '_' + str.upper(func.__name__)

        return property(fget=element_patient_getter(name))

    elif isinstance(func_or_name, str):
        name = func_or_name
        return lambda func: property(fget=element_patient_getter(name))

    else:
        raise TypeError('Argument is not a str or function')


def element_patient_getter(attr_name, wait_for_visibility=True):
    return partial(wait_and_get_property, attr_name=attr_name, wait_for_visibility=wait_for_visibility)


def wait_and_get_property(self, attr_name, wait_for_visibility=True):
    return wait_and_get_element(self, getattr(self, attr_name))


def wait_text(self, xpath, text):
    WebDriverWait(self.driver, constants.WAIT_TIME).until(
        expected_conditions.text_to_be_present_in_element((By.XPATH, xpath), text)
    )


def wait_and_get_element(self, xpath, wait_for_visibility=True, long_wait=False):
    # type: (any, str) -> WebElement
    wait_count = constants.WAIT_TIME
    if long_wait:
        wait_count = constants.LONG_WAIT_TIME

    if wait_for_visibility:
        WebDriverWait(self.driver, wait_count).until(
            expected_conditions.visibility_of_element_located((By.XPATH, xpath))
        )
    else:
        WebDriverWait(self.driver, wait_count).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )

    return self.driver.find_element_by_xpath(xpath)


def canonical_url(u):
    u = u.lower()
    if u.endswith("/"):
        u = u[:-1]
    return u


def same_urls(u1, u2):
    return canonical_url(u1) == canonical_url(u2)


def start_with_url(u1, u2):
    return canonical_url(u1).startswith(canonical_url(u2))
