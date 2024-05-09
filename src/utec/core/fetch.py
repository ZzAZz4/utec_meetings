from utec.core.conference import Conference
from utec.core.driver import get_wired_webdriver, FindWithWait


from datetime import datetime, timedelta
from typing import Any, TYPE_CHECKING
import os
import json

from utec.core.driver import WiredDriver as WiredWebdriver
if TYPE_CHECKING:
    from seleniumwire.request import Request


def get_conferences():
    today = datetime.today()
    end = today + timedelta(days=200)
    start_t = today.strftime("%Y-%m-%d")
    end_t = end.strftime("%Y-%m-%d")
    print(start_t, end_t)

    content = get_conference_json(start_t, end_t)

    conferences: list[Conference] = []
    for conference in content:
        course = conference['conference']["topic"]
        start_date_str = conference["startTime"]
        start_hour_str = conference['conference']["startHour"]
        url = conference.get("joinUrl", None)

        start = datetime.strptime(
            f"{start_date_str} {start_hour_str}", "%Y-%m-%d %H:%M")
        conferences.append(Conference(course, start, url))

    return conferences


def get_conference_json(start: str, end: str):
    driver_type = os.getenv('DRIVER_TYPE', 'chrome')
    with get_wired_webdriver(driver_type) as driver:
        prompt_gmail_login(driver)
        content = intercept_request_content(driver, start, end)

    return content


def prompt_gmail_login(driver: 'WiredWebdriver'):
    LOGIN_BTN_XPATH = (
        '/html/body/div/div/div[2]/button'
    )
    CONFERENCE_BTN_XPATH = (
        '//*[@id="app"]/div[1]/div/div/div[1]/div/div[3]/button'
    )

    driver.get('https://sistema-academico.utec.edu.pe/access')

    finder = FindWithWait(driver)
    login_button = finder.find_element("xpath", LOGIN_BTN_XPATH)
    login_button.click()

    conf_btn = finder.find_element("xpath", CONFERENCE_BTN_XPATH, timeout=360)
    conf_btn.click()

    driver.minimize_window()
    driver.switch_to.window(driver.window_handles[1])
    login_button = finder.find_element("xpath", LOGIN_BTN_XPATH)
    login_button.click()


def intercept_request_content(
    driver: 'WiredWebdriver',
    start: str,
    end: str
) -> list[dict[str, Any]]:
    API_URL = (
        'https://api.utec.edu.pe/conference-api'
        '/v1/conference/list/meeting/student'
    )

    def on_intercept_request(request: 'Request'):
        if request.url == API_URL:
            body = json.loads(request.body.decode('utf-8'))
            body['fechaInicio'] = start
            body['fechaFin'] = end

            modified_body = json.dumps(body, separators=(',', ':'))
            request.body = modified_body.encode('utf-8')

    driver.request_interceptor = on_intercept_request

    driver.get("https://conference.utec.edu.pe/consulta-alumno")

    request = driver.wait_for_request(API_URL, timeout=200)
    assert request.response

    response_body = json.loads(request.response.body.decode('utf-8'))
    content = response_body['content']
    return content
