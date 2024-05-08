from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    from selenium.webdriver import Chrome, Firefox
    from seleniumwire.webdriver import Chrome as WiredChrome
    from seleniumwire.webdriver import Firefox as WiredFirefox
    from selenium.webdriver.remote.webelement import WebElement

    WiredDriver = Union[WiredChrome, WiredFirefox]
    Driver = Union[Chrome, Firefox, WiredChrome, WiredFirefox]
else:
    WiredDriver = 'WiredDriver'
    Driver = 'Driver'


def get_webdriver(type: str) -> 'Driver':
    if type == 'chrome':
        driver = get_chrome_driver()
    elif type == 'firefox':
        driver = get_firefox_driver()
    else:
        raise ValueError(f"Invalid driver type: {type}")

    return driver


def get_wired_webdriver(type: str) -> 'WiredDriver':
    if type == 'chrome':
        driver = get_wired_chrome_driver()
    elif type == 'firefox':
        driver = get_wired_firefox_driver()
    else:
        raise ValueError(f"Invalid driver type: {type}")

    return driver


def get_chrome_driver() -> 'Chrome':
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium import webdriver

    path = ChromeDriverManager().install()
    service = Service(path)
    options = Options()
    options.add_argument("--disable-gpu")
    sdriver = webdriver.Chrome(service=service, options=options)
    return sdriver


def get_wired_chrome_driver() -> 'WiredChrome':
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from seleniumwire import webdriver

    path = ChromeDriverManager().install()
    service = Service(path)
    options = Options()
    options.add_argument("--disable-gpu")
    sdriver = webdriver.Chrome(service=service, options=options)
    return sdriver


def get_firefox_driver() -> 'Firefox':
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from selenium import webdriver

    path = GeckoDriverManager().install()
    service = Service(path)
    options = Options()
    options.add_argument("--disable-gpu")
    sdriver = webdriver.Firefox(service=service, options=options)
    return sdriver


def get_wired_firefox_driver() -> 'WiredFirefox':
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from seleniumwire import webdriver

    path = GeckoDriverManager().install()
    service = Service(path)
    options = Options()
    options.add_argument("--disable-gpu")
    sdriver = webdriver.Firefox(service=service, options=options)
    return sdriver


class FindWithWait:
    def __init__(self, driver: 'Driver'):
        self.driver = driver

    def find_element(
        self, by: str, value: str, timeout: float = 10,
        wait_until=EC.visibility_of_element_located
    ) -> 'WebElement':
        wait = WebDriverWait(self.driver, timeout=timeout)
        return wait.until(wait_until((by, value)))
