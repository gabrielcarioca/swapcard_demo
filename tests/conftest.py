import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pytest import fixture
from seleniumwire import webdriver
from definitions import ROOT_DIR

# File containing user and password to access swapcard system
USER_DATA_JSON_PATH = os.path.join(ROOT_DIR, 'data', 'user.json')


# Loading system user and password
def load_user_data(path):
    with open(path) as data_file:
        data = json.load(data_file)
        return data


@fixture(scope='session')
def browser():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()


@fixture(scope='session')
def abrowser():
    browser = webdriver.Firefox()
    browser.maximize_window()
    yield browser
    browser.quit()


@fixture()
def user_data():
    data = load_user_data(USER_DATA_JSON_PATH)
    return data
