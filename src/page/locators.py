from selenium.webdriver.common.by import By

class LandingPageLocators(object):
    """A class for the landing page element locators"""
    
    SIGNIN_BUTTON = (By.XPATH, '/html/body/div/div/div[2]/button')


class AppMainPageLocators(object):
    """A class for main page locators"""

    APP_LOADED = (By.ID, 'app')
    

class GmailPageLocators(object):
    """A class for gmail login page locators"""
    
    EMAIL_FIELD = (By.XPATH, '//*[@id="identifierId"]')
    PASSW_FIELD = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    
    
class ZoomPageLocators(object):
    """A class for holding Zoom page locators"""
    
    JOIN_MEETING = (By.XPATH, '//*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div')