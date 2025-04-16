@asyncio
Feature: Translation

  Scenario: French
    Given anonymous user on "/fr/hello"
    Then the user see the text "Salut tout le monde !"
    And the user see the text "Comment ça va aujourd'hui ?"
    And the user see the text "T'as qu'une seule vie"
    And the user see the text "1 pomme"
    And the user see the text "2 oranges"
    And the user see the text "banane!"
