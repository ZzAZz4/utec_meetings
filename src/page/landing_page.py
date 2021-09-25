from ..browser.web_page import WebPage
from ..browser.clickable_elem import ClickableElem
from .locators import LandingPageLocators


class LandingPage(WebPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.signin_button = SignInWithGoogleButton(self)
                
    def click_signin(self):
        self.signin_button.click()
        
        
class SignInWithGoogleButton(ClickableElem):
    """ A sign-in button on the landing page.
        I would seriously want to skip this step, but it's impossible """
    locator = LandingPageLocators.SIGNIN_BUTTON
