## 0.12.0  - Released on 2024-09-19
* Add a way to register API routes and expose api doc

## 0.11.1  - Released on 2024-09-18
* Update FastAPI version

## 0.11.0  - Released on 2024-09-18
* Huge documentation update
  * Use sphinx-autodoc2
  * Add documentation for the components.
* Breaking change in the configurator.
  * get_app has been renamed get_asgi_app
  * a few internals classes moved/renamed.

## 0.10.0  - Released on 2024-08-24

* Rename model_result and ModelResult to form_model and FormModel
* Add an edit method for FormModel
* Add a Textarea widget and fix Hidden widget
* Fix rendering of sequence
* Do not render main form as nested models
* Add many functional tests for form field generations

## 0.9.7  - Released on 2024-08-21

* Add title attribute to icons

## 0.9.6  - Released on 2024-08-18

* Add more buttons options for htmx ajax call
* Fix Option id

## 0.9.5  - Released on 2024-08-17

* Use icons to customize collapsible widget for sequence
* Add parameter for button to avoid send params

## 0.9.4  - Released on 2024-08-16

* Don't update browser url while manipulating autoform lists

## 0.9.3  - Released on 2024-08-16

* Fix autoform widgets from jinjax migration

## 0.9.2  - Released on 2024-08-13

* Add a constants class for global variable in templates
* Use icons to customize collapsible widget

## 0.9.1  - Released on 2024-08-12

* Replace fa icons by hero icons

## 0.9.0  - Released on 2024-08-12

* Add fa Icons (extra)

## 0.8.0  - Released on 2024-08-10

* Upgrade JinjaX (Template update required, use vue-like syntax now)

## 0.7.3  - Released on 2024-08-10

* Add some HTML markup

## 0.7.2  - Released on 2024-08-07

* Fix https behind a reverse proxy

## 0.7.1  - Released on 2024-08-04

* Add the registry on request for exception handler

## 0.7.0  - Released on 2024-08-04

* Rewrite how the registry is handled, now part of the request (request.registry)
* Update to get hx-confirm and hx-delete on button

## 0.6.1  - Released on 2024-04-27

* Display errors on every widget

## 0.6.0  - Released on 2024-04-25

* Refactor the pydantic_form to start handling errors in form.

## 0.5.1  - Released on 2024-04-24

* Fix minimum dependency version for JinjaX

## 0.5.0  - Released on 2024-04-24

* Implement new types for pydantic form: Enum, Set[Literal] and Set[Enum]

## 0.4.1  - Released on 2024-04-20

* Add globals to render custom widget with global data

## 0.4.0  - Released on 2024-04-20

* Update JinjaX for global template var support
* Add lots of missing unit tests
* Add support of more html form element
* Update deps

## 0.3.1  - Released on 2024-03-29

* Update FastAPI

## 0.3.0  - Released on 2024-03-29

* Replace jinja2 by JinjaX

## 0.2.3  - Released on 2024-01-29

* Add support of relative import in :class:`Configurator.include` method

## 0.2.2  - Released on 2024-01-28

* Add another settings for session domain cookie
* Update test client wrapper and also wrap bs4 tag
* Fix session cleanup to properly logout

## 0.2.1  - Released on 2024-01-27

* Change add_route signature
  * Set the name of the route mandatory and first argument (breaking change)
  * Add a permission argument
  * Add a settings to inject a check_permission handler

## 0.2.0  - Released on 2024-01-24

* Add a session wrapper in the test client
  Allows to initialize session data in tests

## 0.1.2  - Released on 2024-01-15

* Handle sessions

## 0.1.1  - Released on 2024-01-05

* Update fastapi depencency

## 0.1.0  - Released on 2024-01-05

* Initial release
