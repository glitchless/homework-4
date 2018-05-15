import os

from pages.page import Page
from utils import wait_and_get_element


class UploadPage(Page):
    _VIDEO_UPLOAD = '//*[@id="hook_Block_VideoVitrinaPopupUploader"]/div[4]/div[1]/span'

    def upload_file(self):
        root_element = wait_and_get_element(self, self._VIDEO_UPLOAD)

        element = root_element.find_element_by_tag_name('input')
        element.send_keys(os.getcwd() + '/content/video.mp4')

        self.driver.execute_script('document.evaluate(`{xpath}`, document).iterateNext().dispatchEvent(new Event("change"))'
                                   .format(xpath=self._VIDEO_UPLOAD))
