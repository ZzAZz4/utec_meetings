import keyboard
import time

from src.page.locators import ZoomPageLocators
from src.browser.clickable_elem import ClickableElem
from src.browser.web_page import WebPage


class ZoomMeetingPage(WebPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.join_zoom_meeting = JoinZoomMeetingButton(self)
        self.join_zoom_popup = JoinZoomMeetingPopup()
    
    def click_join(self):
        self.join_zoom_meeting.click()
        
    def accept_popup(self):
        self.join_zoom_popup.accept()
        time.sleep(1)


class JoinZoomMeetingButton(ClickableElem):
    locator = ZoomPageLocators.JOIN_MEETING


class JoinZoomMeetingPopup(object):
    def accept(self):
        keyboard.press_and_release('left')
        keyboard.press_and_release('enter')
    