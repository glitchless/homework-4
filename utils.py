from functools import partial

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import constants


def awaited_property(func, name=None):
    if not name:
        name = '_' + str.upper(func.__name__)

    return property(fget=element_patient_getter(name))


def element_patient_getter(attr_name):
    return partial(wait_and_get_element, attr_name=attr_name)


def wait_and_get_element(self, attr_name):
    print(self)
    WebDriverWait(self.driver, constants.WAIT_TIME).until(
        expected_conditions.visibility_of_element_located((By.XPATH, getattr(self, attr_name)))
    )

    self.driver.find_element_by_xpath(getattr(self, attr_name))
    return
