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
