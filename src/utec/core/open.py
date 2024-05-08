from selenium import webdriver
from selenium.webdriver.common.by import By
from utec.core.driver import WrappedWebdriver
import keyboard
import time
from utec.core.conference import Conference

JOIN_BUTTON_XPATH = '//*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div'


def open_conference(conference: Conference):
    if conference.url is None:
        print("No url to join")
        return

    sdriver = webdriver.Chrome()

    with WrappedWebdriver(sdriver) as driver:
        driver.get(conference.url)

        join_button = driver.find_element(By.XPATH, JOIN_BUTTON_XPATH)
        join_button.click()

        # accept the popup
        keyboard.press_and_release('left')
        keyboard.press_and_release('enter')
        time.sleep(1)
