Feature: Pydantic Form Generation

  Scenario: Textfield
    Given anonymous user on "/form/textfield"
    When I fill the field "nickname" with "Alice"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {"nick":"Alice"}
      """

  Scenario: Intfield
    Given anonymous user on "/form/intfield"
    When I fill the field "seconds" with "42"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {"seconds": 42}
      """

  Scenario: Float
    Given anonymous user on "/form/floatfield"
    When I fill the field "fm station" with "103.3"
    And I click on the "button" "submit" with response info
    Then I see the json
      """
      {"fm": 103.3}
      """


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
    Then I see the json
      """
      {"hobbies": ["reading", "cooking"]}
      """

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
    Then I see the json
      """
      {"pets": ["dog", "cat"]}
      """
