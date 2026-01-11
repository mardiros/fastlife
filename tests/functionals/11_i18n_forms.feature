@asyncio
Feature: Pydantic Form Generation

  @wip
  Scenario: Union
    Given anonymous user on "/fr/forms/discriminator_unionfield"
    When the user clicks on the button "The Dog"
    And the user fills the field "nick" with "Mirza"
    And the user fills the field "meows" with "mou"
    And the user clicks on the button "submit"
    And the user waits
