from selenium.webdriver.common.by import By

from utec.core.driver import WrappedWebdriver

LOGIN_BTN_XPATH = '/html/body/div/div/div[2]/button'
UNAME_INPUT_XPATH = '//*[@id="identifierId"]'
PWD_INPUT_XPATH = '//*[@id="password"]/div[1]/div/div[1]/input'
CONFERENCE_BTN_XPATH = '//*[@id="app"]/div[1]/div/div/div[1]/div/div[3]/button'


def login(driver: WrappedWebdriver):
    driver.get('https://sistema-academico.utec.edu.pe/access')

    login_button = driver.find_element(By.XPATH, LOGIN_BTN_XPATH)
    login_button.click()

    conf_btn = driver.find_element(By.XPATH, CONFERENCE_BTN_XPATH, timeout=360)
    conf_btn.click()

    driver.switch_tab(1)
    login_button = driver.find_element(By.XPATH, LOGIN_BTN_XPATH)
    login_button.click()
