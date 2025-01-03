@order_3
Feature: TNA Admin Password Change Functionality

  Background:
    Given Logged as admin user

  @Negative
  Scenario: Attempt to change password with mismatched new and confirm password
    When I navigate to the dashboard and click on change password button
    And I enter a mismatched new and confirm password
    Then I should see an error message "Passwords does not match"

  @Negative
  Scenario: Attempt to change password with blank fields
    When I navigate to the dashboard and click on change password button
    And I leave the new and confirm password fields blank
    Then I should see an error message "Password field cannot be empty"

  @Negative
  Scenario: Attempt to change password that does not meet security norms
    When I navigate to the dashboard and click on change password button
    And I enter password that does not meet requirements
    Then I should see an error message "Password must meet complexity requirements"

  @Positive
  Scenario: Change password and auto-logout
    When I navigate to the dashboard and click on change password button
    And I enter a new and confirm password
    Then the application auto-logout
    When I login again with the new password
    Then I should logged successfully
