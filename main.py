from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from faker import Faker

options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "emulator-5554",
    "appium:noReset": True,
    "appium:newCommandTimeout": 3600
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

try:
    print("Waiting for Home Screen...")
    wait = WebDriverWait(driver, 15)

    # click settings app
    settings_icon = wait.until(EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Settings")
    ))
    settings_icon.click()

    # find section node that has 'Google' in it then click 
    scrollable_ui = 'new UiScrollable(new UiSelector().scrollable(true))'

    print("Searching for 'Google' section...")
    
    try:
        # scroll until 'Google' appears
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                            value=f'{scrollable_ui}.scrollIntoView(new UiSelector().text("Google"))')
        
        # wait for google node to be clickable 
        google_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Google")')
        ))
        
        # click it once clickable
        google_btn.click()
        print("Successfully clicked Google.")
    
    except Exception as e:
        print(f"Failed to find or click Google: {e}")
    
    time.sleep(5)

    # click 'account' section 
    target_view = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, '//android.view.View[@bounds="[11,210][1080,400]"]'
    )))
    
    target_view.click()

    print("Looking for the Full Text Card...")
    try:
        card_root = wait.until(EC.presence_of_element_located(
            (AppiumBy.ID, "com.google.android.gms:id/og_full_text_card_root")
        ))

        actions = ActionChains(driver)
        actions.move_to_element(card_root).click().perform()
        
        print("Successfully clicked the account card.")

    except Exception as e:
        print(f"Standard click failed, attempting coordinate tap: {e}")
        # fallback: center of [131,778][975,868] is x=553, y=823
        driver.tap([(553, 823)])    
        print("Successfully clicked the View node.")

    print("Looking for 'Create account' button...")
    try:
        create_account_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create account")')
        ))
        
        create_account_btn.click()
        print("Clicked 'Create account'!")

    except Exception as e:
        print(f"Could not click 'Create account': {e}")
        driver.tap([(196, 1175)])

    print("Selecting 'For my personal use'...")
    try:
        personal_use_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("For my personal use")')
        ))
        
        personal_use_btn.click()
        print("Selected 'For my personal use'.")

    except Exception as e:
        print(f"Could not find the menu option: {e}")

    # names (First and last)
    fake = Faker()
    random_first = fake.first_name()
    try:
        print("Searching for First Name using UiSelector...")

        first_name_field = wait.until(EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("firstName")')
        ))

        driver.tap([(539, 640)])
        time.sleep(0.5)

        first_name_field.send_keys(random_first)
        print(f"Success! Entered: {random_first}")

        try:
            last_name_field = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("lastName")')
            last_name_field.click()
            last_name_field.send_keys(fake.last_name())
        except:
            print("Last name field not found, skipping...")

    except Exception as e:
        print(f"Even with UiSelector it failed: {e}")

    # next button
    try:
        print("Looking for the 'NEXT' button...")

        next_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("NEXT")')
        ))
        
        next_btn.click()
        print("Clicked NEXT successfully.")

    except Exception as e:
        print(f"Could not click NEXT: {e}")
        try:
            driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Next")').click()
        except:
            print("Fallback failed as well.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()