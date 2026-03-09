from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from locators import LoginLocators 
from data import TestData # <--- Pudhu import
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 15)

try:
    driver.maximize_window()
    
    # Action: Get URL from data.py
    driver.get(TestData.BASE_URL)
    print(f"✅ Navigated to: {TestData.BASE_URL}")

    # Action: Click Login Icon
    wait.until(EC.element_to_be_clickable(LoginLocators.LOGIN_ICON)).click()

    # Action: Enter Email from data.py
    email_input = wait.until(EC.presence_of_element_located(LoginLocators.EMAIL_FIELD))
    email_input.send_keys(TestData.USER_EMAIL)
    print("✅ Email entered from data.py")

    # Action: Enter Password from data.py
    password_input = driver.find_element(*LoginLocators.PASSWORD_FIELD)
    password_input.send_keys(TestData.USER_PASSWORD)
    print("✅ Password entered from data.py")

    # Action: Submit
    driver.find_element(*LoginLocators.SUBMIT_BUTTON).click()

    print("🚀 Login Successful with Data & Locators separation!")

finally:
    driver.quit()