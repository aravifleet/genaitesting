from playwright.sync_api import sync_playwright
from locators import LoginLocators 
from data import TestData

def run_test():
    with sync_playwright() as p:
        # slow_mo kudutha dhaan browser epdi work aagudhu nu paaka mudiyum
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page() 
        
        try:
            page.goto(TestData.BASE_URL)
            print(f"✅ Navigated to: {TestData.BASE_URL}")

            # [1] remove panniyachu, direct string usage
            page.click(LoginLocators.LOGIN_ICON) 

            page.fill(LoginLocators.EMAIL_FIELD, TestData.USER_EMAIL)
            print("✅ Email entered")

            page.fill(LoginLocators.PASSWORD_FIELD, TestData.USER_PASSWORD)
            print("✅ Password entered")

            page.click(LoginLocators.SUBMIT_BUTTON)
            print("🚀 Login Successful with Playwright!")

        except Exception as e:
            print(f"❌ Error occurred: {e}")
        
        finally:
            browser.close()

if __name__ == "__main__":
    run_test()