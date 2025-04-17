@asyncio
Feature: Translation

  Scenario: French
    Given anonymous user on "/fr/hello"
    Then the user sees the text "Salut tout le monde !"
    And the user sees the text "Comment ça va aujourd'hui ?"
    And the user sees the text "T'as qu'une seule vie"
    And the user sees the text "1 pomme"
    And the user sees the text "2 oranges"
    And the user sees the text "banane!"
