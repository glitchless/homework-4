import os
import configparser

SETTINGS_FILEPATH = 'conf/app.conf'
SETTINGS_SECTION = 'SETTINGS'

config = configparser.ConfigParser()
config.read_file(open(SETTINGS_FILEPATH))

COMMAND_EXECUTOR = config.get(SETTINGS_SECTION, 'command_executor')
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_PATH = os.path.join(DIRECTORY, config.get(SETTINGS_SECTION, 'screenshot_dir'))
WAIT_TIME = config.getint(SETTINGS_SECTION, 'wait_time')
LONG_WAIT_TIME = config.getint(SETTINGS_SECTION, 'long_wait_time')
MAKE_SCREENSHOTS = config.getboolean(SETTINGS_SECTION, 'make_screenshots')
BASE_URL = config.get(SETTINGS_SECTION, 'base_url')
SKIP_FINISHED_TESTS = config.getboolean(SETTINGS_SECTION, 'skip_finished_tests')
