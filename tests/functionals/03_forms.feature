Feature: Pydantic Form Generation

  Scenario: Textfield
    Given anonymous user on "/form/textfield"
    When I fill the field "nickname" with "Alice"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {"nick":"Alice"}
      """

  Scenario: integer
    Given anonymous user on "/form/intfield"
    When I fill the field "seconds" with "42"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {"seconds": 42}
      """

  Scenario: float
    Given anonymous user on "/form/floatfield"
    When I fill the field "fm station" with "103.3"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {"fm": 103.3}
      """

  # # not implemented yet
  # # Scenario: datetime
  # #   Given anonymous user on "/form/datetimefield"
  # #   When I fill the field "rendez-vous" with "2024-01-02"
  # #   Then I see the json
  # #     """
  # #     {"rdv": "2024-01-02T00:00:00Z"}
  # #     """

  Scenario: Bool
    Given anonymous user on "/form/booleanfield"
    When I click on the "checkbox" "Accept contract"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {"aggreed": true}
      """

  Scenario: Set[Literal]
    Given anonymous user on "/form/literalsfield"
    When I click on the "checkbox" "cooking"
    When I click on the "checkbox" "reading"
    And I click on the "button" "submit" with response info
    Then I see the python set "{"reading", "cooking"}" in "hobbies"

  Scenario: Enum
    Given anonymous user on "/form/enumfield"
    When I select the option "female" of "Gender"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {"gender": "female"}
      """

  Scenario: Set[Enum]
    Given anonymous user on "/form/enumsfield"
    When I click on the "checkbox" "lazy dog"
    When I click on the "checkbox" "crazy cat"
    And I click on the "button" "submit" with response info
    Then I see the python set "{"dog", "cat"}" in "pets"

  Scenario: Sequence[str]
    Given anonymous user on "/form/string_sequence"
    When I click on the "button" "Add"
    And I fill the field "0" with "foo"
    When I click on the "button" "Add"
    And I fill the field "1" with "bar"
    And I click on the "button" "submit" with response info
      """
      {"aliases": ["foo", "bar"]}
      """

  Scenario: Model
    Given anonymous user on "/form/model"
    When I fill the field "First name" with "John"
    And I fill the field "Last name" with "Connor"
    And I fill the field "Age" with "16"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {
        "person": {
          "fistname": "John",
          "lastname": "Connor",
          "age": 16
        }
      }
      """
