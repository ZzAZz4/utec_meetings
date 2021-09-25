from .wiretap import Wiretap
from ..data.conferences import Conference
import json


class ConferenceFetch:
    API_URL = 'https://api.utec.edu.pe/conference-api/v1/conference/list/meeting/student'

    def __request_callback(self, request):
        if request.url == self.API_URL:
            body = json.loads(request.body.decode('utf-8'))
            body['fechaInicio'] = self.start
            body['fechaFin'] = self.end
            
            modified_body = json.dumps(body, separators=(',', ':'))
            request.body = modified_body.encode('utf-8')
            
    def __init__(self, driver, start, end):
        self.start = start
        self.end = end
        self.wiretap = Wiretap(driver, self.__request_callback)

    def get_conferences(self):
        with self.wiretap as driver:
            request = driver.wait_for_request(self.API_URL, 1000)
        
        response_body = json.loads(request.response.body.decode('utf-8'))
        content = response_body['content']
        conference_data = map(Conference.from_json, content)
        return sorted(conference_data, key=lambda x: x.start)
