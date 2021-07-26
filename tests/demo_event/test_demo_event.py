import time

from datetime import datetime, timedelta
from login.login_page import LoginPage
from demo_event.demo_event_home_page import DemoEventHomePage
from demo_event.demo_event_attendees_page import DemoEventAttendeesPage

def test_search_attendees(browser, user_data):
    demo_event_id = 'RXZlbnRfMTg5Njc2'
    demo_event_information_id = 'QWR2ZXJ0aXNlbWVudF8yODYz'

    # Going to app page
    browser.get('https://app.swapcard.com')

    # Page objects
    login_page = LoginPage(browser)
    demo_event_home_page = DemoEventHomePage(browser)
    demo_event_attendees_page = DemoEventAttendeesPage(browser)

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
    now = datetime.now()
    request_time_delta = timedelta(minutes=2)

    errors = []
    # Checking URL for request
    event_show = api_requests['event_show']['request']
    event_information = api_requests['event_information_show']['request']
    for key in api_requests:
        request_url = api_requests[key]['request']['url']
        if not request_url == 'https://t.swapcard.com/':
            errors.append(f"URL for {key} request was not https://t.swapcard.com/, it was {request_url}")

    # Checking payload for event_show
    event_id = event_show['postData']['event_id']
    if not event_id == demo_event_id:
        errors.append(
            f"Event Id request for event_show in demo event was {event_id} instead of {demo_event_id}")

    event_type = event_show['postData']['type']
    if not event_type == 'event_show':
        errors.append(
            f"Request type for event_show in demo event was {event_type} instead of event_show")

    event_data = datetime.strptime(event_show['postData']['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if not datetime.now() - event_data < request_time_delta:
        errors.append(
            f"Request date for event_show was {event_data}")

    # Checking payload for event_information
    event_id = event_information['postData']['event_id']
    if not event_id == demo_event_id:
        errors.append(
            f"Event Id request for event_interstitial_information_show in demo event was {event_id} instead of {demo_event_id}")

    information_id = event_information['postData']['information_id']
    if not information_id == demo_event_information_id:
        errors.append(
            f"Demo event information Id for event_interstitial_information_show in demo event was {information_id} instead of {demo_event_information_id}")

    event_type = event_information['postData']['type']
    if not event_type == 'event_interstitial_information_show':
        errors.append(
            f"Request type for event_interstitial_information_show in demo event was {event_type} instead of event_interstitial_information_show")

    event_data = datetime.strptime(event_information['postData']['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if not datetime.now() - event_data < request_time_delta:
        errors.append(
            f"Request date for event_show was {event_data}")

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))
    assert browser.current_url == "https://app.swapcard.com/event/your-demo-event-demo-swapcard-62"

    # Going to the attendees page
    demo_event_attendees_page.atendees_tab_selector().click()

    time.sleep(15)
    assert True
