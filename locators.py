# locators.py file
from selenium.webdriver.common.by import By

class LoginLocators:
    LOGIN_ICON = (By.XPATH, "//a[contains(@href, '/user/login')] | //a[@title='My Account']")
    EMAIL_FIELD = (By.XPATH, "//input[@id='edit-name']")
    PASSWORD_FIELD = (By.XPATH, "//input[@id='edit-pass']")
    SUBMIT_BUTTON = (By.XPATH, "//input[@id='edit-submit']")