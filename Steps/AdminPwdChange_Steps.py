import os
import time
from behave import *
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Environment import *
# Configuration Import
from Configuration import *


@given('Logged as admin user')
def step_impl(context):
    options = Options()
    options.add_experimental_option('detach', False)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--ignore-ssl-errors")
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(10)
    context.driver.maximize_window()
    context.driver.get(DEV_URL)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys(VALID_USERNAME)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys(VALID_PASSWORD)
    time.sleep(1)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_SIGNIN_XPATH).click()


@when('I navigate to the dashboard and click on change password button')
def step_impl(context):
    try:
        # Wait until the 'Change Password' button is clickable and visible
        WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Change Password')]"))
        ).click()  # Click once it's visible and clickable
        print("Navigated to the password field and clicked on 'Change Password'.")
    except TimeoutException:
        print("Failed to find the 'Change Password' button within 10 seconds.")


@when('I enter a mismatched new and confirm password')
def step_impl(context):
    context.driver.find_element(By.XPATH, NEW_PASSWORD_FIELD_XPATH).send_keys(NEW_PASSWORD)
    context.driver.find_element(By.XPATH, CONFIRM_PASSWORD_FIELD_XPATH).send_keys(MISMATCHED_CONFIRM_PASSWORD)
    context.driver.find_element(By.XPATH, "//button[contains(text(),'Save Changes')]").click()

@then('I should see an error message "Passwords does not match"')
def step_impl(context):
    try:
        error_message_element = context.driver.find_element(By.XPATH, "//div[contains(text(),'Passwords does not match')]")
        assert error_message_element.is_displayed(), "Error message 'Passwords does not match' is not displayed."
        print("Error message 'Passwords do not match' is displayed.")
    except AssertionError as e:
        print(f"AssertionError: {str(e)}")
        context.driver.save_screenshot("password_mismatch_error_not_displayed.png")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

@when('I leave the new and confirm password fields blank')
def step_impl(context):
    context.driver.find_element(By.XPATH, NEW_PASSWORD_FIELD_XPATH).send_keys("")
    context.driver.find_element(By.XPATH, CONFIRM_PASSWORD_FIELD_XPATH).send_keys("")
    time.sleep(2)
    context.driver.find_element(By.XPATH, "//button[contains(text(),'Save Changes')]").click()


@then('I should see an error message "Password field cannot be empty"')
def step_impl(context):
    try:
        new_password_error = context.driver.find_element(By.XPATH, "//div[contains(text(),'New password is required')]")
        confirm_password_error = context.driver.find_element(By.XPATH,
                                                             "//div[contains(text(),'Confirm password is required')]")

        assert new_password_error.is_displayed(), "New password error message is not displayed."
        assert confirm_password_error.is_displayed(), "Confirm password error message is not displayed."

        print("Both error messages for empty password fields are displayed.")
    except AssertionError as e:
        print(f"AssertionError: {str(e)}")
        context.driver.save_screenshot("empty_password_fields_error_not_displayed.png")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


@when('I enter password that does not meet requirements')
def step_impl(context):
    context.driver.find_element(By.XPATH, NEW_PASSWORD_FIELD_XPATH).send_keys(WEAK_PASSWORD)
    context.driver.find_element(By.XPATH, CONFIRM_PASSWORD_FIELD_XPATH).send_keys(WEAK_PASSWORD)
    time.sleep(2)
    context.driver.find_element(By.XPATH, "//button[contains(text(),'Save Changes')]").click()

@then('I should see an error message "Password must meet complexity requirements"')
def step_impl(context):
    try:
        error_message_element = context.driver.find_element(By.XPATH, "//p[contains(text(),'Password must be over 6 characters and include an ')]")
        assert error_message_element.is_displayed(), "Error message 'Password must meet complexity requirements' is not displayed."
        print("Error message 'Password must meet complexity requirements' is displayed.")
    except AssertionError as e:
        print(f"AssertionError: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

@when('I enter a new and confirm password')
def step_impl(context):
    context.driver.find_element(By.XPATH, NEW_PASSWORD_FIELD_XPATH).send_keys(NEW_PASSWORD)
    context.driver.find_element(By.XPATH, CONFIRM_PASSWORD_FIELD_XPATH).send_keys(NEW_PASSWORD)
    time.sleep(2)
    context.driver.find_element(By.XPATH, "//button[contains(text(),'Save Changes')]").click()

@then('the application auto-logout')
def step_impl(context):
    time.sleep(2)  # Giving time for auto-logout to complete
    try:
        current_url = context.driver.current_url
        assert current_url == DEV_URL, f"Expected URL after logout: {DEV_URL}, but got: {current_url}"
        print("Application auto-logged out after changing password.")
    except AssertionError as e:
        print(f"AssertionError: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


@when('I login again with the new password')
def step_impl(context):
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys(VALID_USERNAME)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys(NEW_PASSWORD)
    time.sleep(1)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_SIGNIN_XPATH).click()


@then('I should logged successfully')
def step_impl(context):
    time.sleep(2)  # Giving time for auto-logout to complete
    try:
        current_url = context.driver.current_url
        assert current_url == EXPECTED_URL, f"Expected URL after logout: {EXPECTED_URL}, but got: {current_url}"
        print("Application auto-logged out after changing password.")
    except AssertionError as e:
        print(f"AssertionError: {str(e)}")
        context.driver.save_screenshot("auto_logout_failed.png")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")