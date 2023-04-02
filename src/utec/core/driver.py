from seleniumwire.request import Request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.switch_to import SwitchTo
import selenium.webdriver 
import seleniumwire.webdriver

from typing import Protocol, Callable, Any, Self


class ICondition(Protocol):
    def __call__(self, locator: tuple[str, str]) -> Callable[[
        'IWiredWebDriver'], Any]: ...


class IRequestInterceptor(Protocol):
    def __call__(self, request: Request): ...


class IWebDriver(Protocol):
    def get(self, url: str): ...

    def find_element(self, by: str = By.ID,
                     value: 'str | None' = None) -> WebElement: ...

    def close(self): ...
    def quit(self): ...
    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type, exc, traceback, /): ...

    @property
    def switch_to(self) -> SwitchTo: ...

    @property
    def window_handles(self) -> list[str]: ...


class IWiredWebDriver(IWebDriver, Protocol):
    def wait_for_request(
        self, url: str, timeout: 'int | float' = 10, /) -> Request: ...

    @property
    def request_interceptor(self) -> IRequestInterceptor | None: ...

    @request_interceptor.setter
    def request_interceptor(self, interceptor: IRequestInterceptor | None): ...


class Webdriver:
    def __init__(self, driver: IWebDriver):
        self.driver: IWebDriver = driver

    def close(self): self.driver.close()
    def quit(self): self.driver.quit()
    def __enter__(self): self.driver.__enter__(); return self
    def __exit__(self, exc_type, exc, traceback, /): self.driver.quit()

    def get(self, url: str):
        return self.driver.get(url)

    def find_element(self, by: str, value: str, timeout: float = 10,
                     wait_until: ICondition = EC.visibility_of_element_located) -> WebElement:
        wait = WebDriverWait(self.driver, timeout=timeout)
        return wait.until(wait_until((by, value)))

    def switch_tab(self, index: int):
        self.driver.switch_to.window(self.driver.window_handles[index])


class WiredWebdriver(Webdriver):
    def __init__(self, driver: IWiredWebDriver):
        super().__init__(driver)
        self.driver: IWiredWebDriver = driver

    def wait_for_request(self, url: str, timeout: float = 10) -> Request:
        return self.driver.wait_for_request(url, timeout)

    @property
    def request_interceptor(
        self) -> IRequestInterceptor | None: return self.driver.request_interceptor

    @request_interceptor.setter
    def request_interceptor(self, interceptor: IRequestInterceptor |
                            None): self.driver.request_interceptor = interceptor


def make_driver(cls: type[IWebDriver]=selenium.webdriver.Chrome, **kwargs) -> Webdriver:
    driver = cls(**kwargs)
    return Webdriver(driver)

def make_wired_webdriver(cls: type[IWiredWebDriver]=seleniumwire.webdriver.Chrome, **kwargs) -> WiredWebdriver:
    driver = cls(**kwargs)
    return WiredWebdriver(driver)