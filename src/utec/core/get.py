from utec.core.conference import Conference
from datetime import datetime, timedelta

from utec.core.driver import WrappedWiredWebdriver
from utec.core.intercept import intercept_request_content
from utec.core.login import login
from utec.core.progress import ProgressIndicator, EmptyProgressIndicator

from pyvirtualdisplay.display import Display
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service


def get_conference_json(username: str, password: str, start: str, end: str, progress: ProgressIndicator):
    display = Display(visible=False, size=(800, 600))
    display.start()

    path = ChromeDriverManager().install()
    service = Service(path)
    options = Options()
    options.add_argument("--disable-gpu")
    sdriver = webdriver.Chrome(service=service, options=options)

    progress.reset(100)
    progress.set_description("Starting driver...")
    with WrappedWiredWebdriver(sdriver) as driver:
        login(driver, username, password, progress)
        content = intercept_request_content(driver, start, end, progress)

    display.stop()
    return content


def get_conferences(username: str, password: str, progress: ProgressIndicator | None = None):
    progress = progress if progress is not None else EmptyProgressIndicator()

    today = datetime.today()
    end = today + timedelta(days=200)
    start_t = today.strftime("%Y-%m-%d")
    end_t = end.strftime("%Y-%m-%d")
    print(start_t, end_t)

    content = get_conference_json(username, password, start_t, end_t, progress)

    conferences: list[Conference] = []
    for conference in content:
        course = conference['conference']["topic"]
        start_date_str = conference["startTime"]
        start_hour_str = conference['conference']["startHour"]
        url = conference.get("joinUrl", None)

        start = datetime.strptime(f"{start_date_str} {start_hour_str}", "%Y-%m-%d %H:%M")
        conferences.append(Conference(course, start, url))

    return conferences
