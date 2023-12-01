Feature: Basic form

  Scenario: Hello world
    Given anonymous user on "/"
    Then I see the text "Hello World!"
    When I fill the field "First name and last name, or surname" with "Alice"
    And I click on the button "submit"
    Then I see the text "Hello Alice!"

