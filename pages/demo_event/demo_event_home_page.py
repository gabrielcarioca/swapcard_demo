from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

class DemoEventHomePage:
    DEMO_EVENT_CARD = (By.XPATH, "//a[@href='/event/your-demo-event-demo-swapcard-62'][.//img]/div")
    TIMEOUT = 20

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, self.TIMEOUT)

    def demo_event_card(self):
        """ Card for Swapcard Demo event under Past events section. """
        demo_event_card = self.wait.until(expected_conditions.element_to_be_clickable(self.DEMO_EVENT_CARD))
        return demo_event_card


