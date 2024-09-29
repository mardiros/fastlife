Feature: Authentication/Authorization

  Scenario: Redirect to login page, view secured page, logout and redirect home
    Given anonymous user on "/admin/secured"
    Then I see the text "Let's authenticate"
    When I fill the field "username" with "Alice"
    When I fill the field "password" with "secret"
    And I click on the "button" "login"
    Then I see the text "Welcome back Alice!"
    When I click on the "link" "logout"
    Then I see the text "Hello World!"
