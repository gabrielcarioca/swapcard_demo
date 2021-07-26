from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import json

from Utils.api_request_not_sent import APIRequestNotSent

class DemoEventHomePage:
    DEMO_EVENT_CARD = (By.XPATH, "//a[@href='/event/your-demo-event-demo-swapcard-62'][.//img]")
    TIMEOUT = 15

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, self.TIMEOUT)

    def demo_event_card(self):
        """ Card for Swapcard Demo event under Past events section """
        demo_event_card = self.wait.until(expected_conditions.element_to_be_clickable(self.DEMO_EVENT_CARD))
        return demo_event_card

    def wait_until_api_requests_are_sent(self):
        """ Check if event_show and event_interstitial_information API requests are found in browser performance log or if they are sent and found in the next 15 seconds """
        # Waiting for the requests to be sent
        requests_sent = self.wait.until(
            WaitDemoEventAPIRequests()
        )

        # Seeing if the requests weren't found
        if requests_sent['event_show'] == '':
            raise APIRequestNotSent(f'event_show API request was not sent in demo event page for {self.TIMEOUT} seconds after accessing the page')
        elif requests_sent['event_information_show'] == '':
            raise APIRequestNotSent(f'event_interstitial_information_show API request was not sent in demo event page for {self.TIMEOUT} seconds after accessing the page')

        return requests_sent

class WaitDemoEventAPIRequests:
    """ Class with a __call__ method used to validate if event_show and event_interstitial_information_show are found in the performance log for driver

        Attributes:
            driver  The driver or browser to check the performance log for the expected API requests
    """

    def __init__(self):
        self.requests_sent = {'event_show': '', 'event_information_show': ''}

    def __call__(self, driver):
        for log in driver.get_log('performance'):
            log_message = log['message']
            if 'event_show' in log_message:
                self.requests_sent['event_show'] = json.loads(log_message)['message']['params']
                self.requests_sent['event_show']['request']['postData'] = json.loads(
                    self.requests_sent['event_show']['request']['postData'])
            elif 'event_interstitial_information_show' in log_message:
                self.requests_sent['event_information_show'] = json.loads(log_message)['message']['params']
                self.requests_sent['event_information_show']['request']['postData'] = json.loads(
                    self.requests_sent['event_information_show']['request']['postData'])

            # Returning the requests if they are found
            if self.requests_sent['event_show'] != '' and self.requests_sent['event_information_show'] != '':
                return self.requests_sent

        # Otherwise returning false if one of the expected requests was not found in the demo event page
        if self.requests_sent['event_information_show'] == '' or self.requests_sent['event_show'] == '':
            return False
