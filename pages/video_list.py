# coding=utf-8
import os

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page import Page
from component import Component
from urlparse import urljoin
import constants
import router
from utils import awaited_property, wait_and_get_element, same_urls


class VideoListPage(Page):
    PATH = 'video/'

    MY_VIDEO_PATH = 'myVideo/'
    WATCH_LATER_PATH = 'watchLater/'
    SEARCH_PATH = 'search/'

    _FILE_UPLOAD_BUTTON = '//*[@id="hook_Block_VideoVitrinaUploadButton"]/div/a[1]'
    _CONFIRM_ACTION_BUTTON = '//*[@id="vv-confirm-form"]/div[2]/input'
    _VIDEO_TAB_TITLE = '//div[@class="mml_ucard_n_g"]'
    _HOOK_BLOCK = '//*[@id="hook_Block_VideoVitrinaContent"]'
    _VIDEO_SEARCH_FIELD = '//input[@class="search-input_it it"]'
    _VIDEO_SEARCH_DIV = '//*[@data-fetch-type="search"]'
    _VIDEO_LIST = '//*[@id="vv_main_content"]/div/div/div[1]'
    _VIDEO_UPLOAD_PROGRESS = '//div[@class="progress __dark"]'
    _VIDEO_ADD_BUTTON = '//*[@id="hook_Block_VideoVitrinaUploadButton"]/div/a[1]'
    _VIDEO_SCROLL_LIST = '//*[@id="layer_main_cnt_scroll"]'
    _VIDEOS = '//*[@id="vv_main_content"]/div/div/div[1]/div[contains(concat(" ", normalize-space(@class), " "), " vid-card ")]'
    _VIDEO_BY_NUM = '//*[@id="vv_main_content"]/div/div/div[1]/div[contains(concat(" ", normalize-space(@class), " "), " vid-card ")][{num}]'

    _VIDEO_LIST_MYVIDEO = '//*[@id="vv_main_content"]/div/div'
    _VIDEOS_MYVIDEO = '//*[@id="vv_main_content"]/div/div/div[contains(concat(" ", normalize-space(@class), " "), " vid-card ")]'
    _VIDEO_BY_NUM_MYVIDEO = '//*[@id="vv_main_content"]/div/div/div[contains(concat(" ", normalize-space(@class), " "), " vid-card ")][{num}]'
    _VIDEO_BY_NUM_SEARCH = '//*[@data-fetch-type="search"]/*[@class="js-loader-container clearfix"]/div[contains(concat(" ", normalize-space(@class), " "), " vid-card ")][{num}]'

    def wait_load(self):
        wait_and_get_element(self, self._VIDEO_UPLOAD_PROGRESS)

    def wait_noload(self):
        WebDriverWait(self.driver, constants.LONG_WAIT_TIME).until(
            expected_conditions.invisibility_of_element_located((By.XPATH, self._VIDEO_UPLOAD_PROGRESS))
        )

    def open_video_upload_dialog(self):
        wait_and_get_element(self, self._VIDEO_ADD_BUTTON).click()
        return self.VideoUploadDialog(self.driver)

    def confirm_action(self):
        wait_and_get_element(self, self._CONFIRM_ACTION_BUTTON).click()

    def wait_open_search(self):
        wait_and_get_element(self, self._VIDEO_SEARCH_DIV)

    def wait_for_load(self):
        self.wait_and_get_hook_block

    def delete_video(self, video):
        hover = ActionChains(self.driver).move_to_element(video)
        hover.perform()

        delete_button = video.find_element_by_class_name('vl_ic_delete')
        delete_button.click()

        VideoListPage(self.driver).confirm_action()

    @property
    def video_list(self):
        if router.Router().is_on_myvideos_page:
            return wait_and_get_element(self, self._VIDEO_LIST_MYVIDEO)

        return wait_and_get_element(self, self._VIDEO_LIST)

    @awaited_property
    def video_scroll_list(self):
        pass

    @awaited_property('_HOOK_BLOCK')
    def wait_and_get_hook_block(self):
        pass

    def wait_and_get_video_by_num(self, num):
        if router.Router().is_on_myvideos_page:
            return wait_and_get_element(self,
                                        self._VIDEO_BY_NUM_MYVIDEO.format(num=num + 1))  # нумерация в xpath с единицы

        if router.Router().is_on_search_page:
            return wait_and_get_element(self, self._VIDEO_BY_NUM_SEARCH.format(num=num + 1))

        return wait_and_get_element(self, self._VIDEO_BY_NUM.format(num=num + 1))  # нумерация в xpath с единицы

    def scroll_videos_to(self, y):
        self.driver.execute_script('document.evaluate(`{xpath}`, document).iterateNext().scrollTo(0, {to})'
                                   .format(xpath=self._VIDEO_SCROLL_LIST, to=y))

    @property
    def videos(self):
        self.video_list
        if router.Router().is_on_myvideos_page:
            return self.driver.find_elements_by_xpath(self._VIDEOS_MYVIDEO)

        return self.driver.find_elements_by_xpath(self._VIDEOS)

    def search(self, text):
        wait_and_get_element(self, self._VIDEO_SEARCH_FIELD).send_keys(text)

    @property
    def video_count(self):
        return len(self.videos)

    @property
    def video_ids(self):
        return map(lambda node: int(node.get_attribute('data-id')), self.videos)

    class VideoUploadDialog(Component):
        _EXTERNAL_UPLOAD_BUTTON = '//*[@id="vvc-filter"]/span[2]'
        _EXTERNAL_LINK_INPUT_FIELD = '//*[@id="hook_Form_VVAddMovieToAlbum"]/form/div[1]/div/div/input'
        _EXTERNAL_UPLOAD_APPROVE_BUTTON = '//*[@id="hook_Form_VVAddMovieToAlbum"]/form/div[3]/button'
        _VIDEO_UPLOAD = '//*[@id="hook_Block_VideoVitrinaPopupUploader"]/div[4]/div[1]/span'

        def open_external_upload_dialog(self):
            wait_and_get_element(self, self._EXTERNAL_UPLOAD_BUTTON).click()

        def add_external_video(self, link):
            wait_and_get_element(self, self._EXTERNAL_LINK_INPUT_FIELD).send_keys(link)
            wait_and_get_element(self, self._EXTERNAL_UPLOAD_APPROVE_BUTTON).click()

        @awaited_property('_VIDEO_UPLOAD')
        def video_upload(self):
            pass

        def upload_file(self):
            root_element = wait_and_get_element(self, self._VIDEO_UPLOAD)

            element = root_element.find_element_by_tag_name('input')
            element.send_keys(os.getcwd() + '/content/video.mp4')

            # В случае, если браузер не сообщил, мы насильно сообщаем поле ввода, что оно изменилось
            try:
                self.driver.execute_script(
                    'document.evaluate(`{xpath}`, document).iterateNext().dispatchEvent(new Event("change"))'.format(
                        xpath=self._VIDEO_UPLOAD))
            except WebDriverException:
                pass
