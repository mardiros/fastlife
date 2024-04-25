0.6.0  - Released on 2024-04-25
-------------------------------
* Refactor the pydantic_form to start handling errors in form.

0.5.1  - Released on 2024-04-24
-------------------------------
* Fix minimum dependency version for JinjaX

0.5.0  - Released on 2024-04-24
-------------------------------
* Implement new types for pydantic form: Enum, Set[Literal] and Set[Enum]

0.4.1  - Released on 2024-04-20
-------------------------------
* Add globals to render custom widget with global data

0.4.0  - Released on 2024-04-20
-------------------------------
* Update JinjaX for global template var support
* Add lots of missing unit tests
* Add support of more html form element
* Update deps

0.3.1  - Released on 2024-03-29
-------------------------------
* Update FastAPI

0.3.0  - Released on 2024-03-29
-------------------------------
* Replace jinja2 by JinjaX

0.2.3  - Released on 2024-01-29
-------------------------------
* Add support of relative import in :class:`Configurator.include` method

0.2.2  - Released on 2024-01-28
-------------------------------
* Add another settings for session domain cookie
* Update test client wrapper and also wrap bs4 tag
* Fix session cleanup to properly logout

0.2.1  - Released on 2024-01-27
-------------------------------
* Change add_route signature
  * Set the name of the route mandatory and first argument (breaking change)
  * Add a permission argument
  * Add a settings to inject a check_permission handler

0.2.0  - Released on 2024-01-24
-------------------------------
* Add a session wrapper in the test client
  Allows to initialize session data in tests

0.1.2  - Released on 2024-01-15
-------------------------------
* Handle sessions

0.1.1  - Released on 2024-01-05
-------------------------------
* Update fastapi depencency

0.1.0  - Released on 2024-01-05
-------------------------------
* Initial release
