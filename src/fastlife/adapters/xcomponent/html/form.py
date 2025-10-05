from collections.abc import Mapping
from typing import Literal

from xcomponent import XNode

from fastlife.adapters.xcomponent.catalog import catalog


@catalog.component
def Form(
    children: XNode,
    globals: Mapping[str, str],
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
        autofocus={autofocus}
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
    hx_on_after_request: str | None = None,
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
        hx-on::after-request={hx_on_after_request}
        hx-vals={hx_vals}
        hx-confirm={hx_confirm}
        hx-get={hx_get}
        hx-post={hx_post}
        hx-put={hx_put}
        hx-patch={hx_patch}
        hx-delete={hx_delete}
        hx-push-url={
            if isbool(hx_push_url) {
                if hx_push_url { "true" } else { false }
            }
            else { hx_push_url }
        }
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


@catalog.component
def Checkbox(
    name: str,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
    value: str | None = None,
    checked: bool = False,
) -> str:
    """
    Create html ``<input type="checkbox" />`` node.

    :param name: Name of the checkbox
    :param id: unique identifier of the element
    :param class_: css class for the node, defaults to
                  :attr:`fastlife.template_globals.Globals.CHECKBOX_CLASS`
    :param value: http submitted value if the checkbox is checked
    :param checked: Initialized the checkbox as ticked
    """
    return """
        <input
            name={name}
            type="checkbox"
            id={id}
            value={value}
            class={class_ or globals.CHECKBOX_CLASS }
            checked={checked}
            />
    """


@catalog.component
def Password(
    name: str,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
    aria_label: str | None = None,
    placeholder: str | None = None,
    autocomplete: Literal[
        "on",
        "off",
        "current-password",
        "new-password",
    ]
    | None = None,
    inputmode: Literal[
        "none",
        "text",
        "numeric",
    ]
    | None = None,
    minlength: int | None = None,
    maxlength: int | None = None,
    pattern: str | None = None,
    autofocus: bool = False,
    required: bool = False,
    readonly: bool = False,
) -> str:
    """
    Produce ``<input type="password">`` node.

    :param name: submitted name in the form
    :param id: unique identifier of the element
    :param class_: css class for the node, defaults to
                  :attr:`fastlife.template_globals.Globals.INPUT_CLASS`
    :param aria_label: aria-label
    :param placeholder: brief hint to the user as to what kind of information
                        is expected in the field
    :param autocomplete: Define autocomplete mode
    :param inputmode: Define a virtual keyboard layout
    :param minlength: Minimum length
    :param maxlength: Maximum length
    :param pattern: Must match a pattern
    :param autofocus: Give the focus
    :param required: Mark as required field
    :param readonly: Mark as readonly field
    """
    return """
    <input
        name={name}
        type="password"
        id={id}
        aria-label={aria_label}
        placeholder={placeholder}
        autocomplete={autocomplete}
        inputmode={inputmode}
        minlength={minlength}
        maxlength={maxlength}
        pattern={pattern}
        class={class_ or globals.INPUT_CLASS}
        autofocus={autofocus}
        required={required}
        readonly={readonly}
    />
    """


@catalog.component
def Label(
    children: XNode,
    globals: Mapping[str, str],
    for_: str | None = None,
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    Produce ``<label>`` node.

    :param for_: unique identifier of the target element.
    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
                  :attr:`fastlife.template_globals.Globals.LABEL_CLASS`.
    """
    return """
    <label for={for_} class={class_ or globals.LABEL_CLASS} id={id}>
        {children}
    </label>
    """


@catalog.component
def Option(
    children: XNode,
    globals: Mapping[str, str],
    value: str,
    id: str | None = None,
    selected: bool = False,
) -> str:
    """
    Produce ``<option>`` node.

    :param value: posted value after submitted the selected value
    :param id: unique identifier of the element
    :param selected: Used to select the option while rendering the form
    """
    return """
    <option value={value} id={id} selected={selected}>
        {children}
    </option>
    """


@catalog.component
def Select(
    children: XNode,
    globals: Mapping[str, str],
    name: str,
    id: str | None = None,
    class_: str | None = None,
    multiple: bool = False,
) -> str:
    """
    Create html ``<select>`` node.

    :param name: name of the submitted
    :param id: unique identifier of the element
    :param class_: css class for the node, defaults to
                  :attr:`fastlife.template_globals.Globals.SELECT_CLASS`
    :param multiple: Mark as multiple
    """
    return """
    <select name={name} id={id} class={class_ or globals.SELECT_CLASS}
            multiple={multiple}>
        {children}
    </select>
    """


@catalog.component
def Radio(
    globals: Mapping[str, str],
    label: str,
    name: str,
    value: str,
    id: str | None = None,
    checked: bool = False,
    disabled: bool = False,
    onclick: str | None = None,
    div_class: str | None = None,
    class_: str | None = None,
    label_class: str | None = None,
) -> str:
    """
    Produce a ``<input type="radio">`` with its associated label inside a div.

    :param label: label text associated to the radio
    :param name: name of the submitted
    :param value: value that will be submitted if selected
    :param id: unique identifier of the element
    :param checked: Tick the radio button
    :param disabled: Mark the radio button as disabled
    :param onclick: execute some javascript while clicking
    :param div_class: css class for the div node, defaults to
                     :attr:`fastlife.template_globals.Globals.RADIO_DIV_CLASS`
    :param class_: css class for the input node, defaults to
                   :attr:`fastlife.template_globals.Globals.RADIO_INPUT_CLASS`
    :param label_class: css class for the label node, defaults to
                        :attr:`fastlife.template_globals.Globals.RADIO_LABEL_CLASS`
    """

    return """
    <div class={div_class or globals.RADIO_DIV_CLASS}>
        <input type="radio" name={name} id={id} value={value}
            class={class_ or globals.RADIO_INPUT_CLASS}
            onclick={onclick}
            checked={checked}
            disabled={disabled} />
        <Label for={id} class={label_class or globals.RADIO_LABEL_CLASS}>
            {label}
        </Label>
    </div>
    """


@catalog.component
def Textarea(
    children: XNode,
    globals: Mapping[str, str],
    name: str,
    id: str | None = None,
    class_: str | None = None,
    aria_label: str | None = None,
    placeholder: str | None = None,
) -> str:
    """
    html ``<textarea>`` node.

    :param name: name of the submitted
    :param id: unique identifier of the element
    :param class_: css class for the node, defaults to
                   :attr:`fastlife.template_globals.Globals.INPUT_CLASS`
    :param aria_label: aria-label
    :param placeholder: brief hint to the user as to what kind of information
                        is expected in the field
    """

    return """
    <textarea
        name={name}
        id={id}
        aria-label={aria_label}
        placeholder={placeholder}
        class={class_ or globals.INPUT_CLASS}>
        {children}
    </textarea>
    """
