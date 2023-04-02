import os
from sys import platform


def get_start_command():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        return "xdg-open"
    elif platform == "win32":
        return "start \"\""
    else:
        raise Exception("Unsupported platform: " + platform)


def auto_open_conference_from_id(cid: str, pwd: str | None = None):
    pwd = pwd if pwd is not None else ''
    url = "zoommtg://zoom.us/join?confno=" + cid + "&pwd=" + pwd
    start_command = get_start_command()
    os.system('{} "{}"'.format(start_command, url))


def legacy_open_conference(url: str):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from utec.core.driver import make_driver
    import time
    import pynput

    JOIN_BUTTON_XPATH = '//*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div'

    keyboard = pynput.keyboard.Controller()

    service = Service(ChromeDriverManager().install())
    with make_driver(cls=webdriver.Chrome, service=service) as driver:
        driver.get(url)    

        join_button = driver.find_element(By.XPATH, JOIN_BUTTON_XPATH)
        join_button.click()

        keyboard.press(pynput.keyboard.Key.left)
        keyboard.release(pynput.keyboard.Key.left)
        keyboard.press(pynput.keyboard.Key.enter)
        keyboard.release(pynput.keyboard.Key.enter)

        time.sleep(3)

def open_conference(url: str | None, legacy: bool = False):
    if url is None:
        return
    
    if not legacy:
        cid = url.split('/')[-1]
        auto_open_conference_from_id(cid)
    else:
        legacy_open_conference(url)
        
    
    