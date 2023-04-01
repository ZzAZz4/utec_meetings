from utec.core.conference import Conference
from datetime import datetime, timedelta

from utec.core.run import get_conference_json

def get_conferences(username: str, password: str):
    today = datetime.today()
    next_year = today + timedelta(days=365)
    start = today.strftime("%Y-%m-%d")
    end = next_year.strftime("%Y-%m-%d")

    content = get_conference_json(username, password, start, end)

    conferences: list[Conference] = []
    for conference in content:
        course = conference['conference']["topic"]
        start_date_str = conference["startTime"]
        start_hour_str = conference['conference']["startHour"]
        url = conference.get("joinUrl", None)

        start = datetime.strptime(f"{start_date_str} {start_hour_str}", "%Y-%m-%d %H:%M")
        conferences.append(Conference(course, start, url))

    return conferences