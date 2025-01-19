Feature: Platform Admin Password Management

  Background:
    Given I am logged in as a platform administrator
    And I navigate to the User Management section to update the password

  @Negative
  Scenario: Handling mismatched new and confirm passwords
    When I enter a new password that does not match the confirm password
    Then an error message "Passwords do not match" is displayed

  @Negative
  Scenario: Handling blank password fields
    When I leave the new password and confirm password fields blank
    Then an error message "Password fields cannot be empty" is displayed

  @Negative
  Scenario: Handling passwords that violate security norms
    When I enter a password that does not meet the required complexity standards
    Then an error message "Password must include uppercase, lowercase, numbers, and special characters" is displayed

  @Positive
  Scenario: Successfully updating and re-logging in with a new password
    When I enter matching passwords that meet the required complexity standards
    Then the system logs me out automatically relogin with updated password
    Then I am successfully logged in
