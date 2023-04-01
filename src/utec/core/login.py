from loguru import logger
from selenium.webdriver.common.by import By

from utec.core.driver import WrappedWebdriver
from utec.core.progress import ProgressIndicator, EmptyProgressIndicator

LOGIN_BTN_XPATH = '/html/body/div/div/div[2]/button'
UNAME_INPUT_XPATH = '//*[@id="identifierId"]'
PWD_INPUT_XPATH = '//*[@id="password"]/div[1]/div/div[1]/input'
CONFERENCE_BTN_XPATH = '//*[@id="app"]/div[1]/div/div/div[1]/div/div[2]/button'
CONFERENCE_BTN_XPATH = '//*[@id="app"]/div[1]/div/div/div[1]/div/div[2]/button'


def login(driver: WrappedWebdriver, username: str, password: str, progress: ProgressIndicator):
    driver.get('https://sistema-academico.utec.edu.pe/access')

    login_button = driver.find_element(By.XPATH, LOGIN_BTN_XPATH)
    login_button.click()
    progress.set_description("Clicked login button")
    progress.update(10)

    uname_input = driver.find_element(By.XPATH, UNAME_INPUT_XPATH)
    uname_input.click()
    uname_input.send_keys(username + '\n')
    progress.set_description("Sent username")
    progress.update(10)

    pwd_input = driver.find_element(By.XPATH, PWD_INPUT_XPATH)
    pwd_input.click()
    pwd_input.send_keys(password + '\n')
    progress.set_description("Sent password")
    progress.update(10)

    conf_btn = driver.find_element(By.XPATH, CONFERENCE_BTN_XPATH, timeout=120)
    conf_btn.click()
    progress.set_description("Clicked conference button. Redirecting...")
    progress.update(30)

    driver.switch_tab(1)
    login_button = driver.find_element(By.XPATH, LOGIN_BTN_XPATH)
    login_button.click()
    progress.set_description("Clicked login button (again...)")
    progress.update(20)

