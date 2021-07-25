from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from Utils.api_request_not_sent import APIRequestNotSent

class DemoEventHomePage:
    DEMO_EVENT_CARD = (By.XPATH, "//a[@href='/event/your-demo-event-demo-swapcard-62'][.//img]")

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 15)

    def demo_event_card(self):
        demo_event_card = self.wait.until(expected_conditions.element_to_be_clickable(self.DEMO_EVENT_CARD))
        return demo_event_card

    def wait_until_api_requests_are_sent(self):

        # Waiting for the requests to be sent
        sent_requests = self.wait.until(
            WaitDemoEventAPIRequests()
        )

        # Seeing if the requests weren't found
        if sent_requests['event_show'] == '':
            raise APIRequestNotSent('event_show API request not sent in demo event page')
        elif sent_requests['event_information_show'] == '':
            raise APIRequestNotSent('event_interstitial_information_show API request not sent in demo event page')

class WaitDemoEventAPIRequests:
    def __init__(self):
        self.sent_requests = {'event_show': '', 'event_information_show': ''}

    def __call__(self, driver):
        for log in driver.get_log('performance'):
            log_message = log['message']
            if 'event_show' in log_message:
                self.sent_requests['event_show'] = log_message
            elif 'event_interstitial_information_show' in log_message:
                self.sent_requests['event_information_show'] = log_message

            if self.sent_requests['event_show'] != '' and self.sent_requests['event_information_show'] != '':
                return self.sent_requests

        if self.sent_requests['event_information_show'] == '' or self.sent_requests['event_show'] == '':
            return False
