import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then
import allure
from Configuration import *
# Global wait timeout
WAIT_TIMEOUT = 10

def wait_for_element(context, locator, by=By.XPATH):
    """Reusable wait function to wait for an element to be present."""
    return WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((by, locator))
    )
@given("I am logged in as a platform administrator")
def step_logged_in_as_admin(context):
    with allure.step("Log in as a platform administrator"):
        options = Options()
        options.add_experimental_option('detach', False)
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-web-security")
        context.driver = webdriver.Chrome(options=options)
        context.driver.implicitly_wait(WAIT_TIMEOUT)
        context.driver.maximize_window()
        context.driver.get(DEV_URL)
        context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys(New_PFA_Username)
        context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys(VALID_PASSWORD)
        time.sleep(1)
        context.driver.find_element(By.XPATH, LOGIN_SCREEN_SIGNIN_XPATH).click()
        time.sleep(2)
        if EXPECTED_URL == context.driver.current_url:
            print("Logged Successfully")
        else:
            print("Login failed")

@given("I navigate to the User Management section to update the password")
def step_navigate_to_user_management(context):
    with allure.step("Navigate to the User Management section"):
        time.sleep(1)
        element = context.driver.find_element(By.XPATH, "//span[contains(text(),'Controls')]")
        context.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        context.driver.execute_script("arguments[0].click();", element)
        WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Users')]"))).click()
        time.sleep(2)
        context.driver.find_element(By.XPATH, "//span[contains(text(),'Change Password')]").click()


@when("I enter a new password that does not match the confirm password")
def step_enter_mismatched_passwords(context):
    with allure.step("Enter mismatched new and confirm passwords"):
        time.sleep(2)
        context.driver.find_element(By.XPATH, PFA_Newpwd_Locator).send_keys(NEW_PASSWORD)
        context.driver.find_element(By.XPATH, PFA_ConfrimNewpwd_Locator).send_keys(MISMATCHED_CONFIRM_PASSWORD)
        context.driver.find_element(By.XPATH, PFA_SaveChanges_Locator).click()

@then('an error message "Passwords do not match" is displayed')
def step_verify_mismatched_password_error(context):
    with allure.step("Verify error message for mismatched passwords"):
        time.sleep(2)
        error_message = wait_for_element(context, "//div[contains(text(),'Passwords does not match')]").text
        assert error_message == 'Passwords does not match', f'Error message: {error_message}'
        print("Error message 'Passwords do not match' is displayed.")

@when("I leave the new password and confirm password fields blank")
def step_leave_password_fields_blank(context):
    with allure.step("Leave password fields blank"):
        context.driver.find_element(By.XPATH, PFA_Newpwd_Locator).send_keys("")
        context.driver.find_element(By.XPATH, PFA_ConfrimNewpwd_Locator).send_keys("")
        context.driver.find_element(By.XPATH, PFA_SaveChanges_Locator).click()


@then('an error message "Password fields cannot be empty" is displayed')
def step_verify_blank_password_error(context):
    with allure.step("Verify error message for blank password fields"):
        try:
            error_message = wait_for_element(context, "//div[contains(text(),'Password is required')]").text
            assert error_message == 'Password is required', f'Unexpected error message: {error_message}'
            print("Error message 'Password is required' is displayed.")
        except AssertionError as e:
            print(f"Assertion failed: {str(e)}")

        try:
            error_message1 = wait_for_element(context, "//div[contains(text(),'Confirm password is required')]").text
            assert error_message1 == 'Confirm password is required', f'Unexpected error message: {error_message1}'
            print("Error message 'Confirm password is required' is displayed.")
        except AssertionError as e:
            print(f"Assertion failed: {str(e)}")


@when("I enter a password that does not meet the required complexity standards")
def step_enter_weak_password(context):
    with allure.step("Enter a weak password"):
        context.driver.find_element(By.XPATH, PFA_Newpwd_Locator).send_keys(WEAK_PASSWORD)
        context.driver.find_element(By.XPATH, PFA_ConfrimNewpwd_Locator).send_keys(NEW_PASSWORD)
        context.driver.find_element(By.XPATH, PFA_SaveChanges_Locator).click()


@then('an error message "Password must include uppercase, lowercase, numbers, and special characters" is displayed')
def step_verify_weak_password_error(context):
    with allure.step("Verify error message for weak password"):
        time.sleep(2)
        error_message = wait_for_element(context, "//p[contains(text(),'Password must be over 6 characters and include an ')]").text
        assert error_message == 'Password must be over 6 characters and include an uppercase letter, a number and a special character', f'Unexpected error message: {error_message}'



@when("I enter matching passwords that meet the required complexity standards")
def step_enter_valid_password(context):
    with allure.step("Enter a valid password"):
        context.driver.find_element(By.XPATH, PFA_Newpwd_Locator).send_keys(NEW_PASSWORD)
        context.driver.find_element(By.XPATH, PFA_ConfrimNewpwd_Locator).send_keys(NEW_PASSWORD)
        context.driver.find_element(By.XPATH, PFA_SaveChanges_Locator).click()


@then("the system logs me out automatically relogin with updated password")
def step_verify_auto_logout(context):
    with allure.step("Verify automatic logout"):
        time.sleep(2)
        if context.driver.current_url== DEV_URL:
            print("Auto logout successful")
            context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys(New_PFA_Username)
            context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys(NEW_PASSWORD)
            time.sleep(1)
            context.driver.find_element(By.XPATH, LOGIN_SCREEN_SIGNIN_XPATH).click()
        else:
            print("Auto logout failed")



@then("I am successfully logged in")
def step_verify_successful_login(context):
    with allure.step("Verify successful login"):
        Exp_URL = "http://158.176.9.148:30026/#/TapX/network"
        if context.driver.current_url == Exp_URL:
            print("Logged Successfully")
        else:
            print("Login failed")
