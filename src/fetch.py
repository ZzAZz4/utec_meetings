from seleniumwire.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import FakeUserAgent

from .page.app_main_page import AppMainPage
from .page.landing_page import LandingPage
from .page.gmail_login_page import GmailLoginPage

from .intercept.conference_interceptor import ConferenceInterceptor


def headless_options(user_agent=None):
    if user_agent is None:
        user_agent = random_user_agent()

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('log-level=3')
    return chrome_options


def random_user_agent() -> str:
    ua = FakeUserAgent(verify_ssl=False)
    user_agent: str = ua.random
    print(f"{user_agent=}")
    return user_agent


def fetch_conferences(email, password, start, end):
    landing_page_url = 'https://conference.utec.edu.pe/access'
    conference_page_url = 'https://conference.utec.edu.pe/consulta-alumno'
    
    options = headless_options()
    
    with Chrome(ChromeDriverManager().install(), chrome_options=options) as driver:
        driver.get(landing_page_url)
            
        landing_page = LandingPage(driver)
        landing_page.click_signin()
        
        login_page = GmailLoginPage(driver)
        login_page.login(email, password)
        
        app_main_page = AppMainPage(driver)
        app_main_page.wait_for_load()
        
        driver.get(conference_page_url)
        
        conference_interceptor = ConferenceInterceptor(driver, start, end)
        data = conference_interceptor.get_conferences()
            
        return data
