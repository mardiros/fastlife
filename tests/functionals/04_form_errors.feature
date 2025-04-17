@asyncio
Feature: Pydantic Form Errors

  Scenario: Fatal error
    Given anonymous user on "/admin/login"
    When the user fills the field "username" with "root"
    And the user fills the field "password" with "aintnosuccess"
    And the user clicks on the button "Login"
    Then the user sees the text "Something went wrong"
