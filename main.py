from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    print("Searching for 'Google' section...")
    google_section = wait.until(EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR, 
         'new UiScrollable(new UiSelector().scrollable(true))'
         '.scrollIntoView(new UiSelector().text("Google"))')
    ))
    
    google_section.click()
    
    time.sleep(5)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()