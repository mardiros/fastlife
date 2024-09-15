Form
====

.. jinjax:component:: Form(id: str | None = None, class_: str | None = None, method: Literal['get', 'post'] | None = None, action: str | None = None, hx_post: str | Literal[True] | None = None, hx_disable: Literal[True] | None = None, content: Any)

    Create html ``<form>`` node with htmx support by default.
    A :jinjax:component:`CsrfToken` will always be included in the form
    and will be checked by the
    :func:`csrf policy method <fastlife.security.csrf.check_csrf>`.

    ::

      <Form :hx-post="true">
        <Input name="name" placeholder="Bob" />
        <Button>Submit</Button>
      </Form>

    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.templating.renderer.constants.Constants.FORM_CLASS`
    :param method: Http method used
    :param action: url where the form will be submitted
    :param hx_post: url where the form will be submitted using htmx. if ``True``, the current url is used.
    :param hx_disable: if true, then htmx will be disabled for the form and for all its children nodes.
    :param content: child node.
