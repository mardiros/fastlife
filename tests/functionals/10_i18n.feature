Feature: Translation

  @wip
  Scenario: French
    Given anonymous user on "/fr/hello"
    Then I see the text "Salut tout le monde !"
    And I see the text "Comment ça va aujourd'hui ?"
