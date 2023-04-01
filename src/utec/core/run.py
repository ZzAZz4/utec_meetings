from utec.core.driver import WrappedWiredWebdriver
from utec.core.intercept import intercept_request_content
from utec.core.login import login

from pyvirtualdisplay.display import Display
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from loguru import logger

def get_conference_json(username: str, password: str, start: str, end: str):
    display = Display(visible=False, size=(800, 600))
    display.start()

    path = ChromeDriverManager().install()
    options = Options()
    options.add_argument("--disable-gpu")
    sdriver = webdriver.Chrome(path, options=options)
    logger.info("Starting driver...")


    with WrappedWiredWebdriver(sdriver) as driver:
        login(driver, username, password)
        content = intercept_request_content(driver, start, end)
    
    display.stop()
    return content