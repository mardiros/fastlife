@asyncio
Feature: Pydantic Form Generation

  Scenario: Textfield
    Given anonymous user on "/form/textfield"
    When the user fills the field "nickname" with "Alice"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "nick": "Alice"
      }
      """

  Scenario: integer
    Given anonymous user on "/form/intfield"
    When the user fills the field "seconds" with "42"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "seconds": 42
      }
      """

  Scenario: float
    Given anonymous user on "/form/floatfield"
    When the user fills the field "fm station" with "103.3"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "fm": 103.3
      }
      """
  # # not implemented yet
  # # Scenario: datetime
  # #   Given anonymous user on "/form/datetimefield"
  # #   When the user fills the field "rendez-vous" with "2024-01-02"
  # #   Then the user sees the json
  # #     """json
  # #     {"rdv": "2024-01-02T00:00:00Z"}
  # #     """

  Scenario: Bool
    Given anonymous user on "/form/booleanfield"
    When the user clicks on the checkbox "Accept contract"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "aggreed": true
      }
      """

  Scenario: Set[Literal]
    Given anonymous user on "/form/literalsfield"
    When the user clicks on the checkbox "cooking"
    When the user clicks on the checkbox "reading"
    And the user clicks on the button "submit" with response info
    Then the user sees the python set in "hobbies"
      """python
      {"reading", "cooking"}
      """

  Scenario: Enum
    Given anonymous user on "/form/enumfield"
    When the user selects the option "female" of "Gender"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "gender": "female"
      }
      """

  Scenario: Set[Enum]
    Given anonymous user on "/form/enumsfield"
    When the user clicks on the checkbox "lazy dog"
    When the user clicks on the checkbox "crazy cat"
    And the user clicks on the button "submit" with response info
    Then the user sees the python set in "pets"
      """python
      {"dog", "cat"}
      """
  Scenario: Sequence[str]
    Given anonymous user on "/form/string_sequence"
    When the user clicks on the button "Add"
    And the user fills the field "0" with "foo"
    When the user clicks on the button "Add"
    And the user fills the field "1" with "bar"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "aliases": [
          "foo",
          "bar"
        ]
      }
      """

  Scenario: Model
    Given anonymous user on "/form/model"
    When the user fills the field "First name" with "John"
    And the user fills the field "Last name" with "Connor"
    And the user fills the field "Age" with "16"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "professor": {
          "firstname": "John",
          "lastname": "Connor",
          "age": 16
        }
      }
      """

  Scenario: Sequence[str] with custom widget
    Given anonymous user on "/form/string_sequence_widget"
    When the user fills the textarea "Aliases" with
      """
      foo
      bar
      """
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "aliases": [
          "foo",
          "bar"
        ]
      }
      """

  Scenario: Hidden field
    Given anonymous user on "/form/hiddenfield"
    When the user fills the field "name" with "Bob"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "id": 42,
        "name": "Bob"
      }
      """

  Scenario: Union Field
    Given anonymous user on "/form/unionfield"
    When the user clicks on the button "Dog"
    And the user fills the field "nick" with "Buffy"
    And the user clicks on the button "submit" with response info
    Then the user sees the json
      """json
      {
        "pet": {"type": "dog", "nick": "Buffy"}
      }
      """
