import time
from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import allure
from Environment import *
# Configuration Import
from Configuration import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses TensorFlow warnings

@given('I lunched the TNA Login Page')
def step_impl(context):
    options = Options()
    options.add_experimental_option('detach', False)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--ignore-ssl-errors")
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(10)
    context.driver.maximize_window()
    context.driver.get(DEV_URL)

@given('Enter the valid username and password')
def step_impl(context):
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys(VALID_USERNAME)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys(VALID_PASSWORD)
    time.sleep(1)

@given('Enter the invalid username and password')
def step_impl(context):
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys("Invalid_Username")
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys("Invalid_Password")
    time.sleep(1)

@given('Enter the valid username and invalid password')
def step_impl(context):
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys(VALID_USERNAME)
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys("wrong_password")
    time.sleep(1)

@given('Enter the invalid username and valid password')
def step_impl(context):
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys("Admin1")
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys(VALID_PASSWORD)
    time.sleep(1)

@given('Enter the no username and password')
def step_impl(context):
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_USERNAME_XPATH).send_keys("")
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_PASSWORD_XPATH).send_keys("")
    time.sleep(1)

@when('Click on the signin button')
def step_impl(context):
    context.driver.find_element(By.XPATH, LOGIN_SCREEN_SIGNIN_XPATH).click()
    time.sleep(2)

@then('Verify "{expected_message}" is displayed')
def step_impl(context, expected_message):
    ERROR_MESSAGES = {
        "home dashboard": EXPECTED_URL,
        "Invalid username or password": ERROR_MESSAGE_XPATH,
        "Incorrect password": ERROR_MESSAGE_XPATH,
        "Username and password cannot be blank": "//div[contains(text(),'Username is required')] | //div[contains(text(),'Password is required')]",
        "error message": ERROR_MESSAGE_XPATH
    }

    if expected_message == "home dashboard":
        current_url = context.driver.current_url
        assert current_url == EXPECTED_URL, f"Expected URL '{EXPECTED_URL}', but got '{current_url}'."
        print("Test Pass - Login successful with valid credentials")
    else:
        error_xpath = ERROR_MESSAGES.get(expected_message)
        assert error_xpath, f"No XPath mapping found for message: {expected_message}"
        try:
            error_element = context.driver.find_element(By.XPATH, error_xpath)
            assert error_element.is_displayed(), f"Expected message '{expected_message}' is not displayed on the page."
            print(f"Test Pass - Correct error message displayed: '{expected_message}'")
        except Exception as e:
            print(f"Test Fail - Error message validation failed: {str(e)}")
            raise
