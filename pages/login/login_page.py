from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class LoginPage:
    LOGIN_BUTTON = (By.XPATH, "//button[.//span[text()='Login']]")
    EMAIL_FIELD = (By.ID, "lookup-email-input-id")
    PASSWORD_FIELD = (By.ID, "login-with-email-and-password-password-id")
    SEND_LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    MESSAGES_ICON = (By.XPATH, "//a[@href='/messages']//span")

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)

    def login_button(self):
        """ Button on top right of the app page used to open login window. """
        login_button = self.wait.until(expected_conditions.element_to_be_clickable(self.LOGIN_BUTTON))
        return login_button

    def fill_email(self, email):
        """ Fill e-mail field in login window with email.

        :param str email: The e-mail to fill into the e-mail field
        """
        login_field = self.wait.until(expected_conditions.element_to_be_clickable(self.EMAIL_FIELD))
        login_field.send_keys(email)

    def send_login_button(self):
        """ Button to send filled login data in login window. """
        send_login_button = self.wait.until(expected_conditions.element_to_be_clickable(self.SEND_LOGIN_BUTTON))
        return send_login_button

    def fill_password(self, password):
        """ Fill password field in login window with password.

        :param str password: The password to fill into the password field
        """
        password_field = self.wait.until(expected_conditions.element_to_be_clickable(self.PASSWORD_FIELD))
        password_field.send_keys(password)

    def check_if_messages_icon_is_visible(self):
        """ This method is used to check if the messages icon for the logged user is visible.

        It's used to optimize login flow, since when the messages icon is visible, the test can skip login steps, since the user is already logged.
        """
        try:
            WebDriverWait(self.browser, 1).until(expected_conditions.visibility_of_element_located(self.MESSAGES_ICON))
            return True
        except TimeoutException:
            return False

    def wait_for_messages_icon_after_login(self):
        """ After the login, this method waits until the messages icon for the user is displayed.
        When it's displayed, the system can continue testing as it knows the login was perfomed successfully.
        """
        self.wait.until(expected_conditions.visibility_of_element_located(self.MESSAGES_ICON))

    def log_in_if_not_logged_in_yet(self, email, password):
        """ If the user is not logged into the system, it performs the login, otherwise this method just returns.

        :param str email: The e-mail to perform the login in case it's not logged in yet
        :param str password: The password to perform the login in case it's not logged in yet
        """
        # If already logged in, no need to do it again
        if self.check_if_messages_icon_is_visible():
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
            self.wait_for_messages_icon_after_login()
