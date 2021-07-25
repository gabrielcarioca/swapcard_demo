from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    LOGIN_BUTTON = (By.XPATH, "//button[.//span[text()='Login']]")
    EMAIL_FIELD = (By.ID, "lookup-email-input-id")
    PASSWORD_FIELD = (By.ID, "login-with-email-and-password-password-id")
    SEND_LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)

    def login_button(self):
        login_button = self.wait.until(expected_conditions.element_to_be_clickable(self.LOGIN_BUTTON))
        return login_button

    def fill_email(self, email):
        login_field = self.wait.until(expected_conditions.element_to_be_clickable(self.EMAIL_FIELD))
        login_field.send_keys(email)

    def send_login_button(self):
        send_login_button = self.wait.until(expected_conditions.element_to_be_clickable(self.SEND_LOGIN_BUTTON))
        return send_login_button

    def fill_password(self, password):
        password_field = self.wait.until(expected_conditions.element_to_be_clickable(self.PASSWORD_FIELD))
        password_field.send_keys(password)
