Feature: Authentication/Authorization

  Scenario: Redirect to login page, view secured page, logout and redirect home
    Given anonymous user on "/admin/secured"
    Then the user see the text "Let's authenticate"
    When the user fill the field "username" with "Alice"
    When the user fill the field "password" with "secret"
    And the user click on the button "login"
    When the user fill the field "code" with "1234"
    And the user click on the button "login"
    Then the user see the text "Welcome back Alice!"
    When the user click on the link "logout"
    Then the user see the text "Hello World!"
