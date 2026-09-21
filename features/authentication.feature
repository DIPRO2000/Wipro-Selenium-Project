Feature: Authentication API
  As an API automation trainee
  I want to verify documented login behavior
  So that credential verification is covered by Behave BDD

  Scenario: Verify login with valid disposable-account credentials
    Given the API client is configured
    And a disposable account exists
    When I verify login with the disposable account credentials
    Then the HTTP status should be 200
    And the API response code should be 200
    And the response message should be "User exists!"

  Scenario: Reject invalid login credentials
    Given the API client is configured
    When I verify login with invalid credentials
    Then the HTTP status should be 200
    And the API response code should be 404
    And the response message should be "User not found!"

  Scenario: Reject login without the email parameter
    Given the API client is configured
    When I verify login without the email parameter
    Then the HTTP status should be 200
    And the API response code should be 400
    And the response message should be "Bad request, email or password parameter is missing in POST request."

  Scenario: Reject DELETE on the login-verification endpoint
    Given the API client is configured
    When I send a DELETE request to the login verification endpoint
    Then the HTTP status should be 200
    And the API response code should be 405
    And the response message should be "This request method is not supported."
