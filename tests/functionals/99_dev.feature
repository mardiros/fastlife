Feature: Basic form
  @dev
  Scenario: Hello world
    Given anonymous user on "/autoform"
    And I wait

  @icons
  Scenario: show icons
    Given anonymous user on "/icons"
    And I wait

  @dev
  @openapi
  Scenario: show openapi docs
    Given anonymous user on "/api/doc"
    And I wait
