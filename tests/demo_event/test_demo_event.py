import time

from pages.login_page import LoginPage


def test_search_attendees(browser, user_data):
    # Going to app page
    browser.get('https://app.swapcard.com')

    # Logging in
    login_page = LoginPage(browser)
    login_page.login_button().click()
    # Filling e-mail
    login_page.fill_email(user_data['user'])
    login_page.send_login_button().click()
    # Filling password
    login_page.fill_password(user_data['password'])
    login_page.send_login_button().click()

    time.sleep(5)
    assert True
