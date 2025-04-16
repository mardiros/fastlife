@asyncio
Feature: Pydantic Form Errors

  Scenario: Fatal error
    Given anonymous user on "/admin/login"
    When the user fill the field "username" with "root"
    And the user fill the field "password" with "aintnosuccess"
    And the user click on the button "Login"
    Then the user see the text "Something went wrong"
