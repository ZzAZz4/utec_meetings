from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebElem(object):
    locator: tuple[str, str]
    
    def __init__(self, page, condition=EC.visibility_of_element_located):
        self.page = page
        self.condition = condition
        
    def wait_for_load(self, timeout=100):
        driver = self.page.driver
        wait = WebDriverWait(driver, timeout)
        return wait.until(self.condition(self.locator))
        