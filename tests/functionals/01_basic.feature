Feature: Basic form

  Scenario: Hello world
    Given anonymous user on "/"
    Then the user see the text "Hello World!"
    When the user fill the field "Name" with "Alice"
    And the user click on the button "submit"
    Then the user see the text "Hello Alice!"
