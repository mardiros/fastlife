@asyncio
Feature: Authentication/Authorization

  @wip
  Scenario: Redirect to login page, view secured page, logout and redirect home
    Given anonymous user on "/admin/secured"
    Then the user sees the text "Let's authenticate"
    When the user fills the field "username" with "Alice"
    When the user fills the field "password" with "secret"
    And the user clicks on the button "login"
    When the user fills the field "code" with "1234"
    And the user clicks on the button "login"
    Then the user sees the text "Welcome back Alice!"
    When the user clicks on the link "logout"
    Then the user sees the text "Hello World!"
