from loguru import logger
from selenium.webdriver.common.by import By

from utec.core.driver import WrappedWebdriver

LOGIN_BTN_XPATH = '/html/body/div/div/div[2]/button'
UNAME_INPUT_XPATH = '//*[@id="identifierId"]'
PWD_INPUT_XPATH = '//*[@id="password"]/div[1]/div/div[1]/input'
CONFERENCE_BTN_XPATH = '//*[@id="app"]/div[1]/div/div/div[1]/div/div[2]/button'
CONFERENCE_BTN_XPATH = '//*[@id="app"]/div[1]/div/div/div[1]/div/div[2]/button'


def login(driver: WrappedWebdriver, username: str, password: str):
    driver.get('https://sistema-academico.utec.edu.pe/access')

    login_button = driver.find_element(By.XPATH, LOGIN_BTN_XPATH)
    login_button.click()
    logger.info("Clicked login button")

    uname_input = driver.find_element(By.XPATH, UNAME_INPUT_XPATH)
    uname_input.click()
    uname_input.send_keys(username + '\n')
    logger.info("Sent username")

    pwd_input = driver.find_element(By.XPATH, PWD_INPUT_XPATH)
    pwd_input.click()
    pwd_input.send_keys(password + '\n')
    logger.info("Sent password")

    logger.info("Waiting for initial conference page to load...")
    conf_btn = driver.find_element(By.XPATH, CONFERENCE_BTN_XPATH, timeout=120)
    conf_btn.click()
    logger.info("Redirecting to real conference page...")

    driver.switch_tab(1)
    login_button = driver.find_element(By.XPATH, LOGIN_BTN_XPATH)
    login_button.click()
    logger.info("Clicked login button (again...)")

    driver.get("https://conference.utec.edu.pe/consulta-alumno")
    logger.info("Logged in!")
