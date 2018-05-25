# coding=utf-8
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import router
from .page import Page
from os import environ
from .component import Component
import constants
from utils import awaited_property, wait_and_get_element


class VideoPage(Page):
    PATH = 'video/{id}'

    _HOOK_BLOCK = '//*[@id="hook_Block_VideoVitrinaContent"]'
    _VIDEO_LIST = '//*[@id="vv_main_content"]/div/div/div[1]'
    _VIDEO_SCROLL_LIST = '//*[@id="layer_main_cnt_scroll"]'
    _VIDEO_BY_NUM = '//*[@id="vv_main_content"]/div/div/div[1]/div[{num}]'
    _VIDEO_UPLOAD_BUTTON = '//div[@class="vl_add-video"]'
    _VIDEO_WATCH_LATER_BUTTON = '//*[@al-click="watchLater()"]'
    _VIDEO_COMMENTS = '//div[@class="comments_lst_cnt"]/div'
    _VIDEO_COMMENT_TEXT = './/div[@class="comments_text textWrap"]/div'
    _STREAM_COMMENT_TEXT = './/div[@class="vp-chat_i_tx textWrap"]'
    _VIDEO_COMMENT_FIELD = '//div[@data-l="t,ta"]'
    _STREAM_COMMENT_FIELD = '//div[@class="it vp-chat_it"]'
    _STREAM_COMMENTS = '//div[@class="vp-chat_cnt"]/div'
    _STREAM_COMMENT_BUTTON = '//button[@class="button-pro vp-chat_send"]'
    _VIDEO_COMMENT_BUTTON = '//button[@data-l="t,submit"]'
    _REMOVE_COMMENT_BUTTON = '//a[@class="fade-on-hover comments_remove ic10 ic10_close-g"]'
    _VIDEO_PLAYER = '//div[@class="html5-vpl_vid"]/video'
    _VIDEO_PAGE_GET_LINK_BUTTON = '//div[@al-click="openDialog(\'share\')"]'
    _VIDEO_PAGE_GET_LINK_INPUT = '//div[@al-controller="ShareDialogController"]//input'
    _VIDEO_PAGE_COMMENTS_BUTTON = '//ul[@class="widget-list"]/li[1]/div/a'
    _VIDEO_PAGE_LIKE_BUTTON_CONTAINER = '//ul[@class="widget-list"]/li[3]/div/div'
    _VIDEO_PAGE_LIKE_BUTTON = '//ul[@class="widget-list"]/li[3]/div/div/span'

    def wait_for_load(self):
        self.wait_and_get_hook_block

    def open(self, relative_url=''):
        raise NotImplemented('Can`t open a video without an id')

    def send_comment(self, text):
        if router.Router().is_stream:
            wait_and_get_element(self, self._STREAM_COMMENT_FIELD).send_keys(text)
            wait_and_get_element(self, self._STREAM_COMMENT_BUTTON).click()
            return

        try:
            wait_and_get_element(self, self._VIDEO_COMMENT_FIELD).send_keys(text)
            wait_and_get_element(self, self._VIDEO_COMMENT_BUTTON).click()
        except TimeoutException:
            # Фикс
            wait_and_get_element(self, self._STREAM_COMMENT_FIELD).send_keys(text)
            wait_and_get_element(self, self._STREAM_COMMENT_BUTTON).click()

    def remove_comment(self, comment):
        remove_button = comment.find_element_by_class_name('comments_remove')
        self.driver.execute_script(
            "arguments[0].style.visibility = 'visible'; arguments[0].classList.remove('fade-on-hover');", remove_button)
        remove_button.click()

    def find_comment_with_text(self, text):
        xpath_comment = self._VIDEO_COMMENTS
        if router.Router().is_stream:
            xpath_comment = self._STREAM_COMMENTS

        xpath_comment_text = self._VIDEO_COMMENT_TEXT
        if router.Router().is_stream:
            xpath_comment_text = self._STREAM_COMMENT_TEXT

        for element in self.driver.find_elements_by_xpath(xpath_comment):
            comment = element.find_element_by_xpath(xpath_comment_text)
            if comment.text == text:
                return element
        return self.find_comment_with_text(text)

    def open_by_id(self, video_id):
        # type: (int) -> None
        super(VideoPage, self).open(str(video_id))

    def toggle_watch_later(self):
        video = self.watch_video()
        hover = ActionChains(self.driver).move_to_element(video)
        hover.perform()
        wait_and_get_element(self, self._VIDEO_WATCH_LATER_BUTTON).click()

    def get_video_player(self):
        return wait_and_get_element(self, self._VIDEO_PLAYER)

    def get_video_link(self):
        video_player = wait_and_get_element(self, self._VIDEO_PLAYER)
        hover = ActionChains(self.driver).move_to_element(video_player)
        hover.perform()

        wait_and_get_element(self, self._VIDEO_PAGE_GET_LINK_BUTTON).click()
        return wait_and_get_element(self, self._VIDEO_PAGE_GET_LINK_INPUT).get_attribute('value')

    def get_video_id(self):
        return wait_and_get_element(self, self._VIDEO_PAGE_COMMENTS_BUTTON).get_attribute('data-id')

    def get_like_button_container(self):
        return wait_and_get_element(self, self._VIDEO_PAGE_LIKE_BUTTON_CONTAINER)

    def get_like_button(self):
        return wait_and_get_element(self, self._VIDEO_PAGE_LIKE_BUTTON)

    def watch_video(self):
        return wait_and_get_element(self, self._VIDEO_PLAYER, True, True)

    @awaited_property('_HOOK_BLOCK')
    def wait_and_get_hook_block(self):  # то же, что и выше
        pass

    def wait_and_get_video_by_num(self, num):
        return wait_and_get_element(self, self._VIDEO_BY_NUM.format(num=num))

    def open_upload_video(self):
        wait_and_get_element(self, self._VIDEO_UPLOAD_BUTTON)

    def scroll_videos_to(self, y):
        self.driver.execute_script('document.evaluate(`{xpath}`, document).iterateNext().scrollTo(0, {to})'
                                   .format(xpath=self._VIDEO_SCROLL_LIST, to=y))
