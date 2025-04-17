@asyncio
Feature: Basic form

  Scenario: Hello world
    Given anonymous user on "/"
    Then the user sees the text "Hello World!"
    When the user fills the field "Name" with "Alice"
    And the user clicks on the button "submit"
    Then the user sees the text "Hello Alice!"
