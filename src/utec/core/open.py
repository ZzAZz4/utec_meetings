from selenium.webdriver.common.by import By
from utec.core.driver import FindWithWait, get_webdriver
import keyboard
import time
from utec.core.conference import Conference
import os


JOIN_BUTTON_XPATH = '//*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div'


def open_conference(conference: Conference):
    if conference.url is None:
        print("No url to join")
        return

    driver_type = os.getenv('DRIVER_TYPE', 'chrome')

    with get_webdriver(driver_type) as driver:
        driver.get(conference.url)

        finder = FindWithWait(driver)
        join_button = finder.find_element(By.XPATH, JOIN_BUTTON_XPATH)
        join_button.click()

        # accept the popup
        keyboard.press_and_release('left')
        keyboard.press_and_release('enter')
        time.sleep(1)
