from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from Utils.api_request_not_sent import APIRequestNotSent

class DemoEventHomePage:
    DEMO_EVENT_CARD = (By.XPATH, "//a[@href='/event/your-demo-event-demo-swapcard-62'][.//img]/div")
    MESSAGES_ICON = (By.XPATH, "//a[@href='/messages']//span")
    TIMEOUT = 20

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, self.TIMEOUT)

    def demo_event_card(self):
        """ Card for Swapcard Demo event under Past events section """
        demo_event_card = self.wait.until(expected_conditions.element_to_be_clickable(self.DEMO_EVENT_CARD))
        return demo_event_card

    def check_if_messages_icon_is_visible(self):
        try:
            WebDriverWait(self.browser, 1).until(expected_conditions.visibility_of_element_located(self.MESSAGES_ICON))
            return True
        except TimeoutException:
            return False

    def wait_for_messages_icon_after_login(self):
        self.wait.until(expected_conditions.visibility_of_element_located(self.MESSAGES_ICON))
