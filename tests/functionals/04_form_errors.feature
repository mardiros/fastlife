Feature: Pydantic Form Errors

  @wip
  Scenario: Fatal error
    Given anonymous user on "/admin/login"
    When I fill the field "username" with "root"
    And I fill the field "password" with "aintnosuccess"
    And I click on the "button" "Login"
    Then I see the text "Something went wrong"
