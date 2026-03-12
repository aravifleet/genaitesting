import re
import csv
import os
from playwright.sync_api import Playwright, sync_playwright, expect

# Folder setup for screenshots
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def run_checkout(page, data, row_count):
    print(f"🔄 [Row {row_count}] Processing: {data['email']}")
    
    # 1. Navigate to URL
    page.goto("https://live-icsample1657400753.pantheonsite.io/")
    
    # 2. Add to Cart Logic
    page.get_by_role("link", name="Books", exact=True).click()
    page.locator("#product-variation-wrapper--137374").get_by_role("link", name="Add to Cart").click()
    page.locator("#product-variation-wrapper--137294").get_by_role("link", name="Add to Cart").click()
    page.locator("#product-variation-wrapper--137295").get_by_role("link", name="Add to Cart").click()
    
    # 3. Checkout flow
    page.get_by_role("link", name=re.compile(r"Cart \d+ items")).click()
    page.get_by_role("button", name="Checkout").click()
    page.get_by_role("button", name="Continue as Guest").click()
    
    # 4. Form Filling
    page.get_by_role("textbox", name="Email *", exact=True).fill(data['email'])
    page.get_by_role("textbox", name="Confirm email *").fill(data['email'])
    page.get_by_role("textbox", name="label changed to rename *").fill(f"{data['first_name']} {data['last_name']}")
    page.get_by_role("textbox", name="Phone *").fill(data['phone'])
    page.get_by_role("textbox", name="First name *").fill(data['first_name'])
    page.get_by_role("textbox", name="Last name *").fill(data['last_name'])
    page.get_by_role("textbox", name="Street address *").fill(data['address1'])
    page.get_by_role("textbox", name="City *").fill(data['city'])
    page.get_by_label("State (required)").select_option(data['state'])
    page.get_by_role("textbox", name="Zip code *").fill(data['zip'])
    
    # 5. Shipping Selection Stability
    page.get_by_text(data['shipping_method']).click()
    page.wait_for_load_state("networkidle")
    
    # 6. Payment Method Selection (Keyboard Arrow Logic)
    print(f"💳 Selecting Payment Method for Row {row_count}...")
    
    # Click PayPal to establish focus
    paypal_radio = page.get_by_role("radio", name="PayPal")
    paypal_radio.wait_for(state="visible", timeout=10000)
    paypal_radio.click()
    
    # Wait for focus to settle
    page.wait_for_timeout(1000) 
    
    # Sequence: PayPal -> Credit Card -> Purchase Order -> House Account
    page.keyboard.press("ArrowDown") 
    page.wait_for_timeout(400)
    page.keyboard.press("ArrowDown") 
    page.wait_for_timeout(400)
    page.keyboard.press("ArrowDown") 
    page.wait_for_timeout(400)
    page.keyboard.press("Enter")     
    
    # Specific click to handle potential strict mode/DOM issues
    page.locator("label.option", has_text="House Account").click()
    
    # 7. House Account Field Stability
    page.wait_for_load_state("networkidle")
    
    house_field = page.get_by_role("textbox", name="House Account Number *")
    house_field.wait_for(state="visible", timeout=15000)
    
    house_field.click() 
    house_field.fill(data['paymentvalue'])
    house_field.press("Tab") 
    
    # 8. Final Review & Purchase
    continue_btn = page.get_by_role("button", name="Continue to review")
    expect(continue_btn).to_be_enabled(timeout=10000)
    
    page.get_by_role("textbox", name="Customer Comments").fill(data['comments'])
    continue_btn.click()
    
    page.wait_for_load_state("networkidle")
    page.get_by_role("button", name="Complete Purchase").click()

    # 9. Completion & Screenshot
    page.wait_for_load_state("networkidle")
    screenshot_name = f"screenshots/Row_{row_count}_{data['first_name']}.png"
    page.screenshot(path=screenshot_name, full_page=True)
    print(f"✅ [Row {row_count}] Success: Screenshot saved for {data['first_name']}.")

def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        
        index = 0 
        
        try:
            if not os.path.exists('data1.csv'):
                print("❌ Error: data1.csv not found in the current directory.")
                return

            with open('data1.csv', mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for index, row in enumerate(reader, start=1):
                    page = context.new_page()
                    try:
                        run_checkout(page, row, index)
                    except Exception as e:
                        print(f"❌ [Row {index}] Failed: {e}")
                        page.screenshot(path=f"screenshots/FAILED_Row_{index}.png", full_page=True)
                    finally:
                        page.close()
                
                if index == 0:
                    print("⚠️ Warning: CSV file is empty.")
                else:
                    print(f"\n✨ Automation Task Completed. Total rows processed: {index}")

        except Exception as e:
            print(f"❌ Critical System Error: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    main()