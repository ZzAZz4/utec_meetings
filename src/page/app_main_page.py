from selenium.webdriver.support import expected_conditions as EC

from ..browser.web_page import WebPage
from ..browser.web_elem import WebElem
from .locators import AppMainPageLocators

class AppMainPage(WebPage):
    """Page representing the main UTEC Conference website"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.app = AppLoadedElement(self, EC.presence_of_element_located)    
            
    def wait_for_load(self, timeout=100):
        """Waits for the first element on the page to appear."""
        self.app.wait_for_load(timeout)
        

class AppLoadedElement(WebElem):
    """First object to appear on the screen"""
    locator = AppMainPageLocators.APP_LOADED
