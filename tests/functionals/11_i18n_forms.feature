@asyncio
Feature: Pydantic Form Generation

  @wip
  Scenario: Union
    Given anonymous user on "/fr/forms/discriminator_unionfield"
    And the user waits
    When the user fills the field "nickname" with "Alice"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "nick": "Alice"
      }
      """
