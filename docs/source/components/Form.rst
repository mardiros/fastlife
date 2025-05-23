Form
====

.. jinjax:component:: Form(id: str | None = None, class_: str | None = None, method: Literal['get', 'post'] | None = None, action: str | None = None, hx_target: str | None = None, hx_select: str | None = None, hx_swap: str | None = None, hx_post: str | Literal[True] | None = None, hx_disable: Literal[True] | None = None, content: Any)

    Create html ``<form>`` node with htmx support by default.
    A :jinjax:component:`CsrfToken` will always be included in the form
    and will be checked by the
    :func:`csrf policy method <fastlife.service.csrf.check_csrf>`.

    ::

      <Form :hx-post="true">
        <Input name="name" placeholder="Bob" />
        <Button>Submit</Button>
      </Form>

    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.FORM_CLASS`
    :param method: Http method used
    :param action: url where the form will be submitted
    :param hx_target: target the element for swapping than the one issuing the AJAX request.
    :param hx_select: select the content swapped from response of the AJAX request.
    :param hx_swap: specify how the response will be swapped in relative to the target of an AJAX request.
    :param hx_post: url where the form will be submitted using htmx. if ``True``, the current url is used.
    :param hx_disable: if true, then htmx will be disabled for the form and for all its children nodes.
    :param content: child node.
