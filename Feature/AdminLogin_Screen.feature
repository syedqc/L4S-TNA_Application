@order_1
Feature: Verifying TNA Login Page Functionality

  Background:
    Given I lunched the TNA Login Page

  @Positive
  Scenario: Login with valid credentials
    Given Enter the valid username and password
    When Click on the signin button
    Then Verify "home dashboard" is displayed

  @Negative
  Scenario: Login with an invalid username and password
    Given Enter the invalid username and password
    When Click on the signin button
    Then Verify "Invalid username or password" is displayed
  @Negative
  Scenario: Login with a valid username and incorrect password
    Given Enter the valid username and invalid password
    When Click on the signin button
    Then Verify "Incorrect password" is displayed
  @Negative
  Scenario: Login with an invalid username and a valid password
    Given Enter the invalid username and valid password
    When Click on the signin button
    Then Verify "error message" is displayed
  @Negative
  Scenario: Leaving username blank and password blank
    Given Enter the no username and password
    When Click on the signin button
    Then Verify "Username and password cannot be blank" is displayed

