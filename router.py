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
    _MYWIDEO_BUTTON = '//a[@id="vv_btn_myVideo"]'
    _TOP_BUTTON = '//a[@id="vv_btn_top"]'
    _LIVEAPP_BUTTON = '//a[@id="vv_btn_liveApp"]'
    _NEW_BUTTON = '//a[@id="vv_btn_new"]'
    _LIVE_BUTTON = '//a[@id="vv_btn_live"]'
    _SUGGEST_BUTTON = '//a[@id="vv_btn_suggestedAlbums"]'
    _CATALOG_BUTTON = '//a[@id="vv_btn_channels"]'
    _SUBSCRIPTIONS_BUTTON = '//a[@id="vv_btn_subscriptions"]'

    MY_VIDEO_INNERPATHS = [
        urljoin(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.MY_VIDEO_PATH),
        urljoin(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.WATCH_LATER_PATH),
    ]

    @property
    def is_on_myvideos_page(self):
        return bool(filter(lambda url: same_urls(self.driver.current_url, url), self.MY_VIDEO_INNERPATHS))

    @property
    def is_on_search_page(self):
        return same_urls(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.SEARCH_PATH)

    def open_my_videos_by_url(self):
        self.open(VideoListPage.MY_VIDEO_PATH, VideoListPage)

    def open_my_videos(self):
        wait_and_get_element(self, self._MYWIDEO_BUTTON).click()

    def open_top(self):
        wait_and_get_element(self, self._TOP_BUTTON).click()

    def open_liveapp(self):
        wait_and_get_element(self, self._LIVEAPP_BUTTON).click()

    def open_suggest(self):
        wait_and_get_element(self, self._SUGGEST_BUTTON).click()

    def open_new(self):
        wait_and_get_element(self, self._NEW_BUTTON).click()

    def open_catalog(self):
        wait_and_get_element(self, self._CATALOG_BUTTON).click()

    def open_subscriptions(self):
        wait_and_get_element(self, self._SUBSCRIPTIONS_BUTTON).click()

    def open_live(self):
        wait_and_get_element(self, self._LIVE_BUTTON).click()

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
