from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker
import random
import secrets
import time
import string

options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "emulator-5554",
    "appium:noReset": True,
    "appium:newCommandTimeout": 3600
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 20) 
fake = Faker()

def does_node_exist(selector):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, selector)
        ))
        return True
    except:
        return False

def generate_username():
    first = fake.first_name().lower().replace("'", "")
    last = fake.last_name().lower().replace("'", "")
    
    numbers = "".join(random.choices(string.digits, k=random.randint(4, 6)))
    
    username = f"{first}.{last}{numbers}"
    
    return username[:30]

def generate_password(length=12):
    letters_lower = string.ascii_lowercase
    letters_upper = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*" 
    
    password = [
        secrets.choice(letters_lower),
        secrets.choice(letters_upper),
        secrets.choice(digits),
        secrets.choice(special)
    ]
    
    all_chars = letters_lower + letters_upper + digits + special
    password += [secrets.choice(all_chars) for _ in range(length - 4)]
    
    secrets.SystemRandom().shuffle(password)
    
    return "".join(password)

def safe_click(selector_type, selector_value, name="element"):
    print(f"Waiting for {name}...")
    try:
        element = wait.until(EC.element_to_be_clickable((selector_type, selector_value)))
        element.click()
        return element
    except Exception as e:
        print(f"Failed to click {name}: {e}")
        return None

try:
    safe_click(AppiumBy.ACCESSIBILITY_ID, "Settings", "Settings Icon")

    print("Scrolling to Google...")
    scroll_ui = ('new UiScrollable(new UiSelector().scrollable(true))'
                 '.scrollIntoView(new UiSelector().text("Google"))')
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_ui)
    
    safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Google")', "Google Section")

    # account section, use bounds as fallback
    try:
        target_view = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '//android.view.View[@bounds="[11,210][1080,400]"]')
        ))
        target_view.click()
    except:
        print("XPath view not found, trying coordinate tap...")
        driver.tap([(545, 305)])

    # full text card
    safe_click(AppiumBy.ID, "com.google.android.gms:id/og_full_text_card_root", "Account Card")

    # create account and selection
    safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create account")', "Create Account Btn")
    safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("For my personal use")', "Personal Use Option")

    # first name
    first_name_selector = 'new UiSelector().resourceId("firstName")'
    wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, first_name_selector)))
    
    # specific screen location to trigger keyboard
    driver.tap([(539, 640)]) 
    time.sleep(1) # allow keyboard animation to finish
    
    first_name_field = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, first_name_selector)
    first_name_field.send_keys(fake.first_name())
    print("Entered First Name.")

    try:
        last_name_field = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("lastName")')
        last_name_field.click()
        last_name_field.send_keys(fake.last_name())
    except:
        print("Last name field skipped.")

    # combined selector to find "NEXT" or "Next"
    next_logic = 'new UiSelector().textMatches("(?i)next")' # Case-insensitive regex
    safe_click(AppiumBy.ANDROID_UIAUTOMATOR, next_logic, "Next Button")

    # birthday and gender
    months = ["March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
    genders = ["Male", "Female", "Rather not say"]

    r_month = random.choice(months)
    r_day = str(random.randint(1, 28))
    r_year = str(random.randint(1985, 2005))
    r_gender = random.choice(genders)

    try:
        print(f"Selecting Month: {r_month}")
        safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Spinner").instance(0)', "Month Spinner")
        time.sleep(1)
        safe_click(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{r_month}")', r_month)

        print(f"Entering Day: {r_day}")
        day_field = safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("day")', "Day Field")
        day_field.send_keys(r_day)

        print(f"Entering Year: {r_year}")
        year_field = safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("year")', "Year Field")
        year_field.send_keys(r_year)

        print(f"Selecting Gender: {r_gender}")
        safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Spinner").instance(1)', "Gender Spinner")
        
        safe_click(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{r_gender}")', r_gender)

        if driver.is_keyboard_shown():
            driver.hide_keyboard()
            
        safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("(?i)next")', "Next Button")

    except Exception as e:
        print(f"Safe click sequence failed: {e}")

    # custom username case
    if does_node_exist('new UiSelector().text("How you’ll sign in")'):
        try:
            username_selector = 'new UiSelector().className("android.widget.EditText")'

            wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, username_selector)))
        
            # specific screen location to trigger keyboard
            driver.tap([(410, 703)]) 
            time.sleep(1) # allow keyboard animation to finish
        
            username_field = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, username_selector)
            username_field.send_keys(generate_username())
            print("Entered Username.")

            next_logic = 'new UiSelector().textMatches("(?i)next")' 
            safe_click(AppiumBy.ANDROID_UIAUTOMATOR, next_logic, "Next Button")
        except Exception as e:
            print(f"Safe click sequence failed: {e}")
    else:
        # choose username case
        try:
            print("Checking for 'Create your own Gmail address' option...")
            
            create_own_selector = 'new UiSelector().text("Create your own Gmail address")'
            
            create_option = wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, create_own_selector)
            ))
            
            driver.tap([(94, 974)])
            print("Successfully selected 'Create your own' option.")

        except Exception as e:
            print(f"Failed to select Gmail option: {e}")

        try:
            username_field = wait.until(EC.presence_of_element_located(
                (AppiumBy.CLASS_NAME, "android.widget.EditText")
            ))
            
            username = generate_username()
            
            username_field.send_keys(username)
            print(f"Entered Username: {username}")
            
            if driver.is_keyboard_shown():
                driver.hide_keyboard()
                
            next_logic = 'new UiSelector().textMatches("(?i)next")' 
            safe_click(AppiumBy.ANDROID_UIAUTOMATOR, next_logic, "Next Button")

        except Exception as e:
            print(f"Error entering username: {e}")

    # password
    try:
        password_selector = 'new UiSelector().className("android.widget.EditText")'

        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, password_selector)))
    
        # specific screen location to trigger keyboard
        driver.tap([(539, 703)]) 
        time.sleep(1) # allow keyboard animation to finish
    
        username_field = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, password_selector)
        username_field.send_keys(generate_password())
        print("Entered Password.")

        next_logic = 'new UiSelector().textMatches("(?i)next")' 
        safe_click(AppiumBy.ANDROID_UIAUTOMATOR, next_logic, "Next Button")


    except Exception as e:
        print(f"Safe click sequence failed: {e}")

except Exception as e:
    print(f"Critical failure: {e}")

finally:
    time.sleep(5)
    driver.quit()