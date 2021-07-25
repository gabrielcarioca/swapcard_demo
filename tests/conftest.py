import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pytest import fixture
from selenium import webdriver
from definitions import ROOT_DIR


USER_DATA_JSON_PATH = os.path.join(ROOT_DIR, 'data', 'user.json')


def load_user_data(path):
    with open(path) as data_file:
        data = json.load(data_file)
        return data


@fixture(scope='session')
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


@fixture()
def user_data():
    data = load_user_data(USER_DATA_JSON_PATH)
    return data
