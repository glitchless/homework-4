# -*- coding: utf-8 -*-

import unittest
from pages.mainpage import MainPage
import sys
import tests.video

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(tests.video.VideoTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
