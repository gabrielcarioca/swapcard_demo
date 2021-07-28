import json
import copy

from datetime import datetime, timedelta
from demo_event.demo_event_home_page import DemoEventHomePage
from demo_event.demo_event_attendees_page import DemoEventAttendeesPage
from selenium.webdriver.support.ui import WebDriverWait


class DemoEventTests:
    demo_event_id = 'RXZlbnRfMTg5Njc2'
    demo_event_information_id = 'QWR2ZXJ0aXNlbWVudF8yODYz'
    demo_event_view_id = 'RXZlbnRWaWV3Xzc0MjU3'

    class SearchAPIRequestsInBrowser:
        """ Class with a __call__ method used to validate if expected API requests are found in browser

            Attributes:
                driver  The driver or browser to check the performance log for the expected API requests
        """
        def __init__(self, *api_requests):
            self.api_requests = api_requests

        def __call__(self, browser):
            found_request = {}
            swapcard_requests = [request for request in browser.requests if request.url == 'https://t.swapcard.com/']
            for request in swapcard_requests:
                for payload in request.body.decode().split("\n"):
                    payload_json = json.loads(payload.encode())
                    if payload_json['type'] in self.api_requests:
                        found_request[payload_json['type']] = copy.deepcopy(request)
                        found_request[payload_json['type']].body = payload

                if set(found_request.keys()) == set(self.api_requests):
                    return found_request
            return False

    def test_demo_event_page(self, log_in):
        browser = log_in

        # Page objects
        demo_event_home_page = DemoEventHomePage(browser)

        # Going to demo event page
        demo_event_home_page.demo_event_card().click()

        # Validating API requests
        api_requests = WebDriverWait(browser, 20).until(
            self.SearchAPIRequestsInBrowser('event_show', 'event_information_show')
        )
        event_show_request = api_requests['event_show']
        event_information_show_request = api_requests['event_information_show']
        del browser.requests
        request_time_delta = timedelta(minutes=2)

        errors = []
        event_show_body = json.loads(event_show_request.body)
        event_information_show_body = json.loads(event_information_show_request.body)

        # Checking event_show payload
        event_id = event_show_body['event_id']
        if not event_id == self.demo_event_id:
            errors.append(
                f"Event Id payload for event_show in demo event was {event_id} instead of {self.demo_event_id}")

        request_type = event_show_body['type']
        if not request_type == 'event_show':
            errors.append(
                f"Request type for event_show in demo event was {request_type} instead of event_show")

        request_date = datetime.strptime(event_show_body['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if not datetime.now() - request_date < request_time_delta:
            errors.append(
                f"Request date for event_show was {request_date}")

        # Checking event_information_show payload
        event_id = event_information_show_body['event_id']
        if not event_id == self.demo_event_id:
            errors.append(
                f"Event Id payload for event_information_show in demo event was {event_id} instead of {self.demo_event_id}")

        information_id = event_information_show_body['information_id']
        if not information_id == self.demo_event_information_id:
            errors.append(
                f"Demo event information Id for event_information_show in demo event was {information_id} instead of {self.demo_event_information_id}")

        request_type = event_information_show_body['type']
        if not request_type == 'event_information_show':
            errors.append(
                f"Request type for event_information_show in demo event was {request_type} instead of event_information_show")

        request_date = datetime.strptime(event_information_show_body['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if not datetime.now() - request_date < request_time_delta:
            errors.append(
                f"Request date for event_show was {request_date}")

        # Asserting if all API requests were send as expected with correct payload and URL
        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
        assert browser.current_url == "https://app.swapcard.com/event/your-demo-event-demo-swapcard-62"

    def test_attendees_search_in_demo_event(self, log_in):
        browser = log_in
        # Going to Swapcard demo event page
        demo_event_url = "https://app.swapcard.com/event/your-demo-event-demo-swapcard-62"
        if browser.current_url != demo_event_url:
            browser.get(demo_event_url)

        # Page objects
        demo_event_attendees_page = DemoEventAttendeesPage(browser)

        # Going to the attendees page
        demo_event_attendees_page.attendees_tab_selector().click()

        # Filling search field
        del browser.requests
        query = 'LLC'
        demo_event_attendees_page.fill_attendees_search_field(query)

        # Validating API requests
        api_requests = WebDriverWait(browser, 20).until(
            self.SearchAPIRequestsInBrowser('people_view_search')
        )
        people_search_request = api_requests['people_view_search']
        request_time_delta = timedelta(minutes=2)

        errors = []
        people_search_body = json.loads(people_search_request.body.decode())

        # Checking people_view_search payload
        event_id = people_search_body['event_id']
        if not event_id == self.demo_event_id:
            errors.append(
                f"Event Id payload for people_view_search in demo event attendees search was {event_id} instead of {self.demo_event_id}")

        event_view_id = people_search_body['event_view_id']
        if not event_view_id == self.demo_event_view_id:
            errors.append(
                f"Event view Id payload for people_view_search in demo event attendees search was {event_view_id} instead of {self.demo_event_information_id}")

        search_query = people_search_body['query']
        if not search_query == query:
            errors.append(
                f"Query for attendees search in demo event was expected to be {query} but was instead {search_query}")

        search_requests_type = people_search_body['type']
        if not search_requests_type == 'people_view_search':
            errors.append(
                f"Request type for people_view_search in attendees search for demo event was {search_requests_type} instead of people_view_search")

        search_date = datetime.strptime(people_search_body['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if not datetime.now() - search_date < request_time_delta:
            errors.append(
                f" Request date for people_view_search was {search_date}")

        # Asserting if all API requests were send as expected with correct payload and URL
        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
        assert browser.current_url == f"https://app.swapcard.com/event/your-demo-event-demo-swapcard-62/people/RXZlbnRWaWV3Xzc0MjU3?search={query}"

        # Asserting users shown in the page
        search_result_count = demo_event_attendees_page.get_number_of_search_results()
        attendees_data = demo_event_attendees_page.get_attendees_data()
        assert len(attendees_data) == search_result_count

        people_with_search_query = [attendee for attendee in attendees_data if query in attendee['name'] or query in attendee['title'] or query in attendee['company']]
        assert len(people_with_search_query) == search_result_count
