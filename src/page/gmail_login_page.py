from selenium.webdriver.common.keys import Keys

from ..browser.web_page import WebPage
from ..browser.writable_elem import WritableElem
from .locators import GmailPageLocators


class GmailLoginPage(WebPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.email_field = EmailField(self)
        self.password_field = PasswordField(self)
        
    def login(self, email, password):
        self.email_field.__set__(self, email + Keys.ENTER) 
        self.password_field.__set__(self, password + Keys.ENTER)
        
        
class EmailField(WritableElem):
    """Email text field on the GMail login page"""
    locator = GmailPageLocators.EMAIL_FIELD

    
class PasswordField(WritableElem):
    """Password text field on the GMail login page"""
    locator = GmailPageLocators.PASSW_FIELD
