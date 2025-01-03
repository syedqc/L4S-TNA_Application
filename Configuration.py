# Configuration

# URLs
DEV_URL = "http://158.176.9.148:30026/#/login"
EXPECTED_URL = "http://158.176.9.148:30026/#/Controls/userconfig"

# Login Page Locators
VALID_USERNAME = "Admin"
VALID_PASSWORD = "Mnbv#121"
ERROR_MESSAGE_XPATH = "//div[contains(text(),'You have entered invalid User Name or Password')]"
LOGIN_SCREEN_USERNAME_XPATH = "//input[@placeholder='Email address']"
LOGIN_SCREEN_PASSWORD_XPATH = "//input[@placeholder='Password']"
LOGIN_SCREEN_SIGNIN_XPATH = "//span[contains(text(),'Sign In')]"

# Platform Admin Locators
CREATE_ADMIN_BUTTON_XPATH = "//button[@label='Create New User']"
PLATFORM_ADMIN_USERNAME_XPATH = "//input[@name='Loginname']"
PLATFORM_ADMIN_EMAIL_XPATH = "//input[@placeholder='Enter Email Address ']"
PLATFORM_ADMIN_PASSWORD_XPATH = "//input[@id='password-field']"
PLATFORM_ADMIN_RECONFIRM_PASSWORD_XPATH = "//input[@id='password-fieldC']"
SAVE_BUTTON_XPATH = "//button[contains(text(),'Save')]"

# Admin Password Change Functionality
NEW_PASSWORD = "Mnbv#122"
WEAK_PASSWORD = "wrong_password"
MISMATCHED_CONFIRM_PASSWORD = "password123"
NEW_PASSWORD_FIELD_XPATH = "//input[@id='password-fieldP']"
CONFIRM_PASSWORD_FIELD_XPATH = "//input[@id='password-fieldS']"
ADMIN_SAVE_BUTTON_XPATH = "//button[contains(text(),'Save Changes')]"

# Platform Creation Form Locators
PLATFORM_USERNAME_XPATH = "//input[@name='Loginname']"
PLATFORM_EMAIL_XPATH = "//input[@name='email']"
PLATFORM_PASSWORD_XPATH = "//input[@name='newpassword']"
PLATFORM_CONFIRM_PASSWORD_XPATH = "//input[@name='retypepassword']"
PLATFORM_SAVE_BUTTON_XPATH = "//button[contains(text(),'Save')]"
