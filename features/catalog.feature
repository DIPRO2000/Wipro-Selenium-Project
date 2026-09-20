Feature: Catalog API
  As an API automation trainee
  I want to validate the documented catalog endpoints
  So that product and brand catalog behavior is covered with Behave BDD

  Scenario: Get all products
    Given the API client is configured
    When I request the all products list
    Then the HTTP status should be 200
    And the API response code should be 200
    And the response should contain a non-empty "products" list
    And each item in the "products" list should contain fields "id", "name", "price", "brand", and "category"

  Scenario: Get all brands
    Given the API client is configured
    When I request the all brands list
    Then the HTTP status should be 200
    And the API response code should be 200
    And the response should contain a non-empty "brands" list
    And each item in the "brands" list should contain fields "id" and "brand"

  Scenario: Search products with a valid term
    Given the API client is configured
    When I search products for "top"
    Then the HTTP status should be 200
    And the API response code should be 200
    And the response should contain a non-empty "products" list
    And each item in the "products" list should contain fields "id", "name", "price", "brand", and "category"

  Scenario: Reject a product search without the required parameter
    Given the API client is configured
    When I search products without a search term
    Then the HTTP status should be 200
    And the API response code should be 400
    And the response message should be "Bad request, search_product parameter is missing in POST request."
