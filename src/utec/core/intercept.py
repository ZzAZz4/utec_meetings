from utec.core.driver import WrappedWiredWebdriver
from utec.core.progress import ProgressIndicator, EmptyProgressIndicator

from seleniumwire.request import Request
from typing import Any
import json
from loguru import logger

API_URL = 'https://api.utec.edu.pe/conference-api/v1/conference/list/meeting/student'

class RequestInterceptor:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def intercept_request(self, request: Request):
        if request.url == API_URL:
            body = json.loads(request.body.decode('utf-8'))
            body['fechaInicio'] = self.start
            body['fechaFin'] = self.end
            
            modified_body = json.dumps(body, separators=(',', ':'))
            request.body = modified_body.encode('utf-8')

def intercept_request_content(driver: WrappedWiredWebdriver, start, end, progress: ProgressIndicator) -> list[dict[str, Any]]:
    interceptor = RequestInterceptor(start, end)
    driver.request_interceptor = interceptor.intercept_request
    
    driver.get("https://conference.utec.edu.pe/consulta-alumno")
    progress.set_description("Redirected to conference page")
    progress.update(10)

    request = driver.wait_for_request(API_URL, timeout=200)
    assert request.response 

    progress.set_description("Request intercepted")
    progress.update(10)
    
    response_body = json.loads(request.response.body.decode('utf-8'))
    content = response_body['content']
    return content