from dataclasses import dataclass
from datetime import datetime


@dataclass
class Conference:
    course: str
    start: datetime
    end: datetime
    url: str

    @staticmethod
    def from_json(json_data):
        
        conference_data = json_data['conference']
        url = json_data['joinUrl']
        date = json_data['startTime']
        
        course = conference_data['nameCourse']
        start_hour = conference_data['startHour']
        end_hour = conference_data['endHour']

        start_time = datetime.fromisoformat(f"{date} {start_hour}")
        end_time = datetime.fromisoformat(f"{date} {end_hour}")

        return Conference(course, start_time, end_time, url)
