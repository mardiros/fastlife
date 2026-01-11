@asyncio
Feature: Pydantic Form Generation

  @wip
  Scenario: Union
    Given anonymous user on "/fr/forms/discriminator_unionfield"
    When the user clicks on the button "The Dog"
    And the user fills the field "nick" with "Mirza"
    And the user fills the field "meows" with "mou"
    And the user clicks on the button "submit"
    Then the user sees the text "Input should be a valid integer, unable to parse string as an integer"
    When the user fills the field "meows" with "42"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {"pet": {"type": "dog", "nick": "Mirza", "meows": 42}}
      """
