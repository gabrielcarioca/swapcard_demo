import time

from datetime import datetime, timedelta
from login.login_page import LoginPage
from demo_event.demo_event_home_page import DemoEventHomePage
from demo_event.demo_event_attendees_page import DemoEventAttendeesPage


class DemoEventTests:
    demo_event_id = 'RXZlbnRfMTg5Njc2'
    demo_event_information_id = 'QWR2ZXJ0aXNlbWVudF8yODYz'
    demo_event_view_id = 'RXZlbnRWaWV3Xzc0MjU3'

    def test_demo_event_page(self, browser, user_data):



        # Going to Swapcard app page
        browser.get('https://app.swapcard.com')

        # Page objects
        login_page = LoginPage(browser)
        demo_event_home_page = DemoEventHomePage(browser)

        # Logging in
        login_page.login_button().click()
        # Filling e-mail
        login_page.fill_email(user_data['user'])
        login_page.send_login_button().click()
        # Filling password
        login_page.fill_password(user_data['password'])
        login_page.send_login_button().click()

        # Going to demo event page
        demo_event_home_page.demo_event_card().click()
        # Validating API requests
        api_requests = demo_event_home_page.wait_until_api_requests_are_sent()
        request_time_delta = timedelta(minutes=2)

        errors = []
        # Checking requests URL
        event_show = api_requests['event_show']['request']
        event_show_post_data = event_show['postData']
        event_information = api_requests['event_information_show']['request']
        event_information_post_data = event_information['postData']
        for key in api_requests:
            request_url = api_requests[key]['request']['url']
            if not request_url == 'https://t.swapcard.com/':
                errors.append(f"URL for {key} request was not https://t.swapcard.com/, it was {request_url}")

        # Checking event_show payload
        event_id = event_show_post_data['event_id']
        if not event_id == self.demo_event_id:
            errors.append(
                f"Event Id payload for event_show in demo event was {event_id} instead of {self.demo_event_id}")

        request_type = event_show_post_data['type']
        if not request_type == 'event_show':
            errors.append(
                f"Request type for event_show in demo event was {request_type} instead of event_show")

        request_date = datetime.strptime(event_show_post_data['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if not datetime.now() - request_date < request_time_delta:
            errors.append(
                f"Request date for event_show was {request_date}")

        # Checking event_interstitial_information_show payload
        event_id = event_information_post_data['event_id']
        if not event_id == self.demo_event_id:
            errors.append(
                f"Event Id payload for event_interstitial_information_show in demo event was {event_id} instead of {self.demo_event_id}")

        information_id = event_information_post_data['information_id']
        if not information_id == self.demo_event_information_id:
            errors.append(
                f"Demo event information Id for event_interstitial_information_show in demo event was {information_id} instead of {self.demo_event_information_id}")

        request_type = event_information_post_data['type']
        if not request_type == 'event_interstitial_information_show':
            errors.append(
                f"Request type for event_interstitial_information_show in demo event was {request_type} instead of event_interstitial_information_show")

        request_date = datetime.strptime(event_information_post_data['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if not datetime.now() - request_date < request_time_delta:
            errors.append(
                f"Request date for event_show was {request_date}")

        # Asserting if all API requests were send as expected with correct payload and URL
        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
        assert browser.current_url == "https://app.swapcard.com/event/your-demo-event-demo-swapcard-62"

    def test_attendees_search_in_demo_event(self, browser):
        # Page objects
        demo_event_attendees_page = DemoEventAttendeesPage(browser)

        # Going to the attendees page
        demo_event_attendees_page.attendees_tab_selector().click()

        # Filling search field
        query = 'LLC'
        demo_event_attendees_page.fill_attendees_search_field(query)

        # Validating API requests
        api_requests = demo_event_attendees_page.wait_until_api_request_when_filling_search_field()
        request_time_delta = timedelta(minutes=2)

        errors = []
        # Checking request URL
        people_search = api_requests['people_view_search']['request']
        people_search_post_data = people_search['postData']

        if not people_search['url'] == 'https://t.swapcard.com/':
            errors.append(f"URL for people_view_search request was not https://t.swapcard.com/, it was {people_search['url']}")

        # Checking people_view_search payload
        event_id = people_search_post_data['event_id']
        if not event_id == self.demo_event_id:
            errors.append(
                f"Event Id payload for people_view_search in demo event attendees search was {event_id} instead of {self.demo_event_id}")

        event_view_id = people_search_post_data['event_view_id']
        if not event_view_id == self.demo_event_view_id:
            errors.append(
                f"Event view Id payload for people_view_search in demo event attendees search was {event_view_id} instead of {self.demo_event_information_id}")

        search_query = people_search_post_data['query']
        if not search_query == query:
            errors.append(
                f"Query for attendees search in demo event was expected to be {query} but was instead {search_query}")

        search_requests_type = people_search_post_data['type']
        if not search_requests_type == 'people_view_search':
            errors.append(
                f"Request type for people_view_search in attendees search for demo event was {search_requests_type} instead of people_view_search")

        search_date = datetime.strptime(people_search_post_data['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if not datetime.now() - search_date < request_time_delta:
            errors.append(
                f" Request date for people_view_search was {search_date}")

        # Asserting if all API requests were send as expected with correct payload and URL
        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
        assert browser.current_url == f"https://app.swapcard.com/event/your-demo-event-demo-swapcard-62/people/RXZlbnRWaWV3Xzc0MjU3?search={query}"

        time.sleep(5)
        assert True
