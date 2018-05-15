from urlparse import urljoin

from constants import BASE_URL
from pages.component import Component
from pages.page import Page
from pages.video_list import VideoListPage
from utils import wait_and_get_element, same_urls


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Router(object):
    __metaclass__ = Singleton

    def __init__(self, driver=None):
        if driver:
            self.driver = driver

    _WATCHLATER_BUTTON = '//*[@id="vv_btn_watchLater"]'

    MY_VIDEO_INNERPATHS = [
        urljoin(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.MY_VIDEO_PATH),
        urljoin(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.WATCH_LATER_PATH),
    ]

    @property
    def is_on_myvideos_page(self):
        return bool(filter(lambda url: same_urls(self.driver.current_url, url), self.MY_VIDEO_INNERPATHS))

    def open_my_videos_by_url(self):
        self.open(VideoListPage.MY_VIDEO_PATH, VideoListPage)

    def open_watchlater(self):
        self.open_my_videos_by_url()
        wait_and_get_element(self, self._WATCHLATER_BUTTON).click()
        wait_and_get_element(self, self._WATCHLATER_BUTTON).click()  # HI OK devs

    def open(self, relative_url='', page=None):
        # type: (str, Page) -> None
        if page:
            url = urljoin(urljoin(page.BASE_URL, page.PATH), relative_url)
        else:
            url = urljoin(BASE_URL, relative_url)

        self.driver.get(url)
