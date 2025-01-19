import os
import allure
from datetime import datetime
import time
from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from Configuration import *  # Ensure this is used properly


def before_all(context):
    """Set up a base screenshots folder before all tests."""
    os.makedirs("Screenshots", exist_ok=True)
    context.start_time = datetime.now().strftime("%d-%m-%Y_%I-%M%p")

    # Define Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Example option for headless mode

    # Initialize WebDriver with options
    context.driver = webdriver.Chrome(options=chrome_options)


def after_scenario(context, scenario):
    """Capture a screenshot after each scenario and store it in a structured format."""
    try:
        # Ensure the driver is initialized
        if context.driver:
            feature_name = os.path.basename(scenario.feature.filename).replace('.feature', '').replace(' ', '_')
            feature_folder = os.path.join("Screenshots", feature_name, context.start_time)
            os.makedirs(feature_folder, exist_ok=True)

            scenario_status = "Pass" if scenario.status == "passed" else "Fail"
            screenshot_name = f"{scenario_status}-{scenario.name.replace(' ', '_')}.png"
            screenshot_path = os.path.join(feature_folder, screenshot_name)

            context.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            with open(screenshot_path, "rb") as screenshot_file:
                allure.attach(
                    screenshot_file.read(),
                    name=f"{scenario.name} ({scenario_status})",
                    attachment_type=allure.attachment_type.PNG
                )
        else:
            print("Driver not initialized. Skipping screenshot capture.")

    except Exception as e:
        print(f"Failed to capture screenshot: {e}")


def after_all(context):
    """Clean up after all tests, including quitting the driver."""
    if context.driver:
        context.driver.quit()
        print("Driver quit.")
