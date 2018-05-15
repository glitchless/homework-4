from selenium.webdriver import Remote


class Component(object):
    def __init__(self, driver):
        # type: (Remote) -> None
        self.driver = driver
