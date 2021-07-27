from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from demo_event.demo_event_home_page import DemoEventHomePage


class LoginPage:
    LOGIN_BUTTON = (By.XPATH, "//button[.//span[text()='Login']]")
    EMAIL_FIELD = (By.ID, "lookup-email-input-id")
    PASSWORD_FIELD = (By.ID, "login-with-email-and-password-password-id")
    SEND_LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)
        self.demo_event_home_page = DemoEventHomePage(self.browser)

    def login_button(self):
        """ Button on top right of the app page used to open login window """
        login_button = self.wait.until(expected_conditions.element_to_be_clickable(self.LOGIN_BUTTON))
        return login_button

    def fill_email(self, email):
        """ Fill e-mail field in login window with email

        :param str email: The e-mail to fill into the e-mail field
        """
        login_field = self.wait.until(expected_conditions.element_to_be_clickable(self.EMAIL_FIELD))
        login_field.send_keys(email)

    def send_login_button(self):
        """ Button to send filled login data in login window """
        send_login_button = self.wait.until(expected_conditions.element_to_be_clickable(self.SEND_LOGIN_BUTTON))
        return send_login_button

    def fill_password(self, password):
        """ Fill password field in login window with password

        :param str password: The password to fill into the password field
        """
        password_field = self.wait.until(expected_conditions.element_to_be_clickable(self.PASSWORD_FIELD))
        password_field.send_keys(password)

    def log_in_if_not_logged_in_yet(self, email, password):
        # If already logged in, no need to do it again
        if self.demo_event_home_page.check_if_messages_icon_is_visible():
            return
        else:
            # Going to home page
            self.browser.get('https://app.swapcard.com')
            # Logging in
            self.login_button().click()
            # Filling e-mail
            self.fill_email(email)
            self.send_login_button().click()
            # Filling password
            self.fill_password(password)
            self.send_login_button().click()
            # Waiting for login
            self.demo_event_home_page.wait_for_messages_icon_after_login()
