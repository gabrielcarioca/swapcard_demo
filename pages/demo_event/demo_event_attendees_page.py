from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class DemoEventAttendeesPage:
    ATENDEES_TAB_SELECTOR = (By.XPATH, "(//a[@href='/event/your-demo-event-demo-swapcard-62/people/RXZlbnRWaWV3Xzc0MjU3'])[1]")

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)

    def atendees_tab_selector(self):
        atendees_tab_selector = self.wait.until(expected_conditions.element_to_be_clickable(self.ATENDEES_TAB_SELECTOR))
        return atendees_tab_selector
