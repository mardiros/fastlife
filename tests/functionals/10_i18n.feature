Feature: Translation

  @wip
  Scenario: French
    Given anonymous user on "/fr/hello"
    Then I see the text "Salut tout le monde !"
    And I see the text "Comment ça va aujourd'hui ?"
    And I see the text "T'as qu'une seule vie"
    And I see the text "1 pomme"
    And I see the text "2 oranges"
    And I see the text "banane!"
