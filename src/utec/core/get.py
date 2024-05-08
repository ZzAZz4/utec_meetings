from utec.core.conference import Conference
from datetime import datetime, timedelta

from utec.core.driver import WrappedWiredWebdriver
from utec.core.intercept import intercept_request_content
from utec.core.login import login

# from pyvirtualdisplay.display import Display
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service


def get_conference_json(start: str, end: str):
    # display = Display(visible=True, size=(800, 600))
    # display.start()

    path = GeckoDriverManager().install()
    service = Service(path)
    options = Options()
    options.add_argument("--disable-gpu")
    sdriver = webdriver.Firefox(service=service, options=options)

    with WrappedWiredWebdriver(sdriver) as driver:
        login(driver)
        content = intercept_request_content(driver, start, end)

    # display.stop()
    return content


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
