## 0.26.0  - Released on 2025-03-08
* Add a new method to the configuration to customize the request class.
  See [Configurator.set_request_factory](#fastlife.config.configurator.GenericConfigurator.set_request_factory)

## 0.25.2  - Released on 2025-03-03
* Update deps and fix related bugs in JinjaX components.

## 0.25.1  - Released on 2025-03-02
* Update fews JinjaX components
  * New attributes on Input
  * Add Password component for passwords
  * Make Error and Fatal Errors class configurable
* Update pydantic_form widgets for password
* Add a widget for MFACode

## 0.25.0  - Released on 2025-02-18
* Migrate CSS to tailwincss 4

## 0.24.0  - Released on 2025-01-17
* Add a way to hook the lifespan to the app

## 0.23.1  - Released on 2025-01-14
* Fix typing issue
* Update docs

## 0.23.0  - Released on 2024-12-04
* Update Request type.
  * Breaking changes: Request[TUser, TRegistry] -> Request[TRegistry, TIdentity, TClaimedIdentity].
* Update SecurityPolicy, designed for MFA by default.
  * Breaking changes: new abstract method added. build_authentication_state.
  * Breaking changes: there is no more get_authenticated_userid method.
  * The identity method is not abstract anymore, result comes from the build_authentication_state.
  * New method get_authentication_state, claimed_identity and pre_remember.
* Add a AbstractNoMFASecurityPolicy that build a AbstractSecurityPolicy without TClaimedIdentity as None.
* New ACL type added to raise 401 errors due to missing MFA which may not be same url as tu login/password.

## 0.22.1  - Released on 2024-11-27
* Improve Request typing

## 0.22.0  - Released on 2024-11-23
* Add a way to add fatal errors on form in order to display an error block.
* The localizer can be called gettext in the depency in order to simple translation.
* Expose the 99% of the usefull API in the main package.
* Refactor all internal class to get a more hexagonal approach in order to reduce
  circular dependencies.

## 0.21.0  - Released on 2024-11-15
* Make the InlineTemplate the only way to render views template.
  * Breaking change: template args is not supported in Configutor.add_route.
  * Breaking change: template args is not supported in @view_config.
  * Breaking change: template and Template dedendencies have been removed.
* Add new method in the configurator to register global vars for template:
    {meth}`fastlife.config.configurator.GenericConfigurator.add_renderer_global`.
* Add npgettext i18n helper method support.
* Remove babel from dependency list (only a dev dependency).

## 0.20.1  - Released on 2024-11-09
* Add a new class GenericRegistry in order to properly type custom Configurator / Registry / Settings
* Using InlineTemplate, we can pass arbitrary types for pydantic form

## 0.19.0  - Released on 2024-11-07
* Drop Babel from depenencies for i18n, rely on GNUTranslations only
* Change License to MIT
* Replace poetry by uv/pdm
* Update CI workflows

## 0.18.0  - Released on 2024-10-13
* Make the sphinx pluging {mod}`fastlife.adapters.jinjax.jinjax_ext.jinjax_doc`
  parts from the API in order to let users build their own component documentation.

## 0.17.0  - Released on 2024-10-08
* Fix @configure decorator signature for GenericConfigurator
* Breaking change - rename Configurator.set_open_tag to Configurator.set_openapi_tag

## 0.16.4  - Released on 2024-10-04
* Add support of x-real-port for port detection, fallback port to 0 instead of None if missing

## 0.16.3  - Released on 2024-10-03
* Fix middleware that process the x-forwarded-headers to respect ASGI spec for client

## 0.16.2  - Released on 2024-10-03
* Add a new property all_registered_permissions on the Configurator class

## 0.16.1  - Released on 2024-10-03
* Fix import in the SecurityPolicy that make it unusable.

## 0.16.0  - Released on 2024-10-02
* Make the Configurator, Request and Registry Generic.
* Breaking change, remove settings `api_swagger_ui_url` and `api_redoc_url`
  now to register those url, use
  {meth}`fastlife.config.configurator.GenericConfigurator.set_api_documentation_info`
* Breaking change, in the method
  {meth}`fastlife.config.configurator.GenericConfigurator.set_api_documentation_info`
  summary is now kwargs only.

## 0.15.1  - Released on 2024-09-29
* Hotfix components to create tables

## 0.15.0  - Released on 2024-09-29
* Add an {class}`fastlife.service.security_policy.AbstractSecurityPolicy` class
* New method {meth}`fastlife.config.configurator.GenericConfigurator.set_security_policy`
* Breaking change, the check_permission has been removed from the settings.
  to configure the permission policy, a security policy has to be implemented.

## 0.14.0  - Released on 2024-09-26
* Implemement method add_template_search_path in the configurator
* Add a route_prefix in the configurator for configurator.include

## 0.13.0  - Released on 2024-09-25
* Add a way to handle api
* Add a @view_config decorator to register route
* Add a @resource decorator to handle CRUD resource in rest format
* Add @exception_handler decorator
* Add i18n support

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
