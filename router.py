# coding=utf-8
from urllib.parse import urljoin

from selenium.common.exceptions import StaleElementReferenceException

from constants import BASE_URL
from pages.component import Component
from pages.page import Page
from pages.video_list import VideoListPage
from utils import wait_and_get_element, same_urls, start_with_url, wait_text


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Router(object, metaclass=Singleton):
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
    _TAB_NAME_TEXT = '//div[@class="mml_ucard_n_g"]'
    _SUBSCRIPTIONS_BUTTON = '//a[@id="vv_btn_subscriptions"]'

    MY_VIDEO_INNERPATHS = [
        urljoin(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.MY_VIDEO_PATH),
        urljoin(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.WATCH_LATER_PATH),
    ]

    @property
    def is_on_myvideos_page(self):
        return bool([url for url in self.MY_VIDEO_INNERPATHS if same_urls(self.driver.current_url, url)])

    @property
    def is_on_search_page(self):
        return same_urls(self.driver.current_url,
                         urljoin(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.SEARCH_PATH))

    @property
    def is_on_new_page(self):
        return same_urls(self.driver.current_url,
                         urljoin(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.NEW_PATH))

    @property
    def is_stream(self):
        return start_with_url(self.driver.current_url, urljoin(VideoListPage.BASE_URL, VideoListPage.PATH_LIVE))

    @property
    def is_on_live_page(self):
        return same_urls(self.driver.current_url,
                         urljoin(urljoin(VideoListPage.BASE_URL, VideoListPage.PATH), VideoListPage.LIVE_PATH))

    def open_my_videos_by_url(self):
        self.open(VideoListPage.MY_VIDEO_PATH, VideoListPage)

    def open_my_videos(self):
        """
        author: LionZXY
        """
        wait_and_get_element(self, self._MYWIDEO_BUTTON).click()
        wait_text(self, self._TAB_NAME_TEXT, "Моё видео")

    def open_top(self):
        """
        author: LionZXY
        """
        wait_and_get_element(self, self._TOP_BUTTON).click()
        wait_text(self, self._TAB_NAME_TEXT, "Топ недели")

    def open_liveapp(self):
        """
        author: LionZXY
        """
        wait_and_get_element(self, self._LIVEAPP_BUTTON).click()
        wait_text(self, self._TAB_NAME_TEXT, "OK Live")

    def open_suggest(self):
        """
        author: LionZXY
        """
        wait_and_get_element(self, self._SUGGEST_BUTTON).click()
        wait_text(self, self._TAB_NAME_TEXT, "Популярное")

    def open_new(self):
        """
        author: LionZXY
        """
        wait_and_get_element(self, self._NEW_BUTTON).click()
        wait_text(self, self._TAB_NAME_TEXT, "Новинки")

    def open_catalog(self):
        """
        author: LionZXY
        """
        wait_and_get_element(self, self._CATALOG_BUTTON).click()
        wait_text(self, self._TAB_NAME_TEXT, "Каталог")

    def open_subscriptions(self):
        """
        author: LionZXY
        """
        wait_and_get_element(self, self._SUBSCRIPTIONS_BUTTON).click()
        wait_text(self, self._TAB_NAME_TEXT, "Мои подписки")

    def open_live(self):
        """
        author: LionZXY
        """
        wait_and_get_element(self, self._LIVE_BUTTON).click()
        wait_text(self, self._TAB_NAME_TEXT, "Прямой эфир")

    def open_watchlater(self):
        self.open_my_videos_by_url()
        wait_and_get_element(self, self._WATCHLATER_BUTTON).click()
        try:
            wait_and_get_element(self, self._WATCHLATER_BUTTON).click()  # HI OK devs
        except StaleElementReferenceException:
            pass

    def open(self, relative_url='', page=None):
        # type: (str, Page) -> None
        if page:
            url = urljoin(urljoin(page.BASE_URL, page.PATH), relative_url)
        else:
            url = urljoin(BASE_URL, relative_url)

        self.driver.get(url)

    @property
    def TAB_NAME_TEXT(self):
        return self._TAB_NAME_TEXT
