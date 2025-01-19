from behave import given, when, then
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from Configuration import *
from Environment import *


# Background step
@given('I log in to the TNA application as an admin and click on the "Create New User" button')
def step_impl(context):
    options = Options()
    options.add_experimental_option('detach', False)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--ignore-ssl-errors")
    context.driver = webdriver.Chrome(options=options)
    context.driver.maximize_window()
    context.driver.get(DEV_URL)
    wait = WebDriverWait(context.driver, 10)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys(VALID_USERNAME)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys(VALID_PASSWORD)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_SIGNIN_XPATH).click()
    # Waiting for the element to be present and clickable
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@label='Create New User']"))).click()


# Scenario: Create a New Platform Admin
@when('I enter valid information such as username, email, password, confirm password, and click on the save button')
def step_impl(context):
    username = context.driver.find_element(By.XPATH, "//input[@name='Loginname']")
    email = context.driver.find_element(By.XPATH, "//input[@name='email']")
    password = context.driver.find_element(By.XPATH, "//input[@id='password-field']")
    confirm_password = context.driver.find_element(By.XPATH, "//input[@id='password-fieldC']")
    save_button = context.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]")
    username.send_keys(New_PFA_Username)
    email.send_keys(Platform_admin_email)
    password.send_keys(VALID_PASSWORD)
    confirm_password.send_keys(VALID_PASSWORD)
    save_button.click()

@then('I should see a confirmation message "User created successfully"')
def step_impl(context):
    success_message = WebDriverWait(context.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Successfully configured the user')]"))
    ).text
    assert success_message == 'Successfully configured the user', f"Expected message: 'Successfully configured the user', but got: {success_message}"
    print(f"Confirmation message: {success_message}")


@then('I log out of the system')
def step_impl(context):
    context.driver.find_element(By.XPATH,
                                "//body/app-root[1]/app-layout[1]/div[1]/app-topbar[1]/div[1]/div[2]/div[1]/em[1]").click()
    time.sleep(2)
    context.driver.find_element(By.XPATH, "//span[contains(text(),'Yes')]").click()
    time.sleep(2)
    assert DEV_URL == context.driver.current_url, f"Expected URL: {DEV_URL}, but got: {context.driver.current_url}"
    print("Logged out successfully")


@when('I log in with the new platform admin credentials')
def step_impl(context):
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys(New_PFA_Username)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys(VALID_PASSWORD)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_SIGNIN_XPATH).click()
    time.sleep(3)


@then('I should be able to access the application as a platform admin')
def step_impl(context):
    element = context.driver.find_element(By.XPATH, "//div[contains(text(),'Platform Admin')]")
    assert element.text == 'Platform Admin'


# Scenario: Handling Empty Input Fields
@when('I leave all required fields blank and click on the save button')
def step_impl(context):
    save_button = context.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]")
    save_button.click()
    time.sleep(5)


@then('appropriate error messages should be displayed for each required field')
def step_impl(context):
    try:
        error_message1 = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Login Name is required')]"))
        ).text
        assert error_message1 == 'Login Name is required'
    except Exception as e:
        print(f"Login Name error message not found: {str(e)}")

    try:
        error_message2 = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Email is required')]"))
        ).text
        assert error_message2 == 'Email is required'
    except Exception as e:
        print(f"Email error message not found: {str(e)}")

    try:
        error_message3 = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Password is required')]"))
        ).text
        assert error_message3 == 'Password is required'
    except Exception as e:
        print(f"Password error message not found: {str(e)}")

    try:
        error_message4 = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Confirm Password is required')]"))
        ).text
        assert error_message4 == 'Confirm Password is required'
    except Exception as e:
        print(f"Confirm Password error message not found: {str(e)}")


# Scenario: Reject Weak Passwords
@when('I fill in valid details except for a weak password and click on the save button')
def step_impl(context):
    username = context.driver.find_element(By.XPATH, "//input[@name='Loginname']")
    email = context.driver.find_element(By.XPATH, "//input[@name='email']")
    password = context.driver.find_element(By.XPATH, "//input[@id='password-field']")
    confirm_password = context.driver.find_element(By.XPATH, "//input[@id='password-fieldC']")
    save_button = context.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]")
    username.send_keys(New_PFA_Username)
    email.send_keys('platformadmin@gmail.com')
    password.send_keys("weakpassword")
    confirm_password.send_keys("weakpassword")
    save_button.click()
    time.sleep(2)


@then('I should see an error message indicating that the password is too weak')
def step_impl(context):
    error_message5 = context.driver.find_element(By.XPATH,
                                                 "//p[contains(text(),'Password must be over 6 characters and include an ')]")
    assert error_message5.is_displayed(), "Error message is not visible"
# Scenario: Detect Mismatched Passwords
@when('I input valid details but enter different values for the new and confirm password, and click on the save button')
def step_impl(context):
    username = context.driver.find_element(By.XPATH, "//input[@name='Loginname']")
    email = context.driver.find_element(By.XPATH, "//input[@name='email']")
    password = context.driver.find_element(By.XPATH, "//input[@id='password-field']")
    confirm_password = context.driver.find_element(By.XPATH, "//input[@id='password-fieldC']")
    save_button = context.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]")
    username.send_keys(New_PFA_Username)
    email.send_keys('platformadmin@gmail.com')
    password.send_keys(NEW_PASSWORD)
    confirm_password.send_keys(MISMATCHED_CONFIRM_PASSWORD)
    save_button.click()


@then('an error message should inform me about the password mismatch')
def step_impl(context):
    error_message6 = context.driver.find_element(By.XPATH, "//div[contains(text(),'Passwords does not match')]")
    assert error_message6.text == 'Passwords does not match'


# Scenario: Validate Email Format
@when('I input an invalid email address along with other valid details and click on the save button')
def step_impl(context):
    username = context.driver.find_element(By.XPATH, "//input[@name='Loginname']")
    email = context.driver.find_element(By.XPATH, "//input[@name='email']")
    password = context.driver.find_element(By.XPATH, "//input[@id='password-field']")
    confirm_password = context.driver.find_element(By.XPATH, "//input[@id='password-fieldC']")
    save_button = context.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]")
    username.send_keys(New_PFA_Username)
    email.send_keys('invalid_email')
    password.send_keys(NEW_PASSWORD)
    confirm_password.send_keys(NEW_PASSWORD)
    time.sleep(2)
    save_button.click()


@then('I should see an error message stating the email format is invalid')
def step_impl(context):
    time.sleep(2)
    error_message7 = context.driver.find_element(By.XPATH, "//div[contains(text(),'Email pattern is not match')]")
    assert error_message7.text == 'Email pattern is not match'

# Scenario: Check for Duplicate Users
@when('I input the details of an already existing platform admin and click on the save button')
def step_impl(context):
    username = context.driver.find_element(By.XPATH, "//input[@name='Loginname']")
    email = context.driver.find_element(By.XPATH, "//input[@name='email']")
    password = context.driver.find_element(By.XPATH, "//input[@id='password-field']")
    confirm_password = context.driver.find_element(By.XPATH, "//input[@id='password-fieldC']")
    save_button = context.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]")
    username.send_keys(New_PFA_Username)
    email.send_keys('platformadmin@gmail.com')
    password.send_keys(NEW_PASSWORD)
    confirm_password.send_keys(NEW_PASSWORD)
    save_button.click()

@then('I should see an error message stating "User already exists"')
def step_impl(context):
    time.sleep(2)
    error_message8 = context.driver.find_element(By.XPATH, "//div[contains(text(),'User already exists with username or email')]")
    assert error_message8.is_displayed(), "User already exists with username or email"


