# coding=utf-8
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page import Page
from os import environ
from component import Component
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
    _VIDEO_COMMENT_FIELD = '//div[@data-l="t,ta"]'
    _STREAM_COMMENT_FIELD = '//div[@class="it vp-chat_it"]'
    _VIDEO_COMMENT_BUTTON = '//button[@data-l="t,submit"]'
    _REMOVE_COMMENT_BUTTON = '//a[@class="fade-on-hover comments_remove ic10 ic10_close-g"]'
    _VIDEO_PLAYER = '//*[@id="VideoAutoplayPlayerE"]/div/div[2]/video'

    def wait_for_load(self):
        self.wait_and_get_hook_block

    def open(self, relative_url=''):
        raise NotImplemented('Can`t open a video without an id')

    def send_comment(self, text):
        wait_and_get_element(self, self._VIDEO_COMMENT_FIELD).send_keys(text)
        wait_and_get_element(self, self._VIDEO_COMMENT_BUTTON).click()

    def remove_comment(self, comment):
        remove_button = comment.find_element_by_class_name('comments_remove')
        self.driver.execute_script(
            "arguments[0].style.visibility = 'visible'; arguments[0].classList.remove('fade-on-hover');", remove_button)
        remove_button.click()

    def find_comment_with_text(self, text):
        for element in self.driver.find_elements_by_xpath(self._VIDEO_COMMENTS):
            comment = element.find_element_by_xpath(self._VIDEO_COMMENT_TEXT)
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

    def watch_video(self):
        return wait_and_get_element(self, self._VIDEO_PLAYER)

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
