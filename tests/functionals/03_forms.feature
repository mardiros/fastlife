Feature: Pydantic Form Generation

  Scenario: Textfield
    Given anonymous user on "/form/textfield"
    When the user fill the field "nickname" with "Alice"
    And the user click on the button "submit" with response info
    Then the user see the json
      """json
      {
        "nick": "Alice"
      }
      """

  Scenario: integer
    Given anonymous user on "/form/intfield"
    When the user fill the field "seconds" with "42"
    And the user click on the button "submit" with response info
    Then the user see the json
      """json
      {
        "seconds": 42
      }
      """

  Scenario: float
    Given anonymous user on "/form/floatfield"
    When the user fill the field "fm station" with "103.3"
    And the user click on the button "submit" with response info
    Then the user see the json
      """json
      {
        "fm": 103.3
      }
      """
  # # not implemented yet
  # # Scenario: datetime
  # #   Given anonymous user on "/form/datetimefield"
  # #   When the user fill the field "rendez-vous" with "2024-01-02"
  # #   Then the user see the json
  # #     """json
  # #     {"rdv": "2024-01-02T00:00:00Z"}
  # #     """

  Scenario: Bool
    Given anonymous user on "/form/booleanfield"
    When the user click on the checkbox "Accept contract"
    And the user click on the button "submit" with response info
    Then the user see the json
      """json
      {
        "aggreed": true
      }
      """

  Scenario: Set[Literal]
    Given anonymous user on "/form/literalsfield"
    When the user click on the checkbox "cooking"
    When the user click on the checkbox "reading"
    And the user click on the button "submit" with response info
    Then the user see the python set in "hobbies"
      """python
      {"reading", "cooking"}
      """

  Scenario: Enum
    Given anonymous user on "/form/enumfield"
    When I select the option "female" of "Gender"
    And the user click on the button "submit" with response info
    Then the user see the json
      """json
      {
        "gender": "female"
      }
      """

  Scenario: Set[Enum]
    Given anonymous user on "/form/enumsfield"
    When the user click on the checkbox "lazy dog"
    When the user click on the checkbox "crazy cat"
    And the user click on the button "submit" with response info
    Then the user see the python set in "pets"
      """python
      {"dog", "cat"}
      """
  Scenario: Sequence[str]
    Given anonymous user on "/form/string_sequence"
    When the user click on the button "Add"
    And the user fill the field "0" with "foo"
    When the user click on the button "Add"
    And the user fill the field "1" with "bar"
    And the user click on the button "submit" with response info
    Then the user see the json
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
    When the user fill the field "First name" with "John"
    And the user fill the field "Last name" with "Connor"
    And the user fill the field "Age" with "16"
    And the user click on the button "submit" with response info
    Then the user see the json
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
    When I fill the textarea "Aliases" with
      """
      foo
      bar
      """
    And the user click on the button "submit" with response info
    Then the user see the json
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
    When the user fill the field "name" with "Bob"
    And the user click on the button "submit" with response info
    Then the user see the json
      """json
      {
        "id": 42,
        "name": "Bob"
      }
      """

  Scenario: Union Field
    Given anonymous user on "/form/unionfield"
    When the user click on the button "Dog"
    And the user fill the field "nick" with "Buffy"
    And the user click on the button "submit" with response info
    Then the user see the json
      """json
      {
        "pet": {"type": "dog", "nick": "Buffy"}
      }
      """
