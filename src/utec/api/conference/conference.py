from datetime import datetime, timedelta

from src.utec.core.driver import make_wired_webdriver
from src.utec.api.conference.intercept import intercept_request_content
from src.utec.api.conference.login import login
from src.utec.core.progress import ProgressIndicator, EmptyProgressIndicator

from pyvirtualdisplay.display import Display
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service


from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass
class Conference:
    course: str
    start: datetime
    url: str | None


def get_conference_json(username: str, password: str, start: str, end: str, progress: ProgressIndicator):
    display = Display(visible=False, size=(800, 600))
    display.start()

    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--disable-gpu")
    with make_wired_webdriver(cls=webdriver.Chrome, service=service, options=options) as driver:
        progress.reset(100)
        progress.set_description("Starting driver...")
        login(driver, username, password, progress)
        content = intercept_request_content(driver, start, end, progress)

    display.stop()
    return content


def parse_conference_json(content: list[dict[str, Any]]) -> list[Conference]:
    conferences: list[Conference] = []
    for conference in content:
        course = conference['conference']["topic"]
        start_date_str = conference["startTime"]
        start_hour_str = conference['conference']["startHour"]
        url = conference.get("joinUrl", None)

        start = datetime.strptime(f"{start_date_str} {start_hour_str}", "%Y-%m-%d %H:%M")
        conferences.append(Conference(course, start, url))

    return conferences


def get_conferences(username: str, password: str, progress: ProgressIndicator | None = None):
    progress = progress if progress is not None else EmptyProgressIndicator()

    today = datetime.today()
    end = today + timedelta(days=200)
    start_t = today.strftime("%Y-%m-%d")
    end_t = end.strftime("%Y-%m-%d")
    print(start_t, end_t)

    content = get_conference_json(username, password, start_t, end_t, progress)
    conferences = parse_conference_json(content)
    return conferences
