import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pytest import fixture
from seleniumwire import webdriver
from definitions import ROOT_DIR
from login.login_page import LoginPage

import json



# File containing user and password to access swapcard system
USER_DATA_JSON_PATH = os.path.join(ROOT_DIR, 'data', 'user.json')


# Loading system user and password
def load_user_data(path):
    with open(path) as data_file:
        data = json.load(data_file)
        return data


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="append",
        default=[],
        help="list of browsers to run tests against",
    )


# Creates a firefox and chrome browser
def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        metafunc.parametrize("browser", metafunc.config.getoption("browser") if metafunc.config.getoption("browser") else ['Chrome'], indirect=True)


@fixture(scope='module')
def browser(request):
    if request.param == 'Firefox':
        browser = webdriver.Firefox()
    else:
        browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()


@fixture()
def user_data():
    data = load_user_data(USER_DATA_JSON_PATH)
    return data


@fixture()
def log_in(user_data, browser):
    LoginPage(browser).log_in_if_not_logged_in_yet(email=user_data['user'], password=user_data['password'])
    return browser
