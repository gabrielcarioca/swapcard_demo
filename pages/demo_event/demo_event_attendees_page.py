from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import re


class DemoEventAttendeesPage:
    ATTENDEES_TAB_SELECTOR = (By.XPATH, "(//a[@href='/event/your-demo-event-demo-swapcard-62/people/RXZlbnRWaWV3Xzc0MjU3'])[1]")
    ATTENDEES_SEARCH_FIELD = (By.XPATH, "//input[@placeholder='Search']")
    REFINE_THE_LIST_SEARCH_MESSAGE = (By.XPATH, "//div[./p[text()='Refine the list (min. 2 characters)']]")
    NUMBER_OF_ATTENDEES_IN_SEARCH_RESULT = (By.XPATH, "//div[./p[contains(text(), 'result')]]")
    ATTENDEES_DIV_XPATH = "//div[@class='infinite-scroll-component ']//a/div/div[not(.//img)]"

    TIMEOUT = 15

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, self.TIMEOUT)

    def attendees_tab_selector(self):
        """ Attendees link in the tab selector on top of the event page """
        attendees_tab_selector = self.wait.until(expected_conditions.element_to_be_clickable(self.ATTENDEES_TAB_SELECTOR))
        return attendees_tab_selector

    def fill_attendees_search_field(self, search_value):
        """ Fill search field with search_value to refine the list of event attendees

        :param str search_value: The value to insert into the attendees search field to refine the list in the event page
        """
        attendees_search_field = self.wait.until(expected_conditions.element_to_be_clickable(self.ATTENDEES_SEARCH_FIELD))
        attendees_search_field.send_keys(search_value)

        # Waiting for search to be applied in page
        self.wait.until(expected_conditions.invisibility_of_element_located(self.REFINE_THE_LIST_SEARCH_MESSAGE))
        search_result = self.wait.until(expected_conditions.visibility_of_element_located(self.NUMBER_OF_ATTENDEES_IN_SEARCH_RESULT))
        assert bool(re.match(r"\d+\sresults", search_result.text))

    def get_number_of_search_results(self):
        search_result = self.wait.until(
            expected_conditions.visibility_of_element_located(self.NUMBER_OF_ATTENDEES_IN_SEARCH_RESULT))
        search_result_text = search_result.text
        return int(re.search(r"(\d+)\sresults", search_result_text).group(1))

    def get_attendees_data(self):
        attendees = []

        attendees_div = self.browser.find_elements(By.XPATH, self.ATTENDEES_DIV_XPATH)
        for attendee in attendees_div:
            attendee_dict = {}
            attendee_dict['name'] = attendee.find_element(By.XPATH, "(.//span)[1]").text
            attendee_dict['title'] = attendee.find_element(By.XPATH, "(.//span)[2]").text
            attendee_dict['company'] = attendee.find_element(By.XPATH, "(.//span)[3]").text

            attendees.append(attendee_dict)

        return attendees
