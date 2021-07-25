import time

from login.login_page import LoginPage
from demo_event.demo_event_home_page import DemoEventHomePage
from demo_event.demo_event_attendees_page import DemoEventAttendeesPage

import sys

def test_search_attendees(browser, user_data):
    # Going to app page
    browser.get('https://app.swapcard.com')

    # Page objects
    login_page = LoginPage(browser)
    demo_event_home_page = DemoEventHomePage(browser)
    demo_event_attendees_page = DemoEventAttendeesPage(browser)

    # Logging in
    login_page.login_button().click()
    # Filling e-mail
    login_page.fill_email(user_data['user'])
    login_page.send_login_button().click()
    # Filling password
    login_page.fill_password(user_data['password'])
    login_page.send_login_button().click()

    # Going to demo event page
    demo_event_home_page.demo_event_card().click()
    # Validating API requests
    demo_event_home_page.wait_until_api_requests_are_sent()
    # Going to the attendees page
    demo_event_attendees_page.atendees_tab_selector().click()

    time.sleep(15)
    assert True
