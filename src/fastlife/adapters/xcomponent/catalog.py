from collections.abc import Mapping
from typing import Literal

from xcomponent import Catalog, XNode

catalog = Catalog()
"""The catalog to register components."""


@catalog.component
def H1(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    <h1> html tag rendering

    :param children: child node.
    :param globals: injected root component globals variables.
    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.H1_CLASS`.
    """
    return """
        <h1 id={id} class={class_ or globals.H1_CLASS}>
            {children}
        </h1>
    """


@catalog.component
def Form(
    id: str | None = None,
    class_: str | None = None,
    method: Literal["get", "post"] | None = None,
    action: str | None = None,
    hx_target: str | None = None,
    hx_select: str | None = None,
    hx_swap: str | None = None,
    hx_post: str | Literal[True] | None = None,
    hx_disable: Literal[True] | None = None,
) -> str:
    return """
        <form
            id={id}
            class={class_ or globals.FORM_CLASS}
            hx-disable={hx_disable}
            hx-post={hx_post}
            hx-select={hx_select}
            hx-swap={hx_swap}
            hx-target={hx_target}
            action={action}
            method={method}
            >
            <CsrfToken />
            { children }
        </form>
    """


@catalog.component
def CsrfToken(globals: dict[str, str]) -> str:
    return """
        <Hidden
            name={globals.request.csrf_token.name}
            value={globals.request.csrf_token.value}
            />
    """


@catalog.component
def Input(
    name: str,
    value: str = "",
    type: str = "text",
    id: str | None = None,
    class_: str | None = None,
    aria_label: str | None = None,
    placeholder: str | None = None,
    inputmode: Literal[
        "none", "text", "decimal", "numeric", "tel", "search", "email", "url"
    ]
    | None = None,
    autocomplete: Literal[
        "on",
        "off",
        "name",
        "username",
        "current-password",
        "new-password",
        "one-time-code",
        "email",
        "tel",
        "organization",
        "street-address",
        "address-line1",
        "address-line2",
        "address-line3",
        "postal-code",
        "country",
        "country-name",
        "cc-name",
        "cc-number",
        "cc-exp",
        "cc-csc",
        "tel-country-code",
        "tel-national",
        "tel-area-code",
        "tel-local",
        "tel-extension",
        "bday",
        "bday-day",
        "bday-month",
        "bday-year",
        "transaction-amount",
        "transaction-currency",
    ]
    | None = None,
    autofocus: bool = False,
) -> str:
    return """
    <input
        type={type}
        name={name}
        value={value}
        id={id}
        aria-label={ aria_label }
        placeholder={ placeholder }
        inputmode={inputmode}
        autocomplete={autocomplete}
        class={class_ or globals.INPUT_CLASS}
        autofocus
    />
    """


@catalog.component
def Hidden(
    name: str,
    value: str,
    id: str | None = None,
) -> str:
    return """
        <input name={name} value={value} type="hidden" id={id} />
    """


@catalog.component
def Button(
    children: XNode,
    globals: Mapping[str, str],
    type: Literal["submit", "button", "reset"] = "submit",
    id: str | None = None,
    class_: str | None = None,
    name: str = "action",
    value: str = "submit",
    hidden: bool = False,
    aria_label: str | None = None,
    onclick: str | None = None,
    hx_target: str | None = None,
    hx_swap: str | None = None,
    hx_select: str | None = None,
    hx_after_request: str = "",
    hx_vals: str | None = None,
    hx_confirm: str | None = None,
    hx_get: str | None = None,
    hx_post: str | None = None,
    hx_put: str | None = None,
    hx_patch: str | None = None,
    hx_delete: str | None = None,
    hx_params: str | None = None,
    hx_push_url: bool = False,
    full_width: bool = False,
) -> str:
    return """
    <button
        type={type}
        name={name}
        value={value}
        id={id}
        hx-target={hx_target}
        hx-swap={hx_swap}
        hx-select={hx_select}
        onclick={onclick}
        hx-on::after-request={hx_after_request}
        hx-vals={hx_vals}
        hx-confirm={hx_confirm}
        hx-get={hx_get}
        hx-post={hx_post}
        hx-put={hx_put}
        hx-patch={hx_patch}
        hx-delete={hx_delete}
        hx-push-url={hx_push_url}
        hx-params={hx_params}
        aria-label={aria_label}
        class={
            if full_width {
                "w-full " + (class_ or globals.BUTTON_CLASS)
            }
            else {
                class_ or globals.BUTTON_CLASS
            }
        }
        hidden={hidden}
        >
        {children}
    </button>
    """
