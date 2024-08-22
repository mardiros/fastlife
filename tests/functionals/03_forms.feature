Feature: Pydantic Form Generation

  Scenario: Textfield
    Given anonymous user on "/form/textfield"
    When I fill the field "nickname" with "Alice"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {"nick":"Alice"}
      """
