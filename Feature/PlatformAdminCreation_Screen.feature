@order_2
Feature: Platform Admin Management
  As an admin user, I want to manage platform admins effectively
  by creating new users and validating input fields properly.

  Background:
    Given I log in to the TNA application as an admin and click on the "Create New User" button
  @Positive
  Scenario: Create a New Platform Admin
    When I enter valid information such as username, email, password, confirm password, and click on the save button
    Then I should see a confirmation message "User created successfully"
    And I log out of the system
    When I log in with the new platform admin credentials
    Then I should be able to access the application as a platform admin

  @Negative
  Scenario: Handling Empty Input Fields
    When I leave all required fields blank and click on the save button
    Then appropriate error messages should be displayed for each required field

  @Negative
  Scenario: Reject Weak Passwords
    When I fill in valid details except for a weak password and click on the save button
    Then I should see an error message indicating that the password is too weak

  @Negative
  Scenario: Detect Mismatched Passwords
    When I input valid details but enter different values for the new and confirm password, and click on the save button
    Then an error message should inform me about the password mismatch

  @Negative
  Scenario: Validate Email Format
    When I input an invalid email address along with other valid details and click on the save button
    Then I should see an error message stating the email format is invalid

  @Negative
  Scenario: Check for Duplicate Users
    When I input the details of an already existing platform admin and click on the save button
    Then I should see an error message stating "User already exists"
